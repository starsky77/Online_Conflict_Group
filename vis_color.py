import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def map_label_to_int(label):
    try:
        label_int = int(label[2])
        if label_int == 0:
            return 3  # DH0
        elif label_int == 1:
            return 2  # DH1
        elif 2 <= label_int <= 7:
            return 1  # Task conflict
        else:
            return -1
    except ValueError:
        return -1

data = json.load(open("./Data/wikitactics.json", "r"))

sns.set_style("darkgrid")
plt.figure(figsize=(60, 60))
colormap = plt.cm.get_cmap("tab10")

for i in range(213):
    uter_labels = []
    username_colors = {}
    unique_usernames = list(set([uter["username"] for uter in data[i]["utterances"]]))

    for idx, username in enumerate(unique_usernames):
        username_colors[username] = colormap(idx % 10)

    for uter in data[i]["utterances"]:
        flag = -1
        for label in uter["rebuttal_labels"]:
            if map_label_to_int(label)> flag:
                flag=map_label_to_int(label)
            
        uter_labels.append(flag)

    plt.subplot(15, 15, i+1)
    x = np.arange(len(uter_labels))
    
    # Connect adjacent points with lines
    for idx, (x_val, y_val) in enumerate(zip(x, uter_labels)):
        if idx > 0:
            plt.plot(x[idx-1:idx+1], uter_labels[idx-1:idx+1], color=username_colors[data[i]["utterances"][idx]["username"]])
        plt.scatter(x_val, y_val, color=username_colors[data[i]["utterances"][idx]["username"]])

    plt.title(str(i))

plt.savefig('all_subplots_colored_connected_3level.png', dpi=300)
plt.close()
