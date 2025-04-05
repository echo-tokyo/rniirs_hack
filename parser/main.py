from models.models import RscfParser
from utils.storage import load_processed_links, save_processed_links, send_to_database
from utils.utils import format_news_item

def main():
    parser = RscfParser()
    processed_links = load_processed_links()
    current_news = parser.get_news()
    
    if not current_news:
        print("Не удалось получить новости")
        return
    print(current_news)
    new_news = [news for news in current_news if news['link'] not in processed_links]
    
    if new_news:
        print(f"Найдено {len(new_news)} новых новостей")
        new_news_items = []
        
        for i, news in enumerate(new_news, 1):
            print(f"Обработка новой новости {i}/{len(new_news)}: {news['title'][:50]}...")
            try:
                detail = parser.get_news_detail(news['link'])
                news_item = format_news_item(news, detail)
                print(news_item)
                new_news_items.append(news_item)
                processed_links.add(news['link'])
            except Exception as e:
                print(f"Ошибка при обработке новости: {str(e)}")
                continue
        
        if new_news_items:
            save_processed_links(processed_links)
            send_to_database(new_news_items, is_update=True)
            print(f"Обработано и отправлено {len(new_news_items)} новых новостей")
    else:
        print("Новых новостей не найдено")

if __name__ == "__main__":
    main()
    