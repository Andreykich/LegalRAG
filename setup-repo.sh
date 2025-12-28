#!/bin/bash
# Setup script for LegalRAG repository
# This script initializes the complete project structure

set -e

echo "🚀 Initializing LegalRAG Repository..."

# Create directory structure
mkdir -p legalrag/{src,api,data/{raw,processed,indices},configs,notebooks,tests,scripts,reports,docs,presentation}

cd legalrag

# Create src/__init__.py
touch src/__init__.py

# Create api/__init__.py
touch api/__init__.py

# Create tests/__init__.py
touch tests/__init__.py

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Models and large files
*.bin
*.model
*.pt
*.pth
*.ckpt
data/raw/*.json
data/processed/*.jsonl
data/indices/*.bin
*.pkl

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/
EOF

echo "✅ Repository structure created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Copy all Python files from the provided code into their respective directories"
echo "2. Run: pip install -r requirements.txt"
echo "3. Run: python scripts/generate_synthetic_data.py"
echo "4. Run: python scripts/build_index.py"
echo "5. Run: pytest tests/ -v"
echo "6. Run: python scripts/run_server.py"
echo ""
echo "For detailed instructions, see README.md"
