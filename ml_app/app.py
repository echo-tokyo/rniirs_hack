import os
from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Добавляем путь к корню проекта
sys.path.append(str(Path(__file__)))
from config import BASE_DIR

app = FastAPI(
    title="News Classification API",
    description="API для классификации научных новостей и материалов",
    version="1.0.0"
)

# Загрузка моделей при старте приложения
MODELS_DIR = os.path.join(BASE_DIR, "ml_model", "models")

try:
    with open(os.path.join(MODELS_DIR, 'vectorizer.pkl'), 'rb') as f:
        vectorizer: TfidfVectorizer = pickle.load(f)
    
    with open(os.path.join(MODELS_DIR, 'classifier.pkl'), 'rb') as f:
        classifier: LogisticRegression = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Ошибка загрузки моделей: {str(e)}")

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

@app.get("/")
async def health_check():
    return {"status": "OK", "message": "Сервис классификации новостей работает"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: TextRequest):
    try:
        # Векторизация текста
        vectorized_text = vectorizer.transform([request.text])
        
        # Предсказание
        probabilities = classifier.predict_proba(vectorized_text)
        class_idx = np.argmax(probabilities)
        confidence = probabilities[0, class_idx]
        prediction = classifier.classes_[class_idx]
        
        return {
            "prediction": prediction,
            "confidence": float(confidence)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке запроса: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)