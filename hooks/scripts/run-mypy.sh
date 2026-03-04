#!/usr/bin/env bash

cd "$(git rev-parse --show-toplevel)"

if ! find . -name "*.py" -not -path "./.venv/*" | grep -q .; then
    echo "🔬 No Python files found, skipping mypy."
    exit 0
fi

echo "🔬 Running mypy..."
mypy .
mypy_exit=$?

if [ $mypy_exit != 0 ]; then
    echo "❌ mypy found type errors. Fix them before committing."
else
    echo "✅ Types check out!"
fi

exit $mypy_exit
