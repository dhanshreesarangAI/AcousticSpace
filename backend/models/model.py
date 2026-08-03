import torch
import torch.nn as nn
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import numpy as np

class AcousticSpaceModel:
    def __init__(self):
        """
        Initialize AST model for deepfake detection
        """
        self.model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
        self.feature_extractor = ASTFeatureExtractor.from_pretrained(self.model_name)
        self.model = ASTForAudioClassification.from_pretrained(self.model_name)
        self.model.eval()
        print("Model loaded successfully!")

    def preprocess(self, audio, sr):
        """
        Preprocess audio for model input
        """
        inputs = self.feature_extractor(
            audio,
            sampling_rate=sr,
            return_tensors="pt"
        )
        return inputs

    def predict(self, audio, sr):
        """
        Predict if audio is REAL or DEEPFAKE
        """
        inputs = self.preprocess(audio, sr)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
            confidence = torch.max(probabilities).item()

        # Determine prediction
        predicted_class = torch.argmax(probabilities).item()
        prediction = "DEEPFAKE" if predicted_class == 1 else "REAL"

        result = {
            "prediction": prediction,
            "confidence_score": round(confidence * 100, 2),
            "real_probability": round(probabilities[0][0].item() * 100, 2),
            "fake_probability": round(probabilities[0][1].item() * 100, 2)
        }

        print(f"Prediction: {prediction}")
        print(f"Confidence: {confidence * 100:.2f}%")

        return result

    def save_model(self, path="saved_model/ast_model.pt"):
        """
        Save trained model
        """
        torch.save(self.model.state_dict(), path)
        print(f"Model saved at {path}")

    def load_model(self, path="saved_model/ast_model.pt"):
        """
        Load saved model
        """
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
        print(f"Model loaded from {path}")