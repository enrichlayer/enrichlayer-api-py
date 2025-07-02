#!/bin/bash
# Quick publish script for enrichlayer-api

set -e

echo "🚀 EnrichLayer API Publishing Script"
echo "===================================="

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Install it with: pip install poetry"
    exit 1
fi

# Run tests
echo "📋 Running tests..."
python -m pytest tests/ -q
echo "✅ Tests passed"

# Run linting
echo "📋 Running linting..."
ruff check . --exclude codegen/
echo "✅ Linting passed"

# Run type checking
echo "📋 Running type checking..."
mypy enrichlayer_client/
echo "✅ Type checking passed"

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf dist/ build/ *.egg-info

# Build package
echo "📦 Building package..."
poetry build
echo "✅ Package built successfully"

# Show what was built
echo ""
echo "📦 Built packages:"
ls -la dist/

echo ""
echo "🎯 Next steps:"
echo "1. Test on TestPyPI first:"
echo "   poetry config repositories.test-pypi https://test.pypi.org/legacy/"
echo "   poetry config pypi-token.test-pypi <your-test-token>"
echo "   poetry publish -r test-pypi"
echo ""
echo "2. Then publish to PyPI:"
echo "   poetry config pypi-token.pypi <your-pypi-token>"
echo "   poetry publish"
echo ""
echo "3. Don't forget to tag the release:"
echo "   git tag -a v0.1.0 -m 'Release version 0.1.0'"
echo "   git push origin v0.1.0"