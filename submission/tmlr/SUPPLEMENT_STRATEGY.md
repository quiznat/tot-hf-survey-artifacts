# TMLR Supplement Strategy

## What Is Customary
- TMLR has no strict page limit, and substantial technical details can go into the main PDF appendix.
- Supplementary material is optional; reviewers can use discretion on how much to consult it.
- Customary use of supplement: reproducibility assets, expanded tables, or implementation details that are useful but not required to understand core claims.

## Tradeoffs
- Benefit: can improve reproducibility and reviewer confidence.
- Benefit: keeps the core narrative focused and readable.
- Risk: some reviewers may focus mainly on the main PDF.
- Risk: supplement often carries higher anonymization risk (logs, links, screenshots, metadata).
- Cost: extra packaging and validation effort before each revision.

## Recommended Default for This Survey
- Submit the anonymous main PDF as the primary artifact.
- Include a light supplementary package only if it improves review efficiency without creating anonymization risk.

## Suggested Supplement Contents (Anonymous-Safe)
- Study-selection and extraction schema summary.
- Claim-evidence mapping table in anonymous/redacted form.
- Additional benchmark table rows and methodological notes.
- Build/reproducibility checklist without identity-bearing URLs.

## Items to Exclude from Initial Anonymous Supplement
- Direct profile/leaderboard links tied to identity.
- System screenshots that can de-anonymize authorship.
- Unredacted logs with names, handles, hosts, or organization-specific metadata.

## Final Recommendation
For this survey, submit a strong self-contained anonymous main PDF and add only a minimal anonymous supplement. Put essential evidence in the main paper/appendix; use supplement only for non-essential reproducibility details that are cleanly anonymized.

## References
- TMLR submission guidance: https://www.jmlr.org/tmlr/submissions.html
- TMLR/OpenReview author guide (appendix and submission expectations): https://openreview.net/group?id=TMLR
- TMLR FAQ (appendix/supplement expectations and review practice): https://jmlr.org/tmlr/faq/
