import json
import matplotlib.pyplot as plt
import seaborn as sns
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
            # Note that here the class number is different. Different value would influence the cluster result
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

# Choose the number of clusters or a distance threshold
num_clusters = 4

# Get the cluster assignments for each sequence
group_list = fcluster(linkage_matrix, num_clusters, criterion='maxclust')

print(group_list)

colormap = plt.cm.get_cmap("tab10")

# Loop through the 4 groups
for group in range(1, 5):
    group_indices = [idx for idx, value in enumerate(group_list) if value == group]
    plt.figure(figsize=(50, 50))

    for j, i in enumerate(group_indices):
        uter_labels = []
        username_colors = {}
        unique_usernames = list(set([uter["username"] for uter in data[i]["utterances"]]))

        for idx, username in enumerate(unique_usernames):
            username_colors[username] = colormap(idx % 10)

        for uter in data[i]["utterances"]:
            flag = -1
            for label in uter["rebuttal_labels"]:
                if map_label_to_int(label) == 2:
                    flag = 2
                elif flag != 2 and map_label_to_int(label) == 1:
                    flag = 1
                
            uter_labels.append(flag)

        if group==4:
            plt.subplot(15, 15, j+1)
        else:
            plt.subplot(4, 4, j+1)
        x = np.arange(len(uter_labels))

        # Connect adjacent points with lines
        for idx, (x_val, y_val) in enumerate(zip(x, uter_labels)):
            if idx > 0:
                plt.plot(x[idx-1:idx+1], uter_labels[idx-1:idx+1], color=username_colors[data[i]["utterances"][idx]["username"]])
            plt.scatter(x_val, y_val, color=username_colors[data[i]["utterances"][idx]["username"]])
        plt.title(str(i))

    # Save the figure for the current group
    plt.savefig(f'group_{group}_plots.png', dpi=300)
    plt.close()
