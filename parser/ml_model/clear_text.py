import pandas as pd
import re
import os
from pathlib import Path
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

BASE_DIR = str(Path(__file__).parent.parent)

stemmer = SnowballStemmer("russian")
stop_words = set(stopwords.words("russian"))

def preprocess_text(text: str) -> str:
    """Очищает и нормализует текст"""
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Удаляем пунктуацию и цифры
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Удаляем множественные пробелы
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_dataset():
    """Очищает тексты в существующем CSV файле"""
    try:
        # Путь к файлу
        csv_path = os.path.join(BASE_DIR, "news_dataset.csv")
        
        # Читаем CSV файл
        df = pd.read_csv(csv_path)
        
        # Очищаем тексты
        df['text'] = df['text'].apply(preprocess_text)
        
        # Перезаписываем тот же файл
        df.to_csv(csv_path, index=False, encoding='utf-8', quoting=1)
        
        print(f"Тексты в датасете успешно очищены")
        print(f"Количество обработанных записей: {len(df)}")
        
        # Выводим несколько примеров
        print("\nПримеры очищенных текстов:")
        for i in range(min(5, len(df))):
            print(f"{df['text'].iloc[i]} -> {df['label'].iloc[i]}")
            
    except Exception as e:
        print(f"Ошибка при обработке датасета: {str(e)}")

if __name__ == "__main__":
    clean_dataset()