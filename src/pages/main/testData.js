import { testMarkDown } from './testMarkDown'

export const testData = [
    {
        "id":1,
        "title":"news2",
        "description": testMarkDown,
        "date":"2025-04-05",
        "category_id":5,
        "is_confirmed":true,
        "is_liked": false,
        "author_id":1,
        "author":{
            "id":1,
            "login":"user1"
        },
        "category":{
            "id":5,
            "title":"Лооооол"
        }
    },
    {
        "id":2,
        "title":"fwefwfwe",
        "description":"ne423423ws2fwefw desc",
        "date":"2025-04-05",
        "category_id":5,
        "is_confirmed":true,
        "is_liked": true,
        "author_id":1,
        "author":{
            "id":1,
            "login":"РНФ"
        },
        "category":{
            "id":5,
            "title":"Сучка"
        }
    },
    {
        "id":3,
        "title":"newfwefwefwfwfs2",
        "description":"news2 defwefwefwesc",
        "date":"2025-04-05",
        "category_id":5,
        "is_confirmed":true,
        "is_liked": false,
        "author_id":1,
        "author":{
            "id":1,
            "login":"Наука.рф"
        },
        "category":{
            "id":5,
            "title":"Математика"
        }
    },
]