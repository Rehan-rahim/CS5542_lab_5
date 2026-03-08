# Reproducibility Audit Details (REPRO_AUDIT.md)

## 1. Single Command Execution
- We created `reproduce.sh`, which automatically chains data generation and module verification logic, reducing human error in the pipeline setup process.
- It includes short-circuit execution: if `pytest` fails, the pipeline aborts.

## 2. Pinned Environments
- We executed `pip freeze > requirements.txt` to capture the exact dependency tree used locally. 
- The tests check that these packages are available before proceeding.

## 3. Configuration-Driven Execution
- A master configuration file (`config.yaml`) was introduced to centrally store constants.
- We created `scripts/config.py` to standardize the process of loading configuration into pipeline scripts like `preprocess_text.py` and `build_index.py`.
- This separates code logic from configurations. Changing the FAISS `model_name` or algorithm type no longer requires making source-code modifications.

## 4. Controlled Randomness
- Non-deterministic sources of variance during AI inference and synthetic data generation were removed. 
- We set a reproducible application seed (`random_seed: 42` in `config.yaml`).
- Applied seeds explicitly to Python's built-in `random`, `numpy` (via `np.random.seed()`), and `pytorch` (via `torch.manual_seed()`).

## 5. Artifacts and Logging
- Removed hardcoded local scattered output directories. 
- AI Model Metadata and binary FAISS indexes now export reliably to the `artifacts/` folder.
- Output from pipeline data loading and query latency is piped into a centralized, auto-generated `logs/` folder inside `pipeline_logs.csv`. Streamlit dashboards automatically parse from this config-defined log location.


