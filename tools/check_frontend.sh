#!/bin/bash

echo "🔎 DataVisionX Frontend Check"

ERROR=0

echo ""
echo "Checking JavaScript syntax..."

for file in web/js/*.js
do
    node --check "$file" 2>/dev/null

    if [ $? -ne 0 ]; then
        echo "❌ Syntax error: $file"
        ERROR=1
    fi
done

echo ""

if [ $ERROR -eq 0 ]; then
    echo "✅ Frontend OK"
else
    echo "❌ Frontend errors found"
    exit 1
fi
