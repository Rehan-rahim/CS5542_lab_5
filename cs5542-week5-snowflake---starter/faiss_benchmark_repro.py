import faiss
import numpy as np
import time

def generate_data(num_vectors, dimension, seed=42):
    np.random.seed(seed)
    # Generate random synthetic vectors
    data = np.random.random((num_vectors, dimension)).astype('float32')
    return data

def benchmark_faiss():
    print("--- Reproducing Faiss Vector Similarity Search Benchmarks ---")
    
    dimension = 128
    num_train = 50000
    num_queries = 1000
    
    print(f"Generating synthetic dataset: {num_train} vectors, dim={dimension}")
    xb = generate_data(num_train, dimension, seed=42)
    xq = generate_data(num_queries, dimension, seed=123)

    print("\n--- Benchmark 1: Exact Search (IndexFlatL2) ---")
    index_flat = faiss.IndexFlatL2(dimension)
    
    t0 = time.time()
    index_flat.add(xb)
    build_time_flat = time.time() - t0
    print(f"Index built. Total vectors: {index_flat.ntotal}")
    print(f"Build time: {build_time_flat:.4f} seconds")
    
    t0 = time.time()
    D_flat, I_flat = index_flat.search(xq, 10) # Search top 10
    search_time_flat = time.time() - t0
    print(f"Search time ({num_queries} queries): {search_time_flat:.4f} seconds")

    print("\n--- Benchmark 2: Approximate Search (IndexIVFFlat) ---")
    nlist = 100 # Number of clusters
    quantizer = faiss.IndexFlatL2(dimension)
    index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)
    
    t0 = time.time()
    index_ivf.train(xb)
    index_ivf.add(xb)
    build_time_ivf = time.time() - t0
    print(f"Index trained & built. Total vectors: {index_ivf.ntotal}")
    print(f"Build time: {build_time_ivf:.4f} seconds (includes k-means clustering)")
    
    index_ivf.nprobe = 10 # Search across 10 nearest clusters
    t0 = time.time()
    D_ivf, I_ivf = index_ivf.search(xq, 10)
    search_time_ivf = time.time() - t0
    print(f"Search time ({num_queries} queries, nprobe={index_ivf.nprobe}): {search_time_ivf:.4f} seconds")

    # Calculate Recall@10
    intersections = 0
    for i in range(num_queries):
        # Count how many of the exact neighbors were returned by IVF
        intersections += len(set(I_flat[i]).intersection(set(I_ivf[i])))
    
    recall = intersections / (num_queries * 10)
    print("\n--- Conclusion & Comparison ---")
    print(f"IVFFlat Search speedup over FlatL2: {search_time_flat/search_time_ivf:.2f}x")
    print(f"IVFFlat Recall@10: {recall:.4f}")

if __name__ == "__main__":
    benchmark_faiss()
