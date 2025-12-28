#!/bin/bash
# LegalRAG Quick Setup and GitHub Upload Script
# This script automates the entire setup process
# Usage: bash quick-setup.sh

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║        🚀 LegalRAG: Rapid Setup & GitHub Upload Script            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# STEP 1: Check Prerequisites
# ============================================================================

echo -e "${BLUE}[STEP 1]${NC} Checking prerequisites..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git is not installed${NC}"
    echo "Install Git from https://git-scm.com/"
    exit 1
fi
echo -e "${GREEN}✓ Git found: $(git --version)${NC}"

echo ""

# ============================================================================
# STEP 2: Create Project Structure
# ============================================================================

echo -e "${BLUE}[STEP 2]${NC} Creating project structure..."

DIRS=(
    "src"
    "api"
    "data/raw"
    "data/processed"
    "data/indices"
    "configs"
    "notebooks"
    "tests"
    "scripts"
    "reports"
    "docs"
    "presentation"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo -e "${GREEN}✓ Created: $dir${NC}"
done

echo ""

# ============================================================================
# STEP 3: Create __init__.py files
# ============================================================================

echo -e "${BLUE}[STEP 3]${NC} Creating Python package files..."

touch src/__init__.py
echo -e "${GREEN}✓ Created: src/__init__.py${NC}"

touch api/__init__.py
echo -e "${GREEN}✓ Created: api/__init__.py${NC}"

touch tests/__init__.py
echo -e "${GREEN}✓ Created: tests/__init__.py${NC}"

echo ""

# ============================================================================
# STEP 4: Create Virtual Environment
# ============================================================================

echo -e "${BLUE}[STEP 4]${NC} Creating virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}✗ Could not activate virtual environment${NC}"
    exit 1
fi

echo ""

# ============================================================================
# STEP 5: Install Dependencies
# ============================================================================

echo -e "${BLUE}[STEP 5]${NC} Installing dependencies..."

if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt not found${NC}"
    echo "Creating minimal requirements.txt..."
    cat > requirements.txt << 'EOF'
torch==2.0.1
transformers==4.35.0
sentence-transformers==2.2.2
faiss-cpu==1.7.4
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pyyaml==6.0.1
numpy==1.24.3
pytest==7.4.3
EOF
    pip install -r requirements.txt
    echo -e "${GREEN}✓ requirements.txt created and dependencies installed${NC}"
fi

echo ""

# ============================================================================
# STEP 6: GitHub Setup (Interactive)
# ============================================================================

echo -e "${BLUE}[STEP 6]${NC} GitHub Configuration..."
echo ""

read -p "Do you want to push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    
    echo ""
    echo -e "${YELLOW}Follow these steps:${NC}"
    echo "1. Create a new repository on GitHub: https://github.com/new"
    echo "   - Name: legalrag"
    echo "   - Description: RAG-based legal document assistant"
    echo "   - Public/Private: Your choice"
    echo "   - DO NOT add README, .gitignore, or license (you already have them)"
    echo ""
    
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    read -p "Enter your repository name (default: legalrag): " GITHUB_REPO
    GITHUB_REPO=${GITHUB_REPO:-legalrag}
    
    GITHUB_URL="https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git"
    
    echo ""
    echo -e "${BLUE}Initializing Git repository...${NC}"
    
    # Initialize Git
    git init
    git config user.name "Your Name"
    git config user.email "your.email@example.com"
    
    echo -e "${GREEN}✓ Git repository initialized${NC}"
    
    # Add all files
    echo -e "${BLUE}Adding files...${NC}"
    git add .
    echo -e "${GREEN}✓ Files staged${NC}"
    
    # Create initial commit
    echo -e "${BLUE}Creating commit...${NC}"
    git commit -m "Initial commit: Complete LegalRAG project with RAG pipeline, API, tests, and documentation"
    echo -e "${GREEN}✓ Commit created${NC}"
    
    # Add remote
    echo -e "${BLUE}Configuring remote...${NC}"
    git remote add origin "$GITHUB_URL"
    echo -e "${GREEN}✓ Remote configured: $GITHUB_URL${NC}"
    
    # Push to GitHub
    echo ""
    echo -e "${YELLOW}Ready to push to GitHub!${NC}"
    echo "When prompted, authenticate with your GitHub credentials."
    echo ""
    
    read -p "Press Enter to push to GitHub (or Ctrl+C to cancel): " -r
    
    git branch -M main
    git push -u origin main
    
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
    echo -e "${BLUE}Repository: $GITHUB_URL${NC}"
    
else
    echo -e "${YELLOW}⚠ Skipping GitHub setup${NC}"
fi

echo ""

# ============================================================================
# STEP 7: Quick Test
# ============================================================================

echo -e "${BLUE}[STEP 7]${NC} Running quick tests..."

if command -v pytest &> /dev/null; then
    if [ -d "tests" ] && [ -f "tests/__init__.py" ]; then
        echo "Tests directory exists but test files not yet created."
        echo "You can run: pytest tests/ -v (once test files are created)"
    fi
fi

echo ""

# ============================================================================
# FINAL SUMMARY
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE!                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}What's been done:${NC}"
echo "  ✓ Project structure created"
echo "  ✓ Python packages initialized"
echo "  ✓ Virtual environment set up"
echo "  ✓ Dependencies installed"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  ✓ Pushed to GitHub"
fi
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Copy all source code files from the report into:"
echo "   - src/       (config.py, data_loader.py, etc.)"
echo "   - api/       (app.py, models.py, startup.py)"
echo "   - scripts/   (build_index.py, evaluate.py, etc.)"
echo "   - tests/     (test_*.py files)"
echo "   - docs/      (ARCHITECTURE.md, etc.)"
echo ""
echo "2. Generate synthetic data:"
echo "   python scripts/generate_synthetic_data.py"
echo ""
echo "3. Build the index:"
echo "   python scripts/build_index.py"
echo ""
echo "4. Run tests:"
echo "   pytest tests/ -v"
echo ""
echo "5. Start the API server:"
echo "   python scripts/run_server.py"
echo ""
echo "6. Access the API:"
echo "   http://localhost:8000/docs"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  • README.md - Quick start guide"
echo "  • docs/ARCHITECTURE.md - System architecture"
echo "  • docs/MODEL_CARD.md - Model details"
echo "  • docs/SYSTEM_CARD.md - Risks and limitations"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
