import torch
import torch.nn as nn
from transformers import ASTFeatureExtractor, ASTForAudioClassification
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
import sys
sys.path.append('../pipeline')
from audio_loader import load_audio

class ASVspoofDataset(Dataset):
    def __init__(self, real_path, fake_path, feature_extractor):
        """
        Dataset class specifically for ASVspoof data
        """
        self.files = []
        self.labels = []
        self.feature_extractor = feature_extractor

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

        print(f"Dataset loaded: {len(self.files)} files")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        # Load audio file
        audio, sr = load_audio(self.files[idx])

        # Extract features using AST feature extractor
        inputs = self.feature_extractor(
            audio,
            sampling_rate=sr,
            return_tensors="pt",
            padding=True
        )

        return {
            "input_values": inputs.input_values.squeeze(),
            "label": torch.tensor(self.labels[idx])
        }

def fine_tune(real_path, fake_path, epochs=5):
    """
    Fine tune AST model on ASVspoof dataset
    """
    # Load pretrained model and feature extractor
    model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
    feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
    model = ASTForAudioClassification.from_pretrained(
        model_name,
        num_labels=2,
        ignore_mismatched_sizes=True
    )

    # Load dataset
    dataset = ASVspoofDataset(real_path, fake_path, feature_extractor)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # Setup optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    criterion = nn.CrossEntropyLoss()

    # Fine tuning loop
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for batch in dataloader:
            input_values = batch["input_values"]
            labels = batch["label"]

            optimizer.zero_grad()
            outputs = model(input_values=input_values)
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

    # Save fine tuned model
    torch.save(model.state_dict(), "saved_model/fine_tuned_ast.pt")
    print("Fine tuning complete!")
    print("Model saved at saved_model/fine_tuned_ast.pt")

if __name__ == "__main__":
    fine_tune(
        real_path="../../data/real/",
        fake_path="../../data/fake/"
    )