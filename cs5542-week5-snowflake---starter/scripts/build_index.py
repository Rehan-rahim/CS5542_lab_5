import faiss
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import random
import torch
import os
from scripts.config import config

def build_index():
    # Set explicit seeds for reproducibility
    seed = config.get("random_seed", 42)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    input_file = config["indexing"]["input_file"]
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Missing input file: {input_file}. Run preprocess_text.py first.")
        
    df = pd.read_csv(input_file)

    model_name = config["indexing"]["model_name"]
    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        df["text"].tolist(),
        show_progress_bar=True
    )

    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]
    
    index_type = config["indexing"].get("index_type", "IndexFlatL2")
    
    if index_type == "IndexIVFFlat":
        # Integrating efficient index from Faiss reproducibility lessons
        nlist = config["indexing"].get("nlist", 100)
        # We need a quantizer for IVFFlat
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)
        # Train before adding
        index.train(embeddings)
        index.add(embeddings)
    else:
        # Default exact nearest neighbor
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

    out_index_path = config["indexing"]["output_index"]
    out_meta_path = config["indexing"]["output_metadata"]
    
    os.makedirs(os.path.dirname(out_index_path), exist_ok=True)

    faiss.write_index(index, out_index_path)

    with open(out_meta_path, "wb") as f:
        pickle.dump(df.to_dict("records"), f)

    print(f"Index ({index_type}) built successfully with {index.ntotal} vectors.")

if __name__ == "__main__":
    build_index()