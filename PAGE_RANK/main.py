from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

EDGES_PATH = ROOT_DIR / "edges.csv" if (ROOT_DIR / "edges.csv").exists() else BASE_DIR / "edges.csv"
NAMES_PATH = BASE_DIR / "names.csv" if (BASE_DIR / "names.csv").exists() else ROOT_DIR / "names.csv"

CHUNK_SIZE = 1_000_000
EPSILON = 1e-6
MAX_ITER = 100
TOP_K = 5

def load_names(file_name):
    return pd.read_csv(file_name)["Name"].tolist()

def build_sparse_transition(file_name, chunk_size):
    out_deg = np.zeros(1, dtype=np.int64)
    from_list = []
    to_list = []
    max_idx = -1

    for chunk in pd.read_csv(
        file_name,
        usecols=["FromNode", "ToNode"],
        dtype=np.uint32,
        chunksize=chunk_size,
    ):
        f = chunk["FromNode"].to_numpy(dtype=np.int64) - 1
        t = chunk["ToNode"].to_numpy(dtype=np.int64) - 1

        needed = int(f.max()) + 1
        if needed > out_deg.size:
            out_deg.resize(needed, refcheck=False)
        out_deg[:needed] += np.bincount(f, minlength=needed)

        from_list.append(f)
        to_list.append(t)
        max_idx = max(max_idx, int(f.max()), int(t.max()))

    if max_idx < 0:
        raise ValueError("Le fichier d'arêtes est vide.")

    N = max_idx + 1
    if out_deg.size < N:
        padded = np.zeros(N, dtype=np.int64)
        padded[: out_deg.size] = out_deg
        out_deg = padded

    from_arr = np.concatenate(from_list).astype(np.int64)
    to_arr = np.concatenate(to_list).astype(np.int64)
    weights = np.ones_like(from_arr, dtype=np.float64) / out_deg[from_arr]

    T = coo_matrix((weights, (to_arr, from_arr)), shape=(N, N)).tocsr()
    return T, out_deg


def main():
    print("Construction de la matrice clairsemée...")
    T, out_deg = build_sparse_transition(EDGES_PATH, CHUNK_SIZE)
    N = T.shape[0]

    print(f"Nombre de pages : {N}")

    p = np.ones(N, dtype=np.float64) / N

    for k in range(MAX_ITER):
        p_next = T @ p
        dangling = (out_deg == 0)
        if dangling.any():
            p_next += p[dangling].sum() / N

        diff = np.linalg.norm(p_next - p, 1) / np.linalg.norm(p, 1)

        if diff < EPSILON:
            print(f"Convergence atteinte à k = {k + 1}")
            break

        p = p_next

    names = load_names(NAMES_PATH)
    top = np.argsort(p)[::-1][:TOP_K]

    print("\nTOP", TOP_K, "PAGES PAR PAGERANK\n")
    for rank, idx in enumerate(top, start=1):
        name = names[idx] if idx < len(names) else "UNKNOWN"
        print(f"{rank:2d}. {name:30s}")


if __name__ == "__main__":
    main()
