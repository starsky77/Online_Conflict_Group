import json
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import pairwise_distances
from fastdtw import fastdtw


def map_label_to_int(label):
    try:
        label_int = int(label[2])
        if 0 <= label_int <= 1:
            return 2  # Relationship conflict
        elif 2 <= label_int <= 7:
            return 1  # Task conflict
        else:
            return 0
    except ValueError:
        return 0

data = json.load(open("./Data/wikitactics.json", "r"))

sns.set_style("darkgrid")

uters_labels=[]

for i in range(213):
    uter_labels = []
    for uter in data[i]["utterances"]:
        flag = -1
        for label in uter["rebuttal_labels"]:
            if map_label_to_int(label)> flag:
                flag=map_label_to_int(label)
            
        uter_labels.append(flag)
    uters_labels.append(uter_labels)


def binary_indicator(x, y):
    return 0 if x == y else 1

def dtw_distance(x, y):
    distance, _ = fastdtw(x, y, dist=binary_indicator)
    return distance


# Calculate the pairwise distance matrix using DTW
n = len(uters_labels)
distance_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        distance_matrix[i, j] = dtw_distance(uters_labels[i], uters_labels[j])
        distance_matrix[j, i] = distance_matrix[i, j]

# Calculate the linkage matrix using hierarchical clustering
linkage_matrix = linkage(squareform(distance_matrix), method='average')

# Plot the dendrogram
plt.figure(figsize=(30, 6))
dendrogram(linkage_matrix)
plt.title("Dendrogram of Hierarchical Clustering")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.savefig('linkage_matrix.png',dpi=300)
plt.close()

# Choose the number of clusters or a distance threshold
num_clusters = 4

# Get the cluster assignments for each sequence
clusters = fcluster(linkage_matrix, num_clusters, criterion='maxclust')

# print("Cluster assignments:", clusters)