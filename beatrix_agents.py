"""
BEATRIX Multi-Agent-System mit LangGraph
=========================================

Ein Multi-Agent-System, das die BCM 2.0 Module (AWX, INU, JNY, etc.)
als spezialisierte Agenten implementiert.

Architektur:
    User Query
         │
         ▼
    ┌─────────┐
    │ Router  │ ──→ Entscheidet welche Module relevant sind
    └────┬────┘
         │
    ┌────┴────┬────────────┬────────────┐
    ▼         ▼            ▼            ▼
┌───────┐ ┌───────┐   ┌───────┐   ┌───────┐
│  AWX  │ │  INU  │   │  JNY  │   │  ...  │
│ Agent │ │ Agent │   │ Agent │   │       │
└───┬───┘ └───┬───┘   └───┬───┘   └───┬───┘
    │         │           │           │
    └─────────┴─────┬─────┴───────────┘
                    ▼
              ┌───────────┐
              │Synthesizer│ ──→ Kombiniert Antworten
              └─────┬─────┘
                    ▼
               Finale Antwort
"""

import json
import os
from pathlib import Path
from typing import TypedDict, Annotated, Literal
from operator import add

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage

# Lade Umgebungsvariablen
load_dotenv()

# =============================================================================
# KONFIGURATION
# =============================================================================

# Pfad zu den BCM-Modulen
BASE_PATH = Path(__file__).parent

# Modul-Mapping: ID → Ordner/Dateiname
MODULE_MAP = {
    "meta": ("meta", "meta.json"),      # 7232 - Meta-Axiome
    "inu": ("inu", "inu.json"),         # 7234 - Individual Utility
    "knu": ("knu", "knu.json"),         # 7235 - Kollektiver Nutzen
    "idn": ("idn", "idn.json"),         # 7236 - Identitäts-Nutzen
    "awx": ("awx", "awx.json"),         # 7240 - Awareness
    "wax": ("wax", "wax.json"),         # 7243 - Willingness
    "context": ("context", "context.json"),  # 8904 - Kontext
    "seg": ("seg", "seg.json"),         # 7257 - Segmentierung
    "jny": ("jny", "jny.json"),         # 7256 - Journey
    "wtx": ("wtx", "wtx.json"),         # 7260 - Wahrscheinlichkeit
    "int": ("int", "int.json"),         # 9250 - Intervention
}

# Modul-Beschreibungen für den Router
MODULE_DESCRIPTIONS = {
    "meta": "Meta-Axiome und Governance-Regeln des BCM 2.0 Systems",
    "inu": "Individueller Nutzen (FEPSDE: Financial, Emotional, Physical, Social, Digital, Ecological)",
    "knu": "Kollektiver Nutzen für Gruppen und Gesellschaft",
    "idn": "Identitäts-Nutzen (Zugehörigkeit, Anerkennung, Selbstbild)",
    "awx": "Awareness-Funktion: Wie wird potenzieller Nutzen wahrgenommen?",
    "wax": "Willingness-Funktion: Handlungsbereitschaft und Entscheidungsschwellen",
    "context": "Kontext-Logik: Institutionelle, soziale und mediale Einflüsse",
    "seg": "Segmentierung: Leaders, Early Adopters, Pragmatists, Followers, Skeptics, Resistants",
    "jny": "Behavioral Change Journey: 5 Phasen der Verhaltensänderung",
    "wtx": "Wahrscheinlichkeitsfunktionen für Entscheidungen",
    "int": "Interventions-Toolkit: Design von Verhaltensinterventionen",
}


# =============================================================================
# LLM SETUP
# =============================================================================

def get_llm():
    """Initialisiert das LLM basierend auf Umgebungsvariablen."""
    provider = os.getenv("LLM_PROVIDER", "openai")

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0.3,
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
        )


# =============================================================================
# STATE DEFINITION
# =============================================================================

class AgentResponse(TypedDict):
    """Antwort eines einzelnen Modul-Agenten."""
    module: str
    response: str
    relevant_axioms: list[str]


class BeatrixState(TypedDict):
    """Gemeinsamer State für alle Agenten im Graph."""
    # Input
    query: str

    # Router-Entscheidung
    relevant_modules: list[str]

    # Modul-Antworten (werden aggregiert)
    module_responses: Annotated[list[AgentResponse], add]

    # Finale Antwort
    final_response: str


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def load_module(module_id: str) -> dict:
    """Lädt ein BCM-Modul aus der JSON-Datei."""
    if module_id not in MODULE_MAP:
        raise ValueError(f"Unbekanntes Modul: {module_id}")

    folder, filename = MODULE_MAP[module_id]
    path = BASE_PATH / folder / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_axioms(module_data: dict, max_axioms: int = 10) -> list[dict]:
    """Extrahiert die wichtigsten Axiome aus einem Modul."""
    axioms = []

    # Verschiedene Strukturen je nach Modul
    if "A4_Axioms" in module_data:
        # JNY-Struktur
        axioms = module_data["A4_Axioms"][:max_axioms]
    elif "axioms" in module_data:
        # Andere Module
        axiom_data = module_data["axioms"]
        if isinstance(axiom_data, dict):
            for key, value in list(axiom_data.items())[:max_axioms]:
                axioms.append({"id": key, **value} if isinstance(value, dict) else {"id": key, "content": value})
        elif isinstance(axiom_data, list):
            axioms = axiom_data[:max_axioms]

    return axioms


