import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Добавляем корневую директорию parser в путь
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import BASE_DIR

def merge_rare_categories(df, threshold=50):
    """Объединяет редкие категории в 'Другое'"""
    # Находим редкие категории
    category_counts = df['label'].value_counts()
    rare_categories = category_counts[category_counts < threshold].index
    
    # Заменяем редкие категории на 'Другое'
    df['label'] = df['label'].apply(lambda x: 'Другое' if x in rare_categories else x)
    return df

def visualize_dataset():
    try:
        # Читаем датасет
        csv_path = os.path.join(BASE_DIR, "news_dataset.csv")
        df = pd.read_csv(csv_path)
        
        # Объединяем редкие категории
        df = merge_rare_categories(df)
        
        # Сохраняем обновленный датасет
        df.to_csv(csv_path, index=False, encoding='utf-8', quoting=1)
        
        # Создаем фигуру большего размера
        plt.figure(figsize=(15, 10))
        
        # 1. Распределение по категориям
        plt.subplot(2, 1, 1)
        sns.countplot(data=df, x='label', order=df['label'].value_counts().index)
        plt.title('Распределение новостей по категориям')
        plt.xlabel('Категория')
        plt.ylabel('Количество новостей')
        plt.xticks(rotation=45, ha='right')
        
        # 2. Процентное соотношение
        plt.subplot(2, 1, 2)
        percentages = df['label'].value_counts(normalize=True) * 100
        plt.pie(percentages, labels=percentages.index, autopct='%1.1f%%')
        plt.title('Процентное соотношение категорий')
        
        # Добавляем статистику
        total_news = len(df)
        unique_categories = df['label'].nunique()
        print(f"\nСтатистика датасета:")
        print(f"Всего новостей: {total_news}")
        print(f"Количество категорий: {unique_categories}")
        print("\nРаспределение по категориям:")
        for category, count in df['label'].value_counts().items():
            percentage = (count / total_news) * 100
            print(f"{category}: {count} новостей ({percentage:.1f}%)")
        
        # Настраиваем отображение
        plt.tight_layout()
        
        # Сохраняем график
        plt.savefig(os.path.join(BASE_DIR, 'category_distribution.png'))
        print("\nГрафик сохранен в category_distribution.png")
        
        # Показываем график
        plt.show()
        
    except Exception as e:
        print(f"Ошибка при визуализации: {str(e)}")

if __name__ == "__main__":
    visualize_dataset()