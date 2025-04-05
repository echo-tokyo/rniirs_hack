<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const isAdmin = localStorage.getItem('isAdmin')
const route = useRoute()
const router = useRouter()
const newsData = ref({
  header: '',
  description: '',
  date: '',
  category: ''
})

onMounted(() => {
  const mockData = {
    1: {
      header: "НОУ ВЭЙ, ЧИКИПИКИ",
      description: "АЛИНЫ ЧИКИ ПИКИ ГЕТ ДИС ВОРЛД АУТ, НО ВЭЙ ВАТАКАК СМОТРИТЕ",
      date: "03.05.2024",
      category: "Спортивный интерес",
      author: "ФНР"
    }
  }
  
  const id = route.params.id // Use route here
  if (mockData[id]) {
    newsData.value = mockData[id]
  }
})

const newsDelete = () => {
  router.push({name: 'main'}) // Now this will work
}
</script>
<template>
  <div class="news-page">
    <div class="news-container">
      <div class="btns-container">
        <button class="back-button" @click="$router.back()">
          <span>←</span> Назад
        </button>
        <button v-if='isAdmin' class="delete-button" @click="newsDelete()">
          Удалить
        </button>
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
        <p>{{ newsData.description }}</p>
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

.btns-container{
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 2rem;
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
}
</style> 