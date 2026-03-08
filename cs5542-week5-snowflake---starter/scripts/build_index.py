import faiss
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import yaml
MODEL_NAME = "all-MiniLM-L6-v2"

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
    
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)["faiss"]

    print(f"Building IVFPQ Index (nlist={config['nlist']}, m={config['m']}, nbits={config['nbits']})...")
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFPQ(quantizer, dimension, config["nlist"], config["m"], config["nbits"])
    
    print("Training the index on existing data...")
    index.train(embeddings)
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