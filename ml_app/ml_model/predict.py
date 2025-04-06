import pickle
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import BASE_DIR

class NewsClassifier:
    def __init__(self):
        models_dir = os.path.join(BASE_DIR, "ml_model", "models")
        
        # Загружаем векторизатор
        with open(os.path.join(models_dir, 'vectorizer.pkl'), 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        # Загружаем модель
        with open(os.path.join(models_dir, 'classifier.pkl'), 'rb') as f:
            self.model = pickle.load(f)
    
    def predict_category(self, text: str) -> str:
        """Предсказывает категорию для текста новости"""
        # Векторизуем текст
        text_vectorized = self.vectorizer.transform([text])
        # Получаем предсказание
        prediction = self.model.predict(text_vectorized)
        return prediction[0]

def test_classifier():
    classifier = NewsClassifier()
    
    # Тестовые примеры
    test_texts = [
        "Ученые разработали новый метод синтеза полимеров",
        "Фонд объявляет о начале приема заявок",
        "Исследователи обнаружили новый вид бактерий"
    ]
    
    for text in test_texts:
        category = classifier.predict_category(text)
        print(f"\nТекст: {text}")
        print(f"Категория: {category}")

if __name__ == "__main__":
    test_classifier()
