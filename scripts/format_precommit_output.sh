#!/bin/bash

# Run pre-commit and capture output
OUTPUT=$(pre-commit run --all-files)

# Color definitions
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Process each line
while IFS= read -r line; do
    if [[ $line == *"Passed"* ]]; then
        echo -e "${GREEN}${line}${NC}"
    elif [[ $line == *"Failed"* ]]; then
        echo -e "${RED}${line}${NC}"
    elif [[ $line == *"Skipped"* ]]; then
        echo -e "${YELLOW}${line}${NC}"
    else
        echo "$line"
    fi
done <<< "$OUTPUT"

# Summary
passed=$(echo "$OUTPUT" | grep -c "Passed")
failed=$(echo "$OUTPUT" | grep -c "Failed")
skipped=$(echo "$OUTPUT" | grep -c "Skipped")

echo -e "\nSummary:"
echo -e "${GREEN}Passed:${NC} $passed hooks"
echo -e "${RED}Failed:${NC} $failed hooks"
echo -e "${YELLOW}Skipped:${NC} $skipped hooks"

