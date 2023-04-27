import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import torch.nn as nn
import torch.optim as optim
import json
from sklearn.model_selection import train_test_split
import pandas as pd

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

def map_label_to_int(label):
    try:
        label_int = int(label[2])
        if 0 <= label_int <= 2:
            return 1  # Relationship conflict
        elif 3 <= label_int <= 7:
            return 2  # Task conflict
        else:
            return 0  # No conflict
    except ValueError:
        return -1

def preprocess_data(data):

    utterances = []
    labels = []


    for conv in data:
        for i in conv["utterances"]:
            text = i["text"]

            min_label = -1
            if len(i["rebuttal_labels"]) > 0:
                for rebuttal_labels in i["rebuttal_labels"]:
                    label_int = map_label_to_int(rebuttal_labels)
                    if min_label == -1 or (label_int != -1 and label_int < min_label):
                        min_label = label_int
            else:
                min_label = 0  # No label

            if min_label != -1:
                utterances.append(text)
                labels.append(min_label)

    #print count of labels in dataset for 1 and 2
    print(labels.count(0))
    print(labels.count(1))
    print(labels.count(2))

    return utterances, labels

data = json.load(open("./Data/wikitactics.json", "r"))

conversations, labels = preprocess_data(data)

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Load pre-trained model (weights)
model = BertModel.from_pretrained("bert-base-uncased")

model.cuda()

# Set the model in evaluation mode to deactivate the DropOut modules
model.eval()

# Tokenize and process the input
input_texts = [tokenizer.encode(conversation, add_special_tokens=True) for conversation in conversations]

# Pad and create tensor
input_texts = torch.tensor([text[:512] if len(text) > 512 else text + [0] * (512 - len(text)) for text in input_texts])

input_texts = input_texts.cuda()

# Extract embeddings
with torch.no_grad():
    embeddings = model(input_texts)[0][:, 0, :]

# Split the dataset into a training set (80%) and an evaluation set (20%)
train_embeddings, eval_embeddings, train_labels, eval_labels = train_test_split(
    embeddings, labels, test_size=0.2, random_state=42
)

# Classifier model
class Classifier(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Classifier, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.fc(x)

input_dim = 768
output_dim = 4  # 0 to 7 and -1 (no label)

classifier = Classifier(input_dim, output_dim).cuda()

# Training parameters
batch_size = 8
epochs = 10
learning_rate = 1e-3

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(classifier.parameters(), lr=learning_rate)

# Remove data without labels
labeled_indices = [i for i, label in enumerate(labels) if label != -1]
labeled_embeddings = embeddings[labeled_indices]
labeled_labels = torch.tensor([labels[i] for i in labeled_indices])

# DataLoader
train_labels = torch.tensor(train_labels)
eval_labels = torch.tensor(eval_labels)

# DataLoader
train_dataset = torch.utils.data.TensorDataset(train_embeddings, train_labels)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Training loop
for epoch in range(epochs):
    for batch in train_loader:
        x, y = batch
        x = x.cuda()
        y = y.cuda()
        optimizer.zero_grad()
        y_pred = classifier(x)
        loss = criterion(y_pred, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

# Evaluate the model
with torch.no_grad():
    accuracy = (torch.sum(torch.argmax(classifier(eval_embeddings), dim=1) == eval_labels) / len(eval_labels)).item()

print(f"Accuracy: {accuracy * 100:.2f}%")
model_path = './model/utterance.pth'
torch.save(classifier.state_dict(), model_path)