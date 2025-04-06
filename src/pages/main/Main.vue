<script setup>
import { ref, watch, computed } from 'vue'
import { CustomSelect, NewsCard } from '@/components'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Modal from '@/components/Modal.vue'
import CreateNewsForm from '@/components/CreateNewsForm.vue'
import { testData } from './testData'
import { testCategories } from './testCategories'
import { useNewsDataStore, useCategoriesStore } from '@/app/store/store'
import { testFavoriteData } from './testFavoriteData'
import axios from 'axios'
import { decodeJWT } from '@/utils/jwt'

const data = useNewsDataStore()
const categories = useCategoriesStore()
const router = useRouter()
const isAdmin = ref(false)

const currentPage = ref(1)
const totalPages = ref(1)
const isLoading = ref(false)

const selectOptions = computed(() => categories.categoriesList.map(category => category.title))
const selectedCategory = ref(categories.categories.category || '')
const selectedCity = ref(categories.categories.city || '')
const selectedSort = ref(categories.categories.sort || '')

const cityOptions = ['РНФЦ', 'наука.рф', 'Пользователи']
const sortOptions = ['Новые', 'Старые']

const API_URL = 'http://109.73.194.154:81/api/news/short/'
const CATEGORIES_URL = 'http://109.73.194.154:81/api/categories/'

// Добавим функцию для определения источника новости
const getNewsSource = (authorLogin) => {
  if (authorLogin === 'РНФЦ' || authorLogin === 'наука.рф') {
    return authorLogin
  }
  return 'Пользователи'
}

// фильтрация новостей
const filteredNews = computed(() => {
  if (!data.news || !Array.isArray(data.news)) {
    return []
  }

  let result = [...data.news]
  console.log('Состояние новостей перед фильтрацией:', result.map(item => ({
    id: item.id,
    title: item.title
  })))

  if (selectedCategory.value) {
    result = result.filter((news) => news?.category?.title === selectedCategory.value)
  } 

  // Если после фильтрации по категории нет результатов, сбрасываем фильтр по источнику
  if (result.length === 0 && selectedCity.value) {
    selectedCity.value = ''
    return data.news
  }

  if (selectedCity.value) {
    result = result.filter((news) => getNewsSource(news?.author.login) === selectedCity.value)
  }

  if (selectedSort.value === 'Новые') {
    result.sort((a, b) => {
      const dateA = new Date(a?.date || 0)
      const dateB = new Date(b?.date || 0)
      return dateB - dateA
    })
  } else if (selectedSort.value === 'Старые') {
    result.sort((a, b) => {
      const dateA = new Date(a?.date || 0)
      const dateB = new Date(b?.date || 0)
      return dateA - dateB
    })
  }

  return result
})

// отслеживание изменения селектов
watch([selectedCategory, selectedCity, selectedSort], ([category, city, sort]) => {
  console.log({
    Категория: category || null,
    Источник: city || null,
    Сортировка: sort || null,
  })
  categories.updateCategories({
    category: category || null,
    city: city || null,
    sort: sort || null,
  })
})

