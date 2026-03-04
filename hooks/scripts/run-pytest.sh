#!/usr/bin/env bash

cd "$(git rev-parse --show-toplevel)"

echo "🧪 Running pytest..."
pytest
pytest_exit=$?

if [ $pytest_exit != 0 ]; then
    echo "❌ Tests failed. Fix them before committing."
else
    echo "✅ All tests passed!"
fi

exit $pytest_exit
