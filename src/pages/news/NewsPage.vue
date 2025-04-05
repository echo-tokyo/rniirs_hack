<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { testData } from '../main/testData'
import html2pdf from 'html2pdf.js'

const isAdmin = localStorage.getItem('isAdmin')
const route = useRoute()
const router = useRouter()
const id = route.params.id
const newsData = ref({})
const isLoaded = ref(false)
const contentRef = ref(null)
const isPdfButtonVisible = ref(true)
const isBackButtonVisible = ref(true)
const increaseMargin = ref(false)

// Настраиваем marked для обработки ссылок и изображений
marked.use({
  gfm: true,
  breaks: true,
  mangle: false,
  headerIds: false
})

// Создаем вычисляемое свойство для преобразованного HTML
const parsedContent = computed(() => {
  if (!newsData.value.description) return ''
  const html = marked(newsData.value.description)
  return DOMPurify.sanitize(html)
})

onMounted(() => {
  window.scrollTo(0,0)
  // получили данные по id
  newsData.value = testData[0]
  isLoaded.value = true
})

const handleApprove = () => {
  // Здесь будет логика одобрения новости
  console.log('Новость одобрена')
  router.push('/requests')
}

const handleReject = () => {
  // Здесь будет логика отклонения новости
  console.log('Новость отклонена')
  router.push('/requests')
}

const newsDelete = () => {
  router.push({name: 'main'})
}

const handleBack = () => {
  // Скрываем кнопку на некоторое время
  isBackButtonVisible.value = false
  setTimeout(() => {
    isBackButtonVisible.value = true
  }, 2000) // Показать кнопку снова через 2 секунды
  
  // Возвращаемся назад
  router.back()
}

const exportToPdf = () => {
  // Скрываем обе кнопки на некоторое время
  isPdfButtonVisible.value = false
  isBackButtonVisible.value = false
  
  // Увеличиваем margin-top на 80px
  increaseMargin.value = true
  
  setTimeout(() => {
    isPdfButtonVisible.value = true
    isBackButtonVisible.value = true
    increaseMargin.value = false
  }, 3000) // Показать кнопки снова через 3 секунды
  
  const content = contentRef.value
  const filename = `${newsData.value.title || 'news'}.pdf`
  
  const options = {
    margin: 10,
    filename: filename,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }
  
  html2pdf().from(content).set(options).save()
}
</script>

<template>
  <div v-if='isLoaded' class="news-page">
    <div class="news-container" ref="contentRef" :class="{ 'increased-margin': increaseMargin }">
      <div class="btns-container no-print">
        <button v-if="isBackButtonVisible" class="back-button" @click="handleBack">
          <span>←</span> Назад
        </button>
        <div v-if="isAdmin && newsData.status === 'pending'" class="admin-controls">
          <button class="action-button approve" @click="handleApprove">
            Принять
          </button>
          <button class="action-button reject" @click="handleReject">
            Отклонить
          </button>
        </div>
        <button v-if="isPdfButtonVisible" class="pdf-button" @click="exportToPdf">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" fill="currentColor"/>
          </svg>
          Скачать PDF
        </button>
      </div>
      
      <div class="news-header no-print">
        <h1 class="title">{{ newsData.title }}</h1>
        <div class="meta-info">
          <span class="date">{{ newsData.date }}</span>
          <span class="date">{{ newsData.author.login }}</span>
          <span class="category">{{ newsData.category.title }}</span>
        </div>
      </div>

      <div class="news-content markdown-body" v-html="parsedContent"></div>
    </div>

    <button v-if='!isAdmin' class="delete-button no-print" @click="newsDelete">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
      </svg>
      Удалить
    </button>
  </div>
</template>

<style>
img{
  width: 40vw;
}
.news-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.news-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  transition: margin-top 0.3s ease;
}

.increased-margin {
  margin-top: 40px !important;
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
}

.pdf-button {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  background: #1E88E5;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pdf-button:hover {
  background: #1565C0;
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

.delete-button {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  border: 1px solid #FF5252;
  background: white;
  color: #FF5252;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 100;
}

.delete-button:hover {
  background: rgba(255, 82, 82, 0.1);
  transform: translateY(-2px);
}

.delete-button:active {
  transform: translateY(0);
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

@media print {
  .no-print {
    display: none !important;
  }
  
  .news-page {
    background: white;
    padding: 0;
  }
  
  .news-container {
    padding: 0;
  }
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
  
  .pdf-button {
    width: 100%;
    margin-left: 0;
    justify-content: center;
    order: 3;
  }

  .delete-button {
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
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