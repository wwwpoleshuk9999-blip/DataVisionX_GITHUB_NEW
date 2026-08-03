#!/bin/bash

echo "🔎 DataVisionX Frontend Link Check"

JS_DIR="web/js"
errors=0

echo
echo "Checking function references..."

grep -RhoE '\b(load[A-Z][A-Za-z0-9_]*|connect[A-Z][A-Za-z0-9_]*|update[A-Z][A-Za-z0-9_]*|add[A-Z][A-Za-z0-9_]*)\(' "$JS_DIR"/*.js \
| sed 's/(//' \
| sort -u > /tmp/dvx_functions.txt

while read -r func; do
    if [ "$func" = "addEventListener" ]; then continue; fi
    if ! grep -R "function $func" "$JS_DIR" >/dev/null; then
        echo "❌ Missing function: $func"
        errors=1
    fi
done < /tmp/dvx_functions.txt

if [ $errors -eq 0 ]; then
    echo
    echo "✅ Frontend links OK"
    exit 0
else
    echo
    echo "❌ Frontend link errors found"
    exit 1
fi
