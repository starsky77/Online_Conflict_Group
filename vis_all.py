import json
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt


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

sns.set_style("darkgrid")


plt.figure(figsize=(40, 40))

for i in range(213):
    uter_labels = []
    for uter in data[i]["utterances"]:
        flag = -1
        for label in uter["rebuttal_labels"]:
            if map_label_to_int(label)> flag:
                flag=map_label_to_int(label)
            
        uter_labels.append(flag)

    plt.subplot(15, 15, i+1)
    plt.plot(uter_labels)
    plt.title(str(i))

plt.savefig('all_subplots.png', dpi=300)
plt.close()