def format_module_context(module_id: str, module_data: dict) -> str:
    """Formatiert Modul-Daten als Kontext für den Agenten."""
    # Extrahiere Metadaten
    meta_info = ""
    if "module" in module_data:
        meta = module_data["module"]
        meta_info = f"Modul: {meta.get('name', module_id)}\n"
        meta_info += f"Version: {meta.get('version', 'N/A')}\n"
    elif "A1" in module_data:
        meta = module_data["A1"]
        meta_info = f"Modul: {meta.get('module_name', module_id)}\n"
        meta_info += f"Version: {meta.get('version', 'N/A')}\n"
        meta_info += f"Beschreibung: {meta.get('description', '')[:500]}...\n"

    # Extrahiere Axiome
    axioms = extract_axioms(module_data)
    axiom_text = "\n".join([
        f"- {ax.get('id', 'N/A')}: {ax.get('title', ax.get('description', '')[:100])}"
        for ax in axioms
    ])

    return f"{meta_info}\nWichtige Axiome:\n{axiom_text}"


# =============================================================================
# ROUTER AGENT
# =============================================================================

class RouterDecision(BaseModel):
    """Strukturierte Ausgabe des Routers."""
    relevant_modules: list[str] = Field(
        description="Liste der relevanten Modul-IDs (z.B. ['awx', 'jny', 'inu'])"
    )
    reasoning: str = Field(
        description="Kurze Begründung für die Auswahl"
    )


def router_agent(state: BeatrixState) -> dict:
    """
    Router-Agent: Entscheidet welche Module für die Query relevant sind.
    """
    llm = get_llm()

    # Erstelle Modul-Übersicht für den Router
    module_overview = "\n".join([
        f"- {mod_id}: {desc}"
        for mod_id, desc in MODULE_DESCRIPTIONS.items()
    ])

    system_prompt = f"""Du bist der Router für das BEATRIX Behavioral Change Model 2.0.

Deine Aufgabe: Entscheide welche Module für eine Benutzer-Anfrage relevant sind.

Verfügbare Module:
{module_overview}

Regeln:
1. Wähle 1-4 Module die am relevantesten sind
2. Wähle weniger Module für spezifische Fragen
3. Wähle mehr Module für komplexe/übergreifende Fragen
4. "meta" nur bei Fragen zur Systemarchitektur

Antworte im JSON-Format:
{{"relevant_modules": ["modul1", "modul2"], "reasoning": "Begründung"}}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Benutzer-Anfrage: {state['query']}")
    ]

    # Mit strukturierter Ausgabe
    structured_llm = llm.with_structured_output(RouterDecision)
    result = structured_llm.invoke(messages)

    print(f"\n🔀 Router-Entscheidung: {result.relevant_modules}")
    print(f"   Begründung: {result.reasoning}\n")

    return {"relevant_modules": result.relevant_modules}


# =============================================================================
# MODUL-AGENTEN
# =============================================================================

def create_module_agent(module_id: str):
    """Factory-Funktion: Erstellt einen spezialisierten Agenten für ein Modul."""

    def module_agent(state: BeatrixState) -> dict:
        """Spezialisierter Agent für ein BCM-Modul."""

        # Prüfe ob dieses Modul relevant ist
        if module_id not in state.get("relevant_modules", []):
            return {"module_responses": []}

        print(f"🤖 {module_id.upper()}-Agent arbeitet...")

        # Lade Modul-Daten
        module_data = load_module(module_id)
        module_context = format_module_context(module_id, module_data)

        llm = get_llm()

        system_prompt = f"""Du bist ein Experte für das BCM 2.0 Modul "{module_id.upper()}".

Modul-Kontext:
{module_context}

Deine Aufgabe:
1. Beantworte die Frage NUR aus Perspektive dieses Moduls
2. Beziehe dich auf relevante Axiome
3. Sei präzise und fachlich korrekt
4. Antworte auf Deutsch

Modul-Beschreibung: {MODULE_DESCRIPTIONS[module_id]}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Frage: {state['query']}")
        ]

        response = llm.invoke(messages)

        # Erstelle strukturierte Antwort
        agent_response: AgentResponse = {
            "module": module_id,
            "response": response.content,
            "relevant_axioms": [ax.get("id", "") for ax in extract_axioms(module_data, 3)]
        }

        return {"module_responses": [agent_response]}

    return module_agent


