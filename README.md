## PageRank sur un graphe orienté

Ce projet calcule un score PageRank à partir d'une liste d'arêtes (`edges.csv`) et affiche les pages les mieux classées en utilisant les noms fournis dans `names.csv`.

### Données attendues
- `edges.csv` : deux colonnes `FromNode,ToNode` (IDs de nœuds, numérotés à partir de 1).
- `PAGE_RANK/names.csv` (ou `names.csv` à la racine) : une colonne `Name` alignée sur les IDs (ligne 1 = node 1).

### Comment ça marche
1) `compute_out_degree` parcourt `edges.csv` par blocs (`chunksize=1_000_000`) et compte le nombre de sorties pour chaque nœud.  
2) `pagerank_iteration` met à jour le vecteur de probabilité `p` :
   - contribution de chaque nœud vers ses voisins : `p[from] / out_deg[from]`
   - redistribution des nœuds sans sortie (dangling) de façon uniforme
3) La boucle principale (`MAX_ITER`, tolérance `EPSILON`) itère jusqu’à convergence (norme L1 relative) ou jusqu’à la limite d’itérations.  
4) Les résultats sont triés et affichés (top `TOP_K`), avec les noms si disponibles.

### Points importants du code
- `PAGE_RANK/main.py` détecte automatiquement l’emplacement des CSV (racine ou dossier `PAGE_RANK`).  
- Le calcul est en streaming (lecture par chunk) pour supporter de gros fichiers d’arêtes.  
- Les indices sont décalés : `NodeId = idx + 1` quand on accède aux tableaux Python (0-based).

### Lancer le calcul
Depuis la racine du repo :
```bash
python PAGE_RANK/main.py
```

Assure-toi d’avoir `pandas` et `numpy` installés dans ton environnement Python (Anaconda recommandé).

### Complexité temporelle
- Prétraitement (compte des degrés sortants) : `O(M)` où `M` est le nombre d’arêtes, avec lecture par blocs pour limiter la mémoire.
- Une itération PageRank : une seule passe sur `edges.csv`, donc `O(M)` ; le reste (normalisations, norme L1) est `O(N)` avec `N` nœuds.
- Total pour `K` itérations : `O(M + K·M + K·N) ≈ O(K·M)` quand `M >> N`. Chaque passe lit les données en streaming sans stockage dense des arêtes.

### Version clairsemée (optimisée)
- Ce qui change : on lit `edges.csv` une fois pour construire une matrice de transition clairsemée `T` en format CSR (via SciPy), puis chaque itération fait simplement `p_next = T @ p` (multiplication sparse) et ajoute la masse des nœuds pendants. Les IDs sont décalés en 0-based au moment de la construction.
- Pourquoi c’est plus rapide : l’approche initiale relisait le CSV à chaque itération (`K` passes disque). La version sparse fait 1 passe pour construire `T`, puis chaque itération est en mémoire sur une matrice clairsemée : coût `O(M)` pour la construction, puis `O(K·nnz)` avec `nnz = M`, mais sans I/O répétées. Sur de gros graphes, on réduit fortement le temps total et la pression I/O.
