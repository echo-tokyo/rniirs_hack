<script setup>
import { ref, watch } from 'vue'
import { CustomSelect, NewsCard } from "@/components"
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Modal from '@/components/Modal.vue'
import CreateNewsForm from '@/components/CreateNewsForm.vue'
import { testData } from './testData'
import { testCategories } from './testCategories'
import { useNewsDataStore } from '@/app/store/store'

const data = useNewsDataStore()
const router = useRouter()
const isAdmin = localStorage.getItem('isAdmin')

const selectOptions = ref([])
const selectedCategory = ref('')
const selectedCity = ref('')
const selectedSort = ref('')

const cityOptions = [
  'Москва',
  'Санкт-Петербург',
  'Новосибирск',
  'Екатеринбург',
  'Казань',
  'Нижний Новгород'
]

const sortOptions = [
  'По популярности',
  'По возрастанию цены',
  'По убыванию цены',
  'По рейтингу',
  'По отзывам'
]

// Следим за изменениями всех селектов
watch([selectedCategory, selectedCity, selectedSort], ([category, city, sort]) => {
  console.log({
    Категория: category || 'Не выбрано',
    Источник: city || 'Не выбрано',
    Сортировка: sort || 'Не выбрано'
  })
})

onMounted(() => {
  if(!localStorage.getItem('token')){
    router.push({name: 'signin'})
  }

  // получили данные после запроса (testData это response). сохранить в стейт менеджер
  data.updateNews(testData)
  // получили категории после запроса
  selectOptions.value = testCategories.map(el => el.data)
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
      <button v-if='!isAdmin' class="requests-button" @click='router.push("/requests")'>Запросы</button>
      <button class="create-button" @click="isModalOpen = true">
        Создать новость
      </button>
    </div>
  </div>
  <div class="NewsContainer">
    <NewsCard v-for='item in data.news'
    :key='item.id'
    :id='item.id'
    :header='item.title'
    :description='item.description'
    :date='item.date'
    :category='item.category.title'
    :is_liked='item.is_liked'
    @update:is_liked="item.is_liked = $event"
    />
  </div>
  
  <Modal 
    :is-open="isModalOpen"
    @close="isModalOpen = false"
  >
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

.create-button, .requests-button {
  height: 65px;
  border: none;
  border-radius: 20px;
  background: #0066FF;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  width: 100%;
}
.requests-button{
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
