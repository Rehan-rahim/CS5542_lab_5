#!/bin/bash
# reproduce.sh - Single command reproducibility script for Lab 5

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Reproducibility Pipeline..."

# 1. Ensure directories exist
echo "Creating required directories (artifacts, logs)..."
mkdir -p artifacts
mkdir -p logs

# 2. Run Smoke Tests to ensure core components work before full pipeline
echo "Running smoke tests..."
python -m pytest tests/test_smoke.py -v
if [ $? -ne 0 ]; then
    echo "Smoke tests failed. Aborting."
    exit 1
fi
echo "Smoke tests passed."

# 3. Data Preprocessing (if applicable scripts are present)
echo "Running data preprocessing..."
python scripts/preprocess_text.py

# 4. Build Vector Index
echo "Building Faiss vector index..."
python scripts/build_index.py

# 5. Run Faiss benchmark reproducibility component
echo "Running Faiss Benchmark Reproducibility..."
python faiss_benchmark_repro.py

echo "Pipeline completed successfully. Artifacts and logs generated."
