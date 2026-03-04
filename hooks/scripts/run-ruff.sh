#!/usr/bin/env bash

cd "$(git rev-parse --show-toplevel)"

echo "🔍 Running Ruff..."
ruff check .
ruff_exit=$?

if [ $ruff_exit != 0 ]; then
    echo "❌ Ruff found issues. Fix linting before committing."
else
    echo "✅ Ruff is happy!"
fi

exit $ruff_exit
