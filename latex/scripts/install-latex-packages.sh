#!/bin/bash
# =============================================================================
# LaTeX Package Installation Script
# =============================================================================
# This script installs the LaTeX packages required for building the ESL paper
# and other documents in this repository.
#
# Usage:
#   ./install-latex-packages.sh
#
# Supported systems:
#   - Debian/Ubuntu (apt)
#   - RHEL/CentOS/Fedora (dnf/yum)
#   - macOS (Homebrew)
#   - Arch Linux (pacman)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect the operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/redhat-release ]; then
        echo "redhat"
    elif [ -f /etc/arch-release ]; then
        echo "arch"
    else
        echo "unknown"
    fi
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install LaTeX on Debian/Ubuntu
install_debian() {
    echo_info "Detected Debian/Ubuntu system"
    echo_info "Installing TeX Live packages..."

    sudo apt-get update
    sudo apt-get install -y \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-science \
        texlive-bibtex-extra \
        biber \
        latexmk

    echo_info "LaTeX installation complete!"
}

# Install LaTeX on RHEL/CentOS/Fedora
install_redhat() {
    echo_info "Detected RHEL/CentOS/Fedora system"
    echo_info "Installing TeX Live packages..."

    if command_exists dnf; then
        sudo dnf install -y \
            texlive-scheme-medium \
            texlive-collection-latexextra \
            texlive-collection-fontsrecommended \
            texlive-collection-science \
            latexmk
    else
        sudo yum install -y \
            texlive \
            texlive-latex \
            texlive-collection-latexrecommended \
            latexmk
    fi

    echo_info "LaTeX installation complete!"
}

# Install LaTeX on macOS
install_macos() {
    echo_info "Detected macOS system"

    if ! command_exists brew; then
        echo_error "Homebrew is not installed. Please install it first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi

    echo_info "Installing MacTeX via Homebrew..."
    brew install --cask mactex-no-gui

    # Update PATH for current session
    eval "$(/usr/libexec/path_helper)"

    echo_info "LaTeX installation complete!"
    echo_warn "You may need to restart your terminal or run: eval \"\$(/usr/libexec/path_helper)\""
}

# Install LaTeX on Arch Linux
install_arch() {
    echo_info "Detected Arch Linux system"
    echo_info "Installing TeX Live packages..."

    sudo pacman -Sy --noconfirm \
        texlive-core \
        texlive-latexextra \
        texlive-fontsextra \
        texlive-science \
        texlive-bibtexextra \
        biber

    echo_info "LaTeX installation complete!"
}

# Install individual CTAN packages via tlmgr (if needed)
install_ctan_packages() {
    echo_info "Checking for specific CTAN packages..."

    if command_exists tlmgr; then
        # These are the packages used in ESL_Paper_v12.tex
        PACKAGES=(
            "amsmath"
            "amssymb"
            "amsthm"
            "graphicx"
            "booktabs"
            "longtable"
            "array"
            "multirow"
            "xcolor"
            "tcolorbox"
            "enumitem"
            "hyperref"
            "geometry"
            "natbib"
            "caption"
            "float"
        )

        echo_info "Installing CTAN packages: ${PACKAGES[*]}"

        for pkg in "${PACKAGES[@]}"; do
            tlmgr install "$pkg" 2>/dev/null || echo_warn "Package $pkg may already be installed or unavailable"
        done

        echo_info "CTAN package installation complete!"
    else
        echo_warn "tlmgr not found. Skipping individual package installation."
        echo_warn "If packages are missing, install them manually with: tlmgr install <package>"
    fi
}

# Verify the installation
verify_installation() {
    echo_info "Verifying LaTeX installation..."

    if command_exists pdflatex; then
        echo_info "pdflatex: $(pdflatex --version | head -1)"
    else
        echo_error "pdflatex not found!"
        return 1
    fi

    if command_exists latexmk; then
        echo_info "latexmk: $(latexmk --version | head -1)"
    else
        echo_warn "latexmk not found (optional but recommended)"
    fi

    if command_exists biber; then
        echo_info "biber: $(biber --version | head -1)"
    else
        echo_warn "biber not found (needed for some bibliography styles)"
    fi

    echo_info "Installation verification complete!"
}

# Main function
main() {
    echo "=============================================="
    echo "  LaTeX Package Installation Script"
    echo "=============================================="
    echo ""

    OS=$(detect_os)

    case $OS in
        debian)
            install_debian
            ;;
        redhat)
            install_redhat
            ;;
        macos)
            install_macos
            ;;
        arch)
            install_arch
            ;;
        *)
            echo_error "Unsupported operating system: $OSTYPE"
            echo_info "Please install TeX Live manually from: https://www.tug.org/texlive/"
            exit 1
            ;;
    esac

    # Try to install specific CTAN packages
    install_ctan_packages

    # Verify the installation
    verify_installation

    echo ""
    echo "=============================================="
    echo "  Installation Complete!"
    echo "=============================================="
    echo ""
    echo "You can now build LaTeX documents using:"
    echo "  pdflatex document.tex"
    echo "  latexmk -pdf document.tex"
    echo ""
}

# Run main function
main "$@"
