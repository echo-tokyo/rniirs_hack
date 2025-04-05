<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

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
    content: '', // Полный текст статьи
    status: 'pending'
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
        content: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.`,
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

            <div class="news-content">
                <p class="description">{{ newsData.description }}</p>
                <div class="content">
                    <p v-for="(paragraph, index) in newsData.content.split('\n\n')" 
                       :key="index">{{ paragraph }}</p>
                </div>
            </div>
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

.news-content {
    font-size: 18px;
    line-height: 1.6;
    color: #333;
}

.description {
    font-size: 20px;
    color: #666;
    margin-bottom: 24px;
}

.content p {
    margin-bottom: 16px;
}

@media (max-width: 767px) {
    .news-container {
        padding: 0 1rem;
    }

    .title {
        font-size: 24px;
    }

    .news-content {
        font-size: 16px;
    }

    .description {
        font-size: 18px;
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