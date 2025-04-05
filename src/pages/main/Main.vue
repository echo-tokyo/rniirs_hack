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

const data = useNewsDataStore()
const categories = useCategoriesStore()
const router = useRouter()
const isAdmin = localStorage.getItem('isAdmin')

const selectOptions = ref([])
const selectedCategory = ref(categories.categories.category || '')
const selectedCity = ref(categories.categories.city || '')
const selectedSort = ref(categories.categories.sort || '')

const cityOptions = ['РНФ', 'Наука.рф']
const sortOptions = ['Новые', 'Старые']

// фильтрация новостей
const filteredNews = computed(() => {
  if (!data.news || !Array.isArray(data.news)) {
    return []
  }

  let result = [...data.news]

  if (selectedCategory.value) {
    result = result.filter((news) => news?.category?.title === selectedCategory.value)
  }

  if (selectedCity.value) {
    result = result.filter((news) => news?.author.login === selectedCity.value)
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
onMounted(() => {
  if (!localStorage.getItem('token')) {
    router.push({ name: 'signin' })
  }

  // после получения ресурсов
  data.updateNews(testData)
  // после получения категорий
  selectOptions.value = testCategories.map((el) => el?.data)
})

const isModalOpen = ref(false)

const handleCreateNews = (newsData) => {
  console.log('Создана новость:', newsData)
  isModalOpen.value = false
}
</script>

<template>
  <div class="app">
    <div class="container">
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
      <button v-if="!isAdmin" class="requests-button" @click="router.push('/requests')">
        Запросы
      </button>
      <button class="create-button" @click="isModalOpen = true">Создать новость</button>
    </div>
  </div>
  <div class="NewsContainer">
    <div v-if="filteredNews.length == 0" class="no-news-message">Упс! Новости по вашим параметрам не найдены, показаны по схожей тематике</div>
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
        @update:is_liked="item.is_liked = $event"
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

.no-news-message{
  display: flex;
  justify-content: center;
  color: #676767;
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

  .selects-container {
    flex-direction: column;
    align-items: stretch;
  }

  .selects-container > * {
    width: 100%;
  }
}
</style>
