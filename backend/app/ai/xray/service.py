import torch
from torchvision import transforms
from PIL import Image
import io
import json
import os
from .schemas import XRayInferenceOutput, KLProbabilities

class XRayInferenceService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../ai/training')))
        from model import KLGradingModel
        self.model = KLGradingModel(num_classes=5).to(self.device)
        
        self.model_ready = False
        self.model_version = "None"
        models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/xray/'))
        
        try:
            with open(os.path.join(models_dir, 'classification_report.json'), 'r') as f:
                report = json.load(f)
                macro_f1 = report['image_level']['macro_f1']
                # The quality gate threshold: e.g. macro-F1 > 0.4.
                # Right now it's ~0.11 so it will fail this gate!
                if macro_f1 > 0.4:
                    self.model_ready = True
        except Exception:
            self.model_ready = False
            
        if self.model_ready:
            try:
                checkpoint = torch.load(os.path.join(models_dir, 'best_model.pth'), map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.eval()
                self.model_version = checkpoint.get("model_version", "DenseNet121_KL_v1")
            except Exception:
                self.model_ready = False
            
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Policy thresholds
        self.HIGH_CONFIDENCE_THRESHOLD = 0.70
        self.MODERATE_CONFIDENCE_THRESHOLD = 0.50

    def analyze_image(self, file_content: bytes, filename: str) -> XRayInferenceOutput:
        if not self.model_ready:
            return XRayInferenceOutput(
                status="MODEL_NOT_READY",
                image_id=filename,
                message="X-ray AI assessment is currently unavailable because a validated model checkpoint has not been installed."
            )
            
        try:
            img = Image.open(io.BytesIO(file_content)).convert('RGB')
        except Exception:
            return XRayInferenceOutput(
                status="IMAGE_QUALITY_INSUFFICIENT",
                image_id=filename,
                message="The uploaded image could not be reliably assessed because image quality is insufficient."
            )
            
        input_tensor = self.transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            try:
                outputs = self.model(input_tensor)
                probs = torch.softmax(outputs, dim=1).cpu().numpy()[0]
            except Exception:
                return XRayInferenceOutput(
                    status="INFERENCE_FAILED",
                    image_id=filename,
                    message="X-ray analysis could not be completed. Please review the image and try again."
                )
            
        pred_class = int(probs.argmax())
        confidence = float(probs[pred_class])
        
        status = "SUCCESS"
        if confidence < self.MODERATE_CONFIDENCE_THRESHOLD:
            status = "AI_ASSESSMENT_UNCERTAIN"
            
        kl_probs = KLProbabilities(
            KL0=float(probs[0]),
            KL1=float(probs[1]),
            KL2=float(probs[2]),
            KL3=float(probs[3]),
            KL4=float(probs[4])
        )
            
        return XRayInferenceOutput(
            status=status,
            image_id=filename,
            predicted_kl_grade=pred_class if status != "AI_ASSESSMENT_UNCERTAIN" else None,
            probabilities=kl_probs,
            confidence=confidence,
            model_version=self.model_version,
            inference_device=str(self.device),
            message="AI-assisted radiographic severity classification. Clinical correlation is required." if status == "SUCCESS" else "The model produced an uncertain result. No definitive severity classification is displayed."
        )

