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

const data = useNewsDataStore()
const categories = useCategoriesStore()
const router = useRouter()
const isAdmin = localStorage.getItem('isAdmin')

const isFavorite = ref(false)
const selectOptions = computed(() => categories.categoriesList.map(category => category.title))
const selectedCategory = ref(categories.categories.category || '')
const selectedCity = ref(categories.categories.city || '')
const selectedSort = ref(categories.categories.sort || '')

const cityOptions = ['РНФЦ', 'наука.рф', 'Пользователи']
const sortOptions = ['Новые', 'Старые']

const API_URL = 'http://109.73.194.154:81/api/news/'
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

  // Если активен режим избранного, показываем только избранные новости
  if (isFavorite.value) {
    return data.getFavoriteNews()
  }

  let result = [...data.news]

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
const fetchData = async () => {
  const token = localStorage.getItem('access')
  if (!token) {
    router.push({ name: 'signin' })
    return
  }

  try {
    // Проверяем валидность токена
    await axios.post("http://109.73.194.154:81/api/token/verify/", {
      token: token
    })
    
    // Получаем новости с API
    const newsResponse = await axios.get(API_URL, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    // Обновляем новости
    data.updateNews(newsResponse.data.results)
    
    // Выводим 3 случайные новости
    data.getRandomNews()
    
    // Проверяем, есть ли категории в store
    if (categories.categoriesList.length === 0) {
      // Если категорий нет, загружаем их с API
      const categoriesResponse = await axios.get(CATEGORIES_URL, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      console.log('Загружены новые категории:', categoriesResponse.data)
      categories.updateCategoriesList(categoriesResponse.data)
    } else {
      console.log('Используются кэшированные категории:', categories.categoriesList)
    }
    
  } catch (error) {
    console.error('Ошибка при получении данных:', error)
    if (error.response?.status === 401) {
      // Если токен невалидный, удаляем его и редиректим на страницу входа
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      router.push({ name: 'signin' })
    }
  }
}

const isModalOpen = ref(false)

const handleCreateNews = (newsData) => {
  console.log('Создана новость:', newsData)
  isModalOpen.value = false
}

const getFavorite = () => {
  isFavorite.value = !isFavorite.value
}

onMounted(fetchData)
</script>

<template>
  <div class="app">
    <div class="container">
      <div class="filters-container">
        <button class="favorite-button" :class="{ 'active': isFavorite }" @click="getFavorite()">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
              fill="currentColor"
            />
          </svg>
        </button>
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
      <button v-if="!isAdmin" class="requests-button" @click="router.push('/requests')">
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
        :is_liked="item.is_liked"
      />
    </template>
  </div>

  <Modal :is-open="isModalOpen" @close="isModalOpen = false">
    <CreateNewsForm @submit="handleCreateNews" />
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

.favorite-button {
  width: 65px;
  height: 65px;
  border: none;
  border-radius: 20px;
  background: white;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  flex-shrink: 0;
}

.favorite-button:hover {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
}

.favorite-button.active {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.15);
  transform: scale(1.05);
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
    width: 100%;
  }
}
</style>
