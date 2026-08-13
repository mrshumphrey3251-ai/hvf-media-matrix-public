#!/bin/bash
echo "=== HVF FEDERAL GRANT AUDIT & VERIFICATION ==="
echo "Firmographics Check:"
if [ -f ".hvf_firmographics" ]; then
    cat .hvf_firmographics
    echo "[PASS] Federal CAGE Code locked locally."
else
    echo "[FAIL] Missing firmographics file!"
fi

echo ""
echo "NSF Project Pitch Document Check:"
if [ -f "NSF_SBIR_Project_Pitch_Final.md" ]; then
    echo "[PASS] NSF_SBIR_Project_Pitch_Final.md exists."
    echo "Total Line Count: $(wc -l < NSF_SBIR_Project_Pitch_Final.md)"
    echo "Total Word Count: $(wc -w < NSF_SBIR_Project_Pitch_Final.md)"
else
    echo "[FAIL] NSF Pitch Document missing!"
fi
echo "============================================="
