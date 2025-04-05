<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const router = useRouter()
const route = useRoute()
const isAdmin = localStorage.getItem('isAdmin')

const newsData = ref({
    id: null,
    header: '',
    description: '',
    date: '',
    category: '',
    author: '',
    content: '',
    status: 'pending'
})

// Настраиваем marked для обработки ссылок и изображений
marked.use({
    gfm: true,
    breaks: true,
    mangle: false,
    headerIds: false
})

// Создаем вычисляемое свойство для преобразованного HTML
const parsedContent = computed(() => {
    if (!newsData.value.content) return ''
    const html = marked(newsData.value.content)
    return DOMPurify.sanitize(html)
})

// В реальном приложении здесь будет API-запрос
onMounted(() => {
    // Временные данные для демонстрации
    newsData.value = {
        id: route.params.id,
        header: "Название новости",
        description: "Краткое описание новости",
        date: "04.02.2025",
        category: "Категория",
        author: "Автор статьи",
        content: `# Заголовок статьи

Это пример **форматированного** текста с *курсивом* и [ссылкой](https://example.com).

## Подзаголовок

- Пункт списка 1
- Пункт списка 2
- Пункт списка 3

### Код

\`\`\`javascript
console.log('Hello, World!');
\`\`\`

> Это цитата из текста

![Пример изображения](https://example.com/image.jpg)`,
        status: 'pending'
    }
})

const handleApprove = () => {
    console.log('Новость одобрена:', newsData.value)
    router.push('/requests')
}

const handleReject = () => {
    console.log('Новость отклонена:', newsData.value)
    router.push('/requests')
}
</script>

<template>
    <div class="news-page">
        <div class="news-container">
            <div class="btns-container">
                <button class="back-button" @click="$router.push('/requests')">
                    <span>←</span> К запросам
                </button>
                <div class="admin-controls">
                    <button class="action-button approve" @click="handleApprove">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
                        </svg>
                        Принять
                    </button>
                    <button class="action-button reject" @click="handleReject">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" fill="currentColor"/>
                        </svg>
                        Отклонить
                    </button>
                </div>
            </div>
            
            <div class="news-header">
                <h1 class="title">{{ newsData.header }}</h1>
                <div class="meta-info">
                    <span class="date">{{ newsData.date }}</span>
                    <span class="date">{{ newsData.author }}</span>
                    <span class="category">{{ newsData.category }}</span>
                </div>
            </div>

            <div class="news-content markdown-body" v-html="parsedContent"></div>
        </div>
    </div>
</template>

<style scoped>
.news-page {
    min-height: 100vh;
    background: #f5f5f5;
    padding: 2rem 0;
}

.news-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 2rem;
}

.btns-container {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 2rem;
}

.admin-controls {
    display: flex;
    gap: 12px;
}

.action-button {
    padding: 10px 20px;
    border-radius: 12px;
    border: none;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.action-button.approve {
    background: #4CAF50;
    color: white;
}

.action-button.approve:hover {
    background: #43A047;
}

.action-button.reject {
    background: #FF5252;
    color: white;
}

.action-button.reject:hover {
    background: #D32F2F;
}

.back-button {
    background: none;
    border: none;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    color: #666;
    cursor: pointer;
    padding: 0;
}

.back-button:hover {
    color: #0066FF;
}

.news-header {
    margin-bottom: 2rem;
}

.title {
    font-size: 32px;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #333;
}

.meta-info {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.date {
    color: #666;
    font-size: 14px;
}

.category {
    background: rgba(0, 102, 255, 0.1);
    color: #0066FF;
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 14px;
}

@media (max-width: 767px) {
    .news-container {
        padding: 0 1rem;
    }

    .title {
        font-size: 24px;
    }

    .btns-container {
        flex-wrap: wrap;
    }

    .admin-controls {
        width: 100%;
    }

    .action-button {
        flex: 1;
    }
}
</style>

<style>
.markdown-body {
    font-size: 18px;
    line-height: 1.6;
    color: #333;
}

.markdown-body h1 {
    font-size: 2.5em;
    margin: 24px 0;
    font-weight: 600;
}

.markdown-body h2 {
    font-size: 2em;
    margin: 20px 0;
    font-weight: 600;
}

.markdown-body h3 {
    font-size: 1.5em;
    margin: 16px 0;
    font-weight: 600;
}

.markdown-body img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 24px 0;
}

.markdown-body p {
    margin: 16px 0;
}

.markdown-body a {
    color: #0066FF;
    text-decoration: none;
    transition: color 0.2s ease;
}

.markdown-body a:hover {
    color: #0052CC;
    text-decoration: underline;
}

.markdown-body strong {
    font-weight: 600;
}

.markdown-body blockquote {
    margin: 24px 0;
    padding: 16px 24px;
    border-left: 4px solid #0066FF;
    background: rgba(0, 102, 255, 0.05);
    border-radius: 4px;
    font-style: italic;
}

.markdown-body blockquote p {
    margin: 0;
}

.markdown-body ul, .markdown-body ol {
    margin: 16px 0;
    padding-left: 24px;
}

.markdown-body li {
    margin: 8px 0;
}

.markdown-body code {
    background: #f5f5f5;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9em;
}

.markdown-body pre {
    background: #f5f5f5;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 16px 0;
}

.markdown-body pre code {
    background: none;
    padding: 0;
    font-size: 14px;
    line-height: 1.5;
}

.markdown-body table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
}

.markdown-body table th,
.markdown-body table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

.markdown-body table th {
    background: #f5f5f5;
    font-weight: 600;
}

.markdown-body hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 32px 0;
}

@media (max-width: 767px) {
    .markdown-body {
        font-size: 16px;
    }

    .markdown-body h1 {
        font-size: 2em;
    }

    .markdown-body h2 {
        font-size: 1.5em;
    }

    .markdown-body h3 {
        font-size: 1.25em;
    }

    .markdown-body blockquote {
        padding: 12px 16px;
        margin: 16px 0;
    }

    .markdown-body pre {
        padding: 12px;
    }

    .markdown-body table th,
    .markdown-body table td {
        padding: 8px;
    }
}
</style> 