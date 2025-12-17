"""
BEATRIX Simple Agent - Einfache Version ohne LangGraph
=======================================================

Eine vereinfachte Version für Einsteiger, die zeigt wie man
die BCM-Module als Kontext für einen LLM-Agenten nutzt.

Dieses Beispiel verwendet nur LangChain (ohne LangGraph).
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# KONFIGURATION
# =============================================================================

BASE_PATH = Path(__file__).parent

# Welche Module für welche Themen?
MODULE_TOPICS = {
    "awareness": "awx",
    "bewusstsein": "awx",
    "wahrnehmung": "awx",
    "nutzen": "inu",
    "utility": "inu",
    "entscheidung": "inu",
    "journey": "jny",
    "phase": "jny",
    "verhaltensänderung": "jny",
    "segment": "seg",
    "zielgruppe": "seg",
    "willingness": "wax",
    "bereitschaft": "wax",
    "kontext": "context",
    "intervention": "int",
    "kollektiv": "knu",
    "gruppe": "knu",
    "identität": "idn",
}


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def load_module(module_id: str) -> dict:
    """Lädt ein BCM-Modul."""
    module_paths = {
        "awx": "awx/awx.json",
        "inu": "inu/inu.json",
        "jny": "jny/jny.json",
        "seg": "seg/seg.json",
        "wax": "wax/wax.json",
        "context": "context/context.json",
        "int": "int/int.json",
        "knu": "knu/knu.json",
        "idn": "idn/idn.json",
        "meta": "meta/meta.json",
        "wtx": "wtx/wtx.json",
    }

    path = BASE_PATH / module_paths.get(module_id, f"{module_id}/{module_id}.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_relevant_modules(query: str) -> list[str]:
    """Einfache Keyword-basierte Modul-Erkennung."""
    query_lower = query.lower()
    modules = set()

    for keyword, module in MODULE_TOPICS.items():
        if keyword in query_lower:
            modules.add(module)

    # Default: INU wenn nichts gefunden
    if not modules:
        modules.add("inu")

    return list(modules)


def extract_module_summary(module_data: dict, max_chars: int = 2000) -> str:
    """Extrahiert eine kompakte Zusammenfassung eines Moduls."""
    summary_parts = []

    # Versuche verschiedene Strukturen
    if "metadata" in module_data:
        meta = module_data["metadata"]
        if "context" in meta:
            summary_parts.append(f"Kontext: {meta['context'][:500]}")
        if "objectives" in meta:
            summary_parts.append(f"Ziele: {', '.join(meta['objectives'][:3])}")

    if "A2_Scope" in module_data:
        summary_parts.append(f"Scope: {module_data['A2_Scope'].get('description', '')[:300]}")

    if "A4_Axioms" in module_data:
        axioms = module_data["A4_Axioms"][:5]
        axiom_text = "\n".join([
            f"  - {ax['id']}: {ax['title']} ({ax.get('formula', 'N/A')})"
            for ax in axioms
        ])
        summary_parts.append(f"Axiome:\n{axiom_text}")

    if "A1" in module_data:
        a1 = module_data["A1"]
        if "description" in a1:
            summary_parts.append(f"Beschreibung: {a1['description'][:400]}")

    return "\n\n".join(summary_parts)[:max_chars]


# =============================================================================
# SIMPLE AGENT
# =============================================================================

class BeatrixSimpleAgent:
    """Einfacher BEATRIX-Agent ohne LangGraph."""

    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        """Initialisiert das LLM."""
        provider = os.getenv("LLM_PROVIDER", "openai")

        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.3)
        else:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o", temperature=0.3)

    def query(self, question: str) -> str:
        """Beantwortet eine Frage mit BCM-Kontext."""

        # 1. Finde relevante Module
        modules = detect_relevant_modules(question)
        print(f"📦 Relevante Module: {modules}")

        # 2. Lade Modul-Kontext
        context_parts = []
        for mod_id in modules:
            try:
                module_data = load_module(mod_id)
                summary = extract_module_summary(module_data)
                context_parts.append(f"=== MODUL: {mod_id.upper()} ===\n{summary}")
            except Exception as e:
                print(f"⚠️  Fehler beim Laden von {mod_id}: {e}")

        context = "\n\n".join(context_parts)

        # 3. Erstelle Prompt
        system_prompt = f"""Du bist ein Experte für das Behavioral Change Model (BCM) 2.0 von FehrAdvice.

BCM-Kontext:
{context}

Regeln:
1. Beantworte Fragen basierend auf dem BCM-Kontext
2. Beziehe dich auf relevante Axiome und Konzepte
3. Antworte auf Deutsch
4. Sei präzise und fachlich korrekt
"""

        # 4. LLM aufrufen
        from langchain_core.messages import SystemMessage, HumanMessage

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]

        response = self.llm.invoke(messages)
        return response.content


# =============================================================================
# NOCH EINFACHER: Ohne LangChain (nur OpenAI SDK)
# =============================================================================

def query_with_openai_sdk(question: str) -> str:
    """
    Minimalbeispiel: Nur OpenAI SDK, kein LangChain.
    Zeigt das Grundprinzip.
    """
    from openai import OpenAI

    client = OpenAI()  # Verwendet OPENAI_API_KEY aus Umgebung

    # Lade ein Modul als Kontext
    modules = detect_relevant_modules(question)
    module_data = load_module(modules[0])
    context = extract_module_summary(module_data, max_chars=3000)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"Du bist ein BCM 2.0 Experte.\n\nKontext:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "="*50)
    print("🧠 BEATRIX Simple Agent")
    print("="*50)

    agent = BeatrixSimpleAgent()

    # Beispiel-Fragen
    examples = [
        "Was sind die Phasen der Behavioral Change Journey?",
        "Wie funktioniert Awareness im BCM?",
        "Was ist der individuelle Nutzen?",
    ]

    print("\nBeispiel-Fragen:")
    for i, q in enumerate(examples, 1):
        print(f"  {i}. {q}")

    while True:
        print("\n")
        question = input("Deine Frage (q = beenden): ").strip()

        if question.lower() in ['q', 'quit', 'exit']:
            break

        if question:
            print("\n🤔 Denke nach...\n")
            answer = agent.query(question)
            print("-"*50)
            print(answer)
            print("-"*50)


if __name__ == "__main__":
    main()
