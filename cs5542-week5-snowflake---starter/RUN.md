# Lab 5: Reproducibility Run Guide

## Single Command Execution

To execute the entire reproducible pipeline (Part A & Part B), simply run:

```bash
bash reproduce.sh
```

### What `reproduce.sh` does:
1. **Creates Required Directories:** Generates `artifacts/` and `logs/` folders if they do not exist.
2. **Smoke Tests:** Runs a suite of `pytest` assertions located in `tests/test_smoke.py` to ensure the environment matches the pinned configuration and that configurations load successfully.
3. **Data Preprocessing:** Runs `scripts/preprocess_text.py`, seeding randomness from `config.yaml` and writing parsed textual dataset chunks to `artifacts/processed_text.csv`.
4. **Index Building:** Runs `scripts/build_index.py`, taking configurations from `config.yaml` (including the exact random seed, AI model name, and Index type—which defaults to the faster `IndexIVFFlat`) to build a vector database and save it to `artifacts/index.faiss`.
5. **Faiss Reproducibility Benchmark:** Runs `faiss_benchmark_repro.py` to print a live terminal comparison of Faiss exact vs approximate search speeds and recall metrics.

---

### Dashboard

After running the pipeline, launch the main web application to interact with your data:

```bash
streamlit run app/streamlit_app.py
```
