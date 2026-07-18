# PII Redaction Tool for DOCX

This project implements a **hybrid PII redaction pipeline** for `.docx` documents using:
1. **Rule-based regex + context heuristics** (for high-precision structured PII like Email/Phone, and block patterns like Address/Company), and  
2. **Detector-assisted extraction** (via a hybrid detector) for candidate entities before replacement.

The system redacts:
- **NAME**
- **EMAIL**
- **PHONE**
- **COMPANY**
- **ADDRESS**

## Approach
I used a **hybrid strategy** instead of pure NER:
- **Company detection**: suffix-based legal entity matching (e.g., Limited, Securities, Bank, etc.).
- **Address detection**: contiguous block detection using location/address keywords and PIN-code patterns, with stop-line logic (Telephone/Email/Website/SEBI/etc.).
- **Email/Phone detection**: context-anchored line-level filtering + detector extraction.
- **Name detection**: conservative capitalized multi-token pattern, plus explicit handling for `Contact Person:` lines.
- **Replacement strategy**:
  - Name/Email/Phone → existing faker/mapper pipeline.
  - Company/Address → deterministic, template-based fake mapping to avoid unstable/random outputs and preserve document readability.

## Why this approach
A pure NER approach performed inconsistently on long financial/legal DOCX with mixed formatting, tables, and broken line wraps.  
A rule + detector hybrid gave better control over precision and document-structure preservation.

## Key Tradeoffs
- **Pros**
  - Strong recall on structured fields (Phone/Email).
  - More stable outputs for Company/Address after deterministic mapping.
  - Works across body, tables, headers, and footers.
- **Cons**
  - Rule-based name/address/company logic can miss uncommon formats.
  - Table-heavy documents can still produce boundary errors.
  - Conservative name filtering reduces false positives but can increase false negatives.

## Observed Failure Modes
1. **Name misses in complex tables**  
   Some shareholder/person names in unusual table formatting were not redacted initially.
2. **Address under-detection in long unbroken lines**  
   Single-line mixed company+address strings can evade clean block segmentation.
3. **Company false positives / over-matches**  
   Legal suffix keywords can occasionally match non-company phrases.
4. **Residual artifacts in redacted text**  
   Proxy evaluation shows some FP where detector catches new synthetic strings post-redaction.

## Input / Output Artifacts

The data foler contains complete input and output artifacts for evaluation.

- **Input 
  - Original DOCX document containing real PII.

- **Predictions File

- **Redacted Output (`data/output/redacted.docx`)**
  - Final document with all detected PII replaced by deterministic synthetic values while preserving the original document layout and formatting.

## Deployment
A Streamlit app is used for upload → redact → download workflow and is deployable on Streamlit Community Cloud.
