import json
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def map_label_to_int(label):
    try:
        label_int = int(label[2])
        if 0 <= label_int <= 1:
            return 2  # Relationship conflict
        elif 2 <= label_int <= 7:
            return 1  # Task conflict
        else:
            return -1
    except ValueError:
        return -1


data = json.load(open("./Data/wikitactics.json", "r"))
colormap = plt.cm.get_cmap("tab10")

sns.set_style("darkgrid")

# for i in range(213):
#     uter_labels = []
#     for uter in data[i]["utterances"]:
#         flag = -1
#         for label in uter["rebuttal_labels"]:
#             if map_label_to_int(label)> flag:
#                 flag=map_label_to_int(label)
            
#         uter_labels.append(flag)

#     plt.figure(figsize=(10, 8))
#     plt.plot(uter_labels)
#     plt.title(str(data[i]["conv_id"]))
#     plt.savefig(f'./Vis/conv_{i}.png')
#     plt.close()
#     with open(f'./Vis/conv_{i}.txt', 'w') as f:
#         for uterance in data[i]["utterances"]:
#             f.write(str(uterance) + '\n')


for i in range(213):
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

    plt.figure(figsize=(10, 8))
    x = np.arange(len(uter_labels))
    
    # Connect adjacent points with lines
    for idx, (x_val, y_val) in enumerate(zip(x, uter_labels)):
        if idx > 0:
            plt.plot(x[idx-1:idx+1], uter_labels[idx-1:idx+1], color=username_colors[data[i]["utterances"][idx]["username"]])
        plt.scatter(x_val, y_val, color=username_colors[data[i]["utterances"][idx]["username"]])

    plt.title(str(data[i]["conv_id"]))
    plt.savefig(f'./Vis/conv_{i}.png')
    plt.close()
    with open(f'./Vis/conv_{i}.txt', 'w') as f:
        for uterance in data[i]["utterances"]:
            f.write(str(uterance) + '\n')
