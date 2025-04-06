import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
import os
import sys

from config import BASE_DIR

def train_classifier():
    # 1. Загрузка данных
    csv_path = os.path.join(BASE_DIR, "news_dataset.csv")
    df = pd.read_csv(csv_path)
    
    # Очистка данных
    print("\nПредварительная обработка данных:")
    print(f"Исходное количество записей: {len(df)}")
    
    # Удаляем строки с пустыми значениями
    df = df.dropna(subset=['text', 'label'])
    
    # Удаляем дубликаты
    df = df.drop_duplicates(subset=['text'])
    
    print(f"Количество записей после очистки: {len(df)}")
    print("\nРаспределение по категориям:")
    print(df['label'].value_counts())
    
    # 2. Подготовка данных
    X = df['text'].values  # тексты новостей
    y = df['label'].values  # категории
    
    # Разделение на тренировочную и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Векторизация текста
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        strip_accents='unicode'
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    # 4. Обучение модели
    model = LogisticRegression(
        multi_class='multinomial',
        max_iter=1000,
        random_state=42
    )
    
    model.fit(X_train_vectorized, y_train)
    
    # 5. Оценка модели
    y_pred = model.predict(X_test_vectorized)
    print("\nОтчет о классификации:")
    print(classification_report(y_test, y_pred))
    
    # 6. Сохранение модели и векторизатора
    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    with open(os.path.join(models_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open(os.path.join(models_dir, 'classifier.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    print("\nМодель и векторизатор сохранены в директории models/")
    
    # 7. Пример использования
    print("\nПример классификации:")
    test_texts = [
        "Ученые разработали новый метод синтеза полимеров",
        "Фонд объявляет о начале приема заявок",
        "Исследователи обнаружили новый вид бактерий"
    ]
    
    test_vectorized = vectorizer.transform(test_texts)
    predictions = model.predict(test_vectorized)
    
    for text, pred in zip(test_texts, predictions):
        print(f"\nТекст: {text}")
        print(f"Предсказанная категория: {pred}")

if __name__ == "__main__":
    train_classifier() 