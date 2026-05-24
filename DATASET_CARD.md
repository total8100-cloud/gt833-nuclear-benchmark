# Dataset Card: GT-833 Nuclear Regulatory Benchmark

## Dataset Summary

GT-833 is an expert-validated reference annotation benchmark for nuclear regulatory constraint extraction. It covers the complete five-level U.S./international nuclear digital I&C regulatory hierarchy (10 CFR → NRC RG → IEEE/ANSI → IEC → EPRI), annotated using a structured 7-tuple constraint schema.

## Languages

English (regulatory documents)

## Data Fields

Each requirement entry contains:

```json
{
  "id": "GT-001",
  "text": "The system shall respond within 100 milliseconds.",
  "requirement_type": "mandatory",
  "source": "IEEE 7-4.3.2",
  "hierarchy_level": 2,
  "hierarchy_level_name": "Industry Standard (IEEE / ANSI)",
  "parent_regulation": "RG 1.152",
  "top_regulation": "10 CFR 50.55a",
  "difficulty": "easy",
  "constraints": [
    {
      "constraint_type": "temporal",
      "variable": "response_time",
      "operator": "<=",
      "value": 100,
      "unit": "milliseconds",
      "direction": "minimize",
      "confidence": 0.95
    }
  ]
}
```

## Source Distribution

| Level | Source | Items | Access |
|-------|--------|-------|--------|
| 0 | 10 CFR (federal regulations) | 21 | Public |
| 1 | NRC Regulatory Guides | 204 | Public |
| 2 | IEEE/ANSI Standards | 514 | On request |
| 2 | IEC International Standards | 73 | On request |
| 3 | EPRI Industry Guidance | 21 | On request |
| **Total** | | **833** | |

## Annotation Protocol

Two-stage expert-adjudicated annotation protocol:

1. **Stage 1 (LLM-assisted)**: Llama-3.3-70B generates candidate 7-tuple annotations
2. **Stage 2 (Expert adjudication)**: Nuclear software V&V practitioner with KEPCO E&C regulatory review experience reviews every annotation

## Copyright Notice

IEEE, IEC, and EPRI documents are copyrighted. This dataset provides:
- Researcher-generated **paraphrases** (not verbatim text) for copyrighted sources
- Full text for NRC public-domain documents only
- Source identifiers (e.g., `"source": "IEEE 7-4.3.2"`) for traceability

## Data Access

See [README.md](README.md) for the tiered access policy and request procedure.

## Citation

```bibtex
@article{lim2026gt833neusys,
  title   = {{GT-833} and {NeuSys}: An Auditable Neuro-Symbolic Framework
             for Nuclear Regulatory Constraint Extraction and Consistency Checking},
  author  = {Lim, Gyu-Hyun and Jung, Yuchul},
  journal = {Reliability Engineering and System Safety},
  year    = {2026},
  note    = {Under review}
}
```
