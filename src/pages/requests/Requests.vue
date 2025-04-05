<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import RequestCard from '@/components/RequestCard.vue'

const router = useRouter()
const isAdmin = localStorage.getItem('isAdmin')

// Временные данные для демонстрации
const pendingNews = ref([
  {
    id: 1,
    header: "Название новости",
    description: "Описание новости, очень длинное описание новости",
    date: "04.02.2025",
    category: "Категория",
    status: 'pending'
  },
  {
    id: 2,
    header: "Название новости",
    description: "Описание новости, очень длинное описание новости",
    date: "04.02.2025",
    category: "Категория",
    status: 'pending'
  }
])

const handleApprove = (newsData) => {
  console.log('Новость одобрена:', newsData)
  pendingNews.value = pendingNews.value.filter(news => news.id !== newsData.id)
}

const handleReject = (newsData) => {
  console.log('Новость отклонена:', newsData)
  pendingNews.value = pendingNews.value.filter(news => news.id !== newsData.id)
}
</script>

<template>
  <div class="requests-page">
    <div class="requests-container">
      <div class="header">
        <button class="back-button" @click="$router.push('/')">
          <span>←</span> Назад
        </button>
        <h1>Запросы</h1>
      </div>

      <div v-if="pendingNews.length > 0" class="news-grid">
        <RequestCard
          v-for="news in pendingNews"
          :key="news.id"
          v-bind="news"
          @approve="handleApprove"
          @reject="handleReject"
        />
      </div>
      <div v-else class="empty-state">
        <h2>Нет активных запросов</h2>
        <p>Здесь будут отображаться запросы на публикацию новостей</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.requests-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.requests-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.header {
  display: flex;
  
  flex-direction: column;
  gap: 20px;
  margin-bottom: 32px;
}

.header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin: 0;
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

.news-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.empty-state svg {
  margin-bottom: 24px;
  color: #666;
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.empty-state p {
  font-size: 16px;
  color: #666;
  margin: 0;
  max-width: 300px;
}

@media (max-width: 767px) {
  .requests-container {
    padding: 0 1rem;
  }

  .header h1 {
    font-size: 24px;
  }

  .empty-state {
    padding: 48px 16px;
  }

  .empty-state h2 {
    font-size: 20px;
  }

  .empty-state p {
    font-size: 14px;
  }
}
</style>