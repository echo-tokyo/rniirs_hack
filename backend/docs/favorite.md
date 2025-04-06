## Получение списка избранного текущего юзера

### Input

> (в заголовках токен авторизации)

```text
GET /api/news/favorite/
```

### Output

```json5
[
    {
        "id": 5,
        "title": "news2",
        "description": "news2 desc",
        "date": "2025-04-05",
        "is_confirmed": true,
        "liked": true,
        "author_id": 1,
        "author":{
          "id": 1,
          "login": "user1"
        },
        "category_id": 5,
        "category": {
            "id": 5,
            "title": "Математика"
        }
    }
    // ...
]
```

## Получение списка избранного определённого юзера

### Input

> (в заголовках токен авторизации)
> 
> _Query:_
> 
> `user_id` - ID юзера, список избранного которого нужно получить

```text
GET /api/news/favorite/?user_id=2
```

### Output

> тот же (см. выше)

## Помещение новости в список избранного юзера

### Input

> (в заголовках токен авторизации)
> 
> _Path:_
> 
> `pk` - ID новости, которую нужно поместить в список избранного

```text
PATCH /api/news/favorite/{pk}/like/
```

### Output

> тот же (см. выше)

## Удаление новости из списка избранного юзера

### Input

> (в заголовках токен авторизации)
> 
> _Path:_
> 
> `pk` - ID новости, которую нужно убрать из списка избранного

```text
PATCH /api/news/favorite/{pk}/unlike/
```

### Output

> тот же (см. выше)