// загрузка ресурсов
const fetchData = async (page = 1) => {
  const token = localStorage.getItem('access')
  if (!token) {
    router.push({ name: 'signin' })
    return
  }

  try {
    isLoading.value = true
    // Проверяем валидность токена
    await axios.post("http://109.73.194.154:81/api/token/verify/", {
      token: token
    })
    
    // Получаем новости с API с учетом страницы
    const newsResponse = await axios.get(`${API_URL}?page=${page}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('Полученные данные с сервера:', newsResponse.data.results.map(item => ({
      id: item.id,
      title: item.title,
      liked: item.liked
    })))
    
    // Обновляем новости и информацию о пагинации
    data.updateNews(newsResponse.data.results)
    totalPages.value = Math.ceil(newsResponse.data.count / 10)
    currentPage.value = page
    
    // Проверяем, есть ли категории в store
    if (categories.categoriesList.length === 0) {
      const categoriesResponse = await axios.get(CATEGORIES_URL, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      categories.updateCategoriesList(categoriesResponse.data)
    }
    
  } catch (error) {
    console.error('Ошибка при получении данных:', error)
    if (error.response?.status === 401) {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      router.push({ name: 'signin' })
    }
  } finally {
    isLoading.value = false
  }
}

const handlePageChange = (newPage) => {
  if (newPage >= 1 && newPage <= totalPages.value && newPage !== currentPage.value) {
    window.scrollTo(0, 0)
    fetchData(newPage)
  }
}

const isModalOpen = ref(false)

const handleCreateNews = async () => {
  isModalOpen.value = false
  // Обновляем список новостей после создания
  await fetchData(currentPage.value)
}

const handleCloseModal = () => {
  isModalOpen.value = false
}

// Проверяем isAdmin при монтировании компонента
onMounted(() => {
  const token = localStorage.getItem('access')
  if (token) {
    const decodedToken = decodeJWT(token)
    isAdmin.value = decodedToken?.is_superuser || false
  }
  fetchData(1)
})
</script>

<template>
  <div class="app">
    <div class="container">
      <div class="filters-container">
        <div class="selects-container">
          <CustomSelect
            v-model="selectedCategory"
            :options="selectOptions"
            placeholder="Выберите категорию"
          />
          <CustomSelect
            v-model="selectedCity"
            :options="cityOptions"
            placeholder="Искать из источника"
          />
          <CustomSelect
            v-model="selectedSort"
            :options="sortOptions"
            placeholder="Сортировать по дате"
          />
        </div>
      </div>
      <button v-if="isAdmin" class="requests-button" @click="router.push('/requests')">
        Запросы
      </button>
      <button class="create-button" @click="isModalOpen = true">Создать новость</button>
    </div>
  </div>
  <div class="NewsContainer">
    <div v-if="filteredNews.length == 0" class="no-news-message">
      Упс! Новости по вашим параметрам не найдены, показаны по схожей тематике
    </div>
    <template v-if="filteredNews.length > 0">
      <NewsCard
        v-for="item in filteredNews"
        :key="item.id"
        :id="item.id"
        :header="item.title"
        :description="item.description"
        :date="item.date"
        :category="item.category?.title"
      />
    </template>

    <!-- Pagination controls -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        class="pagination-button" 
        :disabled="currentPage === 1"
        @click="handlePageChange(currentPage - 1)"
      >
        ←
      </button>
      <div class="pagination-info">
        {{ currentPage }} из {{ totalPages }}
      </div>
      <button 
        class="pagination-button" 
        :disabled="currentPage === totalPages"
        @click="handlePageChange(currentPage + 1)"
      >
        →
      </button>
    </div>
  </div>

  <Modal :is-open="isModalOpen" @close="handleCloseModal">
    <CreateNewsForm @close="handleCreateNews" />
  </Modal>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.no-news-message {
  display: flex;
  justify-content: center;
  color: #676767;
}
.filters-container {
  display: flex;
  gap: 20px;
  width: 100%;
}

.selects-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  width: 100%;
}

.selects-container > * {
  flex: 1;
  min-width: 200px; /* Минимальная ширина для селектов */
}

.create-button,
.requests-button {
  height: 65px;
  border: none;
  border-radius: 20px;
  background: #0066ff;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  width: 100%;
}

.requests-button {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  background-color: white;
  color: #161616;
}

.create-button:hover {
  background: #0052cc;
}

.NewsContainer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

@media (min-width: 768px) {
  .selects-container {
    gap: 30px;
  }
}

@media (max-width: 767px) {
  .container {
    padding: 1rem;
  }

  .NewsContainer {
    padding: 0 1rem;
  }

  .filters-container {
    flex-direction: column;
  }

  .selects-container {
    flex-direction: column;
    align-items: stretch;
  }

  .selects-container > * {
    width: 100%;
  }

  .favorite-button {
    display: none;
  }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
  padding-bottom: 30px;
}

.pagination-button {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 12px;
  background: white;
  color: #333;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
}

.pagination-button:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
  box-shadow: none;
}

.pagination-button:not(:disabled):hover {
  background: #f5f5f5;
}

.pagination-info {
  font-size: 16px;
  color: #666;
}

/* Loading state */
.NewsContainer {
  position: relative;
  min-height: 200px;
}

.NewsContainer.loading {
  opacity: 0.7;
  pointer-events: none;
}

@media (max-width: 767px) {
  .pagination {
    gap: 10px;
  }

  .pagination-button {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }
}
</style>
