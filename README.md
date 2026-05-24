# GT-833 and NeuSys: Nuclear Regulatory Constraint Extraction Benchmark

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Paper](https://img.shields.io/badge/Paper-RESS_2026-blue)](https://doi.org/XXXX)

Official repository for:

> **GT-833 and NeuSys: An Auditable Neuro-Symbolic Framework for Nuclear Regulatory Constraint Extraction and Consistency Checking**  
> Gyu-Hyun Lim, Yuchul Jung  
> *Reliability Engineering and System Safety* (2026, under review)

---

## Overview

This repository provides:

| Resource | Description | Access |
|----------|-------------|--------|
| `data/public/gt833_nrc_public_v3.json` | 225 NRC public-domain annotations | Public |
| `data/schema/annotation_schema_v3.json` | Full 7-tuple annotation schema | Public |
| `evaluation/` | Benchmark evaluation scripts | Public |
| Full GT-833 (833 items incl. IEEE/IEC/EPRI) | Complete benchmark | On request |

---

## GT-833 Benchmark

GT-833 is an expert-validated reference annotation benchmark for nuclear regulatory constraint extraction comprising **833 requirements** from 24 regulatory sources across a five-standard-body regulatory hierarchy:

```
Level 0: 10 CFR Federal Regulations         (21 items)
Level 1: NRC Regulatory Guides              (204 items)
Level 2: IEEE/ANSI & IEC Standards          (587 items)  ← copyrighted
Level 3: EPRI Industry Guidance             (21 items)   ← copyrighted
```

Each requirement is annotated with a **7-tuple constraint**:
`(type, variable, operator, value, unit, direction, confidence)`

### Statistics

| Metric | Value |
|--------|-------|
| Total requirements | 833 |
| Boolean constraints | 97.4% |
| Numeric constraints | 1.7% |
| Temporal constraints | 0.9% |
| Regulatory sources | 24 |

---

## Data Access Policy

### Public Release (this repo)
- **NRC ADAMS subset** (225 items): NRC Regulatory Guides and 10 CFR — public domain, full text included
- **Annotation schema**: 7-tuple structure documentation
- **Evaluation code**: Scripts for reproducing benchmark results

### On Academic Request
- **Full GT-833** (833 items): IEEE/IEC/EPRI-sourced annotations
  - Paraphrased requirement text (copyright-compliant)
  - Full 7-tuple annotations and evaluation labels

To request the full dataset, open a GitHub Issue with:
1. Your institutional affiliation
2. Intended use (research / teaching / evaluation)
3. Confirmation that you hold relevant IEEE/IEC standard access

We aim to respond within 5 business days.

---

## Quick Start

```bash
git clone https://github.com/limgyuhyun/gt833-nuclear-benchmark
cd gt833-nuclear-benchmark
pip install -r requirements.txt

# Run evaluation on public subset
python evaluation/evaluate.py --data data/public/gt833_nrc_public_v3.json
```

---

## NeuSys Pipeline

NeuSys is a three-stage Neuro-Symbolic pipeline for auditable constraint extraction:

```
Stage 0 (optional): RAG retrieval (NeuSys-RAG variant)
Stage 1: Candidate Constraint Generation (few-shot LLM)
Stage 2: Hallucination Guard (CRITICAL-only blocking)
Stage 3: Scoped SMT Consistency Checking (Z3)
```

Key safety properties:
- **FTR = 0.000%**: No expert-valid constraints rejected by guard
- **GEC = 100%**: Every admitted constraint carries audit trail
- **Statistically equivalent F1** to neural-only LLM Few-Shot baseline

---

## Citation

```bibtex
@article{lim2026gt833neusys,
  title   = {{GT-833} and {NeuSys}: An Auditable Neuro-Symbolic Framework
             for Nuclear Regulatory Constraint Extraction and
             Consistency Checking},
  author  = {Lim, Gyu-Hyun and Jung, Yuchul},
  journal = {Reliability Engineering and System Safety},
  year    = {2026},
  note    = {Under review}
}
```

---

## License

- **Annotation data and evaluation code**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **NRC source documents**: U.S. Government public domain
- **IEEE/IEC/EPRI references**: Cited by identifier only; original texts not redistributed

---

## Contact

Gyu-Hyun Lim · Kumoh National Institute of Technology  
total8100@kumoh.ac.kr
