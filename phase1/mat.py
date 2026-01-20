# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA

# # Load embeddings
# embeddings = np.load("embeddings.npy")

# # Reduce to 2D
# pca = PCA(n_components=2)
# reduced_embeddings = pca.fit_transform(embeddings)

# # Plot
# plt.figure()
# plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
# plt.title("Embedding Visualization (PCA)")
# plt.xlabel("Component 1")
# plt.ylabel("Component 2")
# plt.show()

# visualize_pca_3d.py

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# from mpl_toolkits.mplot3d import Axes3D

# embeddings = np.load("embeddings.npy")

# pca = PCA(n_components=3)
# points = pca.fit_transform(embeddings)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
# ax.scatter(points[:, 0], points[:, 1], points[:, 2])
# ax.set_title("PCA 3D Embedding Visualization")
# plt.show()

# visualize_tsne.py

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.manifold import TSNE

# embeddings = np.load("embeddings.npy")

# tsne = TSNE(n_components=2, perplexity=10, random_state=42)
# points = tsne.fit_transform(embeddings)

# plt.figure()
# plt.scatter(points[:, 0], points[:, 1])
# plt.title("t-SNE Embedding Visualization")
# plt.show()

# visualize_umap.py

import numpy as np
import matplotlib.pyplot as plt
import umap

embeddings = np.load("embeddings.npy")

reducer = umap.UMAP(n_components=2, random_state=42)
points = reducer.fit_transform(embeddings)

plt.figure()
plt.scatter(points[:, 0], points[:, 1])
plt.title("UMAP Embedding Visualization")
plt.show()
