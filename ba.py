import base64
import io
import librosa
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Tuple
import warnings

warnings.filterwarnings('ignore')

app = FastAPI(title="Multi-Language AI Voice Detection API")

class AudioInput(BaseModel):
    audio_base64: str
    language: str

class VoiceDetectionResponse(BaseModel):
    classification: str
    confidence_score: float
    explanation: str
    language: str
    features_summary: Dict[str, float]

def extract_advanced_features(audio_bytes: bytes) -> Dict[str, float]:
    try:
        audio_buffer = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_buffer, sr=16000, mono=True)
        
        features = {}
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = float(np.mean(mfcc))
        features['mfcc_std'] = float(np.std(mfcc))
        
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zcr_mean'] = float(np.mean(zcr))
        features['zcr_std'] = float(np.std(zcr))
        
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = float(np.mean(spec_centroid))
        features['spectral_centroid_std'] = float(np.std(spec_centroid))
        
        spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['spectral_rolloff_mean'] = float(np.mean(spec_rolloff))
        features['spectral_rolloff_std'] = float(np.std(spec_rolloff))
        
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_mean'] = float(np.mean(chroma))
        features['chroma_std'] = float(np.std(chroma))
        
        spec_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        features['spectral_contrast_mean'] = float(np.mean(spec_contrast))
        features['spectral_contrast_std'] = float(np.std(spec_contrast))
        
        tempogram = librosa.feature.tempogram(y=y, sr=sr)
        features['tempogram_mean'] = float(np.mean(tempogram))
        
        rms = librosa.feature.rms(y=y)
        features['rms_mean'] = float(np.mean(rms))
        features['rms_std'] = float(np.std(rms))
        
        return features
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

def detect_voice_advanced(features: Dict[str, float], language: str) -> Tuple[int, float, str]:
    ai_score = 0.0
    explanations = []
    
    if features['mfcc_std'] < 15:
        ai_score += 0.2
        explanations.append("Low MFCC variance detected")
    else:
        explanations.append("Natural MFCC variation")
    
    if features['zcr_mean'] > 0.15 or features['zcr_mean'] < 0.05:
        ai_score += 0.2
        explanations.append("Unusual zero-crossing patterns")
    else:
        explanations.append("Natural zero-crossing patterns")
    
    if features['spectral_centroid_mean'] > 4000 or features['spectral_centroid_mean'] < 2000:
        ai_score += 0.15
        explanations.append("Anomalous spectral centroid")
    else:
        explanations.append("Natural spectral centroid")
    
    if features['spectral_rolloff_std'] < 1000:
        ai_score += 0.15
        explanations.append("Overly smooth spectral envelope")
    else:
        explanations.append("Natural spectral envelope variation")
    
    if features['chroma_std'] < 0.15:
        ai_score += 0.15
        explanations.append("Unnaturally perfect pitch")
    else:
        explanations.append("Natural pitch variation")
    
    if features['rms_std'] < 0.01:
        ai_score += 0.15
        explanations.append("Overly consistent amplitude")
    else:
        explanations.append("Natural amplitude variation")
    
    if ai_score > 0.5:
        label = 1
        confidence = min(0.99, 0.5 + ai_score * 0.5)
    else:
        label = 0
        confidence = min(0.99, 1 - ai_score)
    
    explanation = " | ".join(explanations)
    return label, confidence, explanation

def validate_language(language: str) -> bool:
    supported_languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    return language in supported_languages

@app.get("/")
async def root():
    return {
        "message": "Multi-Language AI Voice Detection API",
        "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
        "endpoint": "/detect_voice"
    }

@app.post("/detect_voice", response_model=VoiceDetectionResponse)
async def detect_voice(data: AudioInput) -> VoiceDetectionResponse:
    if not validate_language(data.language):
        raise HTTPException(
            status_code=400,
            detail="Unsupported language. Supported: Tamil, English, Hindi, Malayalam, Telugu"
        )
    
    try:
        audio_bytes = base64.b64decode(data.audio_base64)
        features = extract_advanced_features(audio_bytes)
        label, confidence, explanation = detect_voice_advanced(features, data.language)
        
        response = VoiceDetectionResponse(
            classification="AI-generated" if label == 1 else "Human",
            confidence_score=round(confidence, 4),
            explanation=explanation,
            language=data.language,
            features_summary={
                "mfcc_std": round(features['mfcc_std'], 2),
                "zcr_mean": round(features['zcr_mean'], 4),
                "spectral_centroid": round(features['spectral_centroid_mean'], 2),
                "chroma_std": round(features['chroma_std'], 4),
                "rms_mean": round(features['rms_mean'], 4)
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

{
  "audio_base64": "BASE64_ENCODED_AUDIO_HERE",
  "language": "English"
}

import requests
import base64

API_URL = "http://127.0.0.1:8000/detect_voice"

# Read your audio file (MP3, WAV, etc.)
with open("your_audio_file.mp3", "rb") as f:
    audio_bytes = f.read()

# Encode to Base64
audio_base64 = base64.b64encode(audio_bytes).decode()

# Test request
payload = {
    "audio_base64": audio_base64,
    "language": "English"  # Change to Tamil, Hindi, Malayalam, Telugu
}

response = requests.post(API_URL, json=payload)
print(response.json())

{
  "classification": "Human",
  "confidence_score": 0.85,
  "explanation": "Natural MFCC variation | Natural zero-crossing patterns...",
  "language": "English",
  "features_summary": {...}
}