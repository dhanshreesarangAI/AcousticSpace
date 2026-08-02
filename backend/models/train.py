import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
import sys
sys.path.append('../pipeline')
from model import AcousticSpaceModel
from feature_extractor import extract_all_features

class AudioDataset(Dataset):
    def __init__(self, real_path, fake_path):
        """
        Load real and fake audio files from dataset
        """
        self.files = []
        self.labels = []

        # Load real audio files — label 0
        for file in os.listdir(real_path):
            if file.endswith(".wav"):
                self.files.append(os.path.join(real_path, file))
                self.labels.append(0)

        # Load fake audio files — label 1
        for file in os.listdir(fake_path):
            if file.endswith(".wav"):
                self.files.append(os.path.join(fake_path, file))
                self.labels.append(1)

        print(f"Total files loaded: {len(self.files)}")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        features = extract_all_features(self.files[idx])
        label = self.labels[idx]
        return features, label

def train_model(real_path, fake_path, epochs=10):
    """
    Train the AST model on ASVspoof dataset
    """
    # Load dataset
    dataset = AudioDataset(real_path, fake_path)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    # Initialize model
    acoustic_model = AcousticSpaceModel()
    optimizer = torch.optim.Adam(
        acoustic_model.model.parameters(), 
        lr=0.0001
    )
    criterion = nn.CrossEntropyLoss()

    # Training loop
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for features, labels in dataloader:
            optimizer.zero_grad()
            outputs = acoustic_model.model(**features)
            loss = criterion(outputs.logits, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            predicted = torch.argmax(outputs.logits, dim=1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

        accuracy = correct / total * 100
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"Loss: {total_loss:.4f}")
        print(f"Accuracy: {accuracy:.2f}%")
        print("---")

    # Save trained model
    acoustic_model.save_model("saved_model/ast_model.pt")
    print("Training complete!")

if __name__ == "__main__":
    train_model(
        real_path="../../data/real/",
        fake_path="../../data/fake/"
    )
    
    