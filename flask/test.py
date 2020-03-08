import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
import numpy as np

wine = pd.read_csv('wineQualityReds.csv')
wine['quality2'] = np.where(wine['quality']<=4,1, np.where(wine['quality']<=6,2,3))

X = wine.drop(columns=['quality','quality2'])
y = wine['quality2']
target_names = np.unique(y)
target_names
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)
lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(X, y).transform(X)

X = wine.drop(columns=['quality','quality2'])
y = wine['quality2']
target_names = np.unique(y)
print(target_names)
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)
lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(X, y).transform(X)


# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s'
 % str(pca.explained_variance_ratio_))
plt.figure()
colors = ['navy', 'turquoise', 'darkorange']
lw = 2
for color, i, target_name in zip(colors, target_names, target_names):
 plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, lw=lw,
 label=target_name)
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('PCA of WINE dataset')
plt.figure()
for color, i, target_name in zip(colors, target_names, target_names):
 plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], alpha=.8, color=color,
 label=target_name)
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('LDA of WINE dataset')
print(plt.show())