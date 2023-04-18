import json
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt


def map_label_to_int(label):
    try:
        label_int = int(label[2])
        if 0 <= label_int <= 2:
            return 2  # Relationship conflict
        elif 3 <= label_int <= 7:
            return 1  # Task conflict
        else:
            return -1
    except ValueError:
        return -1

data = json.load(open("./Data/wikitactics.json", "r"))

sns.set_style("darkgrid")

# Create a large figure
plt.figure(figsize=(40, 40))

for i in range(213):
    uter_labels = []
    for uter in data[i]["utterances"]:
        flag = -1
        for label in uter["rebuttal_labels"]:
            if map_label_to_int(label) == 2:
                flag = 2
            elif flag != 2 and map_label_to_int(label) == 1:
                flag = 1
            
        uter_labels.append(flag)

    plt.subplot(15, 15, i+1)
    plt.plot(uter_labels)

# Save the large figure containing all subplots
plt.savefig('all_subplots.png', dpi=300)
plt.close()