# =============================================================================
# SYNTHESIZER AGENT
# =============================================================================

def synthesizer_agent(state: BeatrixState) -> dict:
    """
    Synthesizer: Kombiniert alle Modul-Antworten zu einer kohärenten Antwort.
    """
    print("\n🔄 Synthesizer kombiniert Antworten...")

    module_responses = state.get("module_responses", [])

    if not module_responses:
        return {"final_response": "Keine relevanten Module gefunden."}

    # Formatiere Modul-Antworten
    responses_text = "\n\n".join([
        f"=== {resp['module'].upper()} ===\n{resp['response']}"
        for resp in module_responses
    ])

    llm = get_llm()

    system_prompt = """Du bist der Synthesizer für das BEATRIX Behavioral Change Model 2.0.

Deine Aufgabe:
1. Kombiniere die Antworten der Modul-Experten zu einer kohärenten Gesamtantwort
2. Zeige Zusammenhänge zwischen den Modulen auf
3. Strukturiere die Antwort klar und verständlich
4. Antworte auf Deutsch
5. Verwende Markdown für bessere Lesbarkeit

Wichtig: Integriere die verschiedenen Perspektiven, wiederhole nicht einfach."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""Ursprüngliche Frage: {state['query']}

Modul-Antworten:
{responses_text}

Erstelle eine integrierte Antwort:""")
    ]

    response = llm.invoke(messages)

    return {"final_response": response.content}


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def build_beatrix_graph() -> StateGraph:
    """Baut den LangGraph für das BEATRIX Multi-Agent-System."""

    # Erstelle Graph
    graph = StateGraph(BeatrixState)

    # Füge Router hinzu
    graph.add_node("router", router_agent)

    # Füge Modul-Agenten hinzu
    for module_id in MODULE_MAP.keys():
        graph.add_node(f"agent_{module_id}", create_module_agent(module_id))

    # Füge Synthesizer hinzu
    graph.add_node("synthesizer", synthesizer_agent)

    # Verbindungen: START → Router
    graph.add_edge(START, "router")

    # Router → Alle Modul-Agenten (parallel)
    for module_id in MODULE_MAP.keys():
        graph.add_edge("router", f"agent_{module_id}")

    # Alle Modul-Agenten → Synthesizer
    for module_id in MODULE_MAP.keys():
        graph.add_edge(f"agent_{module_id}", "synthesizer")

    # Synthesizer → END
    graph.add_edge("synthesizer", END)

    return graph.compile()


# =============================================================================
# MAIN / USAGE
# =============================================================================

class BeatrixMultiAgent:
    """Hauptklasse für das BEATRIX Multi-Agent-System."""

    def __init__(self):
        self.graph = build_beatrix_graph()

    def query(self, question: str) -> str:
        """Stellt eine Frage an das Multi-Agent-System."""
        print(f"\n{'='*60}")
        print(f"📝 Frage: {question}")
        print('='*60)

        # Initialer State
        initial_state: BeatrixState = {
            "query": question,
            "relevant_modules": [],
            "module_responses": [],
            "final_response": ""
        }

        # Graph ausführen
        result = self.graph.invoke(initial_state)

        print(f"\n{'='*60}")
        print("✅ FINALE ANTWORT:")
        print('='*60)
        print(result["final_response"])

        return result["final_response"]


def main():
    """Beispiel-Verwendung des BEATRIX Multi-Agent-Systems."""

    # Initialisiere System
    beatrix = BeatrixMultiAgent()

    # Beispiel-Fragen
    example_queries = [
        "Wie beeinflusst Awareness die Verhaltensänderung?",
        "Was sind die 5 Phasen der Behavioral Change Journey?",
        "Wie funktioniert die Segmentierung von Zielgruppen im BCM?",
        "Welche Rolle spielt der individuelle Nutzen bei Entscheidungen?",
    ]

    print("\n" + "="*60)
    print("🚀 BEATRIX Multi-Agent-System")
    print("="*60)
    print("\nVerfügbare Module:")
    for mod_id, desc in MODULE_DESCRIPTIONS.items():
        print(f"  • {mod_id}: {desc[:50]}...")

    print("\n" + "-"*60)
    print("Beispiel-Fragen:")
    for i, q in enumerate(example_queries, 1):
        print(f"  {i}. {q}")
    print("-"*60)

    # Interaktiver Modus
    while True:
        print("\n")
        user_input = input("Deine Frage (oder 'q' zum Beenden): ").strip()

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Auf Wiedersehen! 👋")
            break

        if user_input:
            beatrix.query(user_input)


if __name__ == "__main__":
    main()
