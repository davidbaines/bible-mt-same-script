# v1 reference scores (superseded)

These are the complete score tables and results documents from the series'
first run (22 H100 runs, completed 2026-07-25) — kept for comparison, **not
valid as reported results**. A code review
(`bible-mt-family-transfer-v1/experiments/code-review-findings.md`) confirmed
three defects live during every v1 run:

1. **Checkpoint selection used test verses.** The early-stopping set was
   sampled from the test pairs (~21% overlap for gap-filling test sets), so
   every headline score carries optimistic bias — gap-filling most.
2. **Test sets silently shrank to the source translation's coverage.**
   "Whole OT" drafting scores cover only source-covered verses (Ethiopic
   especially).
3. **`<range>` markers passed through as source text.** tel2017 (100 cells),
   gmve (198) and gofe (127) are affected: Telugu and Ethiopic baselines are
   slightly deflated, so those fusion gains are slightly inflated.

v2 re-runs all 22 runs on the fixed `synoptic` toolkit with a validation set
disjoint from both training and test material. Compare v2 numbers against
these to quantify what the defects were worth.
