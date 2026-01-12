## PageRank sur un graphe orienté

Ce projet calcule un score PageRank à partir d'une liste d'arêtes (`edges.csv`) et affiche les pages les mieux classées en utilisant les noms fournis dans `names.csv`.

### Données attendues
- `edges.csv` : deux colonnes `FromNode,ToNode` (IDs de nœuds, numérotés à partir de 1).
- `PAGE_RANK/names.csv` (ou `names.csv` à la racine) : une colonne `Name` alignée sur les IDs (ligne 1 = node 1).

### Comment ça marche
1) **Rappel théorique** : PageRank cherche le vecteur stationnaire `p` vérifiant `p = T @ p`, où `T` est la matrice de transition normalisée par colonne. Les nœuds sans sortie (dangling) redistribuent leur masse uniformément pour conserver `∑ p_i = 1`.  
2) `build_sparse_transition` lit `edges.csv` par blocs (`chunksize=1_000_000`), compte les degrés sortants et construit les tableaux 0-based `from_arr`, `to_arr`.  
3) Une matrice clairsemée `T` est créée avec `scipy.sparse.coo_matrix`, puis convertie en CSR pour accélérer les produits `T @ p`.  
4) La boucle principale (`MAX_ITER`, tolérance `EPSILON`) applique `p_next = T @ p`, ajoute la contribution uniforme des nœuds pendants, et vérifie la norme L1 relative pour détecter la convergence.  
5) Les résultats sont triés (top `TOP_K`), et les noms sont récupérés dans `names.csv` (ou `UNKNOWN` si l’ID n’existe pas).  

### Points importants du code
- `PAGE_RANK/main.py` détecte automatiquement l’emplacement des CSV (racine ou dossier `PAGE_RANK`).  
- La construction de la matrice est en streaming pour limiter la mémoire, puis les itérations se font intégralement en mémoire (`scipy.sparse`).  
- Les indices sont convertis en 0-based pour numpy/SciPy, mais la sortie reste alignée avec les IDs 1-based du CSV.

### Lancer le calcul
Depuis la racine du repo :
```bash
python PAGE_RANK/main.py
```

Assure-toi d’avoir `pandas`, `numpy` et `scipy` installés dans ton environnement Python (Anaconda recommandé).

### Complexité temporelle
- Prétraitement (construction de `T`) : `O(M)` où `M` est le nombre d’arêtes, avec une seule passe disque grâce à la lecture par blocs.  
- Une itération PageRank sur la version clairsemée : `O(nnz)` avec `nnz = M` pour `T @ p`, plus `O(N)` pour gérer les nœuds pendants (`N` = nombre de nœuds).  
- Total pour `K` itérations : `O(M + K·(M + N)) ≈ O(K·M)` quand `M >> N`, ce qui correspond à la complexité théorique du PageRank classique.

### Version clairsemée (optimisée)
- Ce qui change : on lit `edges.csv` une fois pour construire une matrice de transition clairsemée `T` en format CSR (via SciPy), puis chaque itération fait simplement `p_next = T @ p` et ajoute la masse des nœuds pendants. Les IDs sont décalés en 0-based au moment de la construction.  
- Pourquoi c’est plus rapide : l’approche initiale relisait le CSV à chaque itération (`compute_out_degree` + `pagerank_iteration` streamés), soit `K` passes disque. La version sparse construit `T` en une seule passe, puis toutes les itérations restent en mémoire : coût `O(M)` pour la construction, puis `O(K·nnz)` avec `nnz = M`, sans I/O répétées. Sur de gros graphes, on réduit fortement le temps total et la pression I/O tout en gardant la même logique théorique.
