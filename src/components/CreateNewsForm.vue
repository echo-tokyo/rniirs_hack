<script setup>
import { ref, onMounted } from 'vue'
import { CustomSelect } from '@/components'
import axios from 'axios'
import { decodeJWT } from '@/utils/jwt'

const title = ref('')
const content = ref('')
const selectedCategory = ref('')
const categories = ref([])
const error = ref(null)

const emit = defineEmits(['submit', 'close'])

const API_URL = 'http://109.73.194.154:81/api'

// Загрузка категорий
const loadCategories = async () => {
  try {
    const token = localStorage.getItem('access')
    if (!token) return

    const response = await axios.get(`${API_URL}/categories/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    categories.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error)
  }
}

const handleSubmit = async () => {
  try {
    const token = localStorage.getItem('access')
    if (!token) {
      error.value = 'Необходима авторизация'
      return
    }

    const decodedToken = decodeJWT(token)
    const userId = decodedToken?.user_id

    if (!userId) {
      error.value = 'Не удалось определить пользователя'
      return
    }

    if (!title.value || !content.value || !selectedCategory.value) {
      error.value = 'Заполните все поля'
      return
    }

    const selectedCategoryId = categories.value.find(cat => cat.title === selectedCategory.value)?.id

    if (!selectedCategoryId) {
      error.value = 'Выберите категорию'
      return
    }

    const response = await axios.post(`${API_URL}/news/`, {
      title: title.value,
      description: content.value,
      category_id: selectedCategoryId,
      author_id: userId,
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    console.log('Новость успешно создана:', response.data)
    
    // Очищаем форму
    title.value = ''
    content.value = ''
    selectedCategory.value = ''
    error.value = null
    
    // Закрываем модальное окно
    emit('close')
  } catch (err) {
    console.error('Ошибка при создании новости:', err)
    error.value = 'Ошибка при создании новости'
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <form @submit.prevent="handleSubmit" class="create-news-form">
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div class="form-group">
      <input
        v-model="title"
        type="text"
        placeholder="Название новости"
        class="form-input"
      />
    </div>
    <div class="form-group">
      <CustomSelect
        v-model="selectedCategory"
        :options="categories.map(cat => cat.title)"
        placeholder="Выберите категорию"
        class="category-select"
      />
    </div>
    <div class="form-group">
      <textarea
        v-model="content"
        placeholder="Текст новости"
        class="form-textarea"
        rows="6"
      ></textarea>
    </div>
    <button type="submit" class="submit-button">
      Отправить на проверку
    </button>
  </form>
</template>

<style scoped>
.create-news-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-input,
.form-textarea {
  font-family: 'Montseratt', sans-serif;
  width: 100%;
  padding: 16px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  font-size: 20px;
  transition: border-color 0.2s ease;
  outline: none;
  resize: none;
}

.form-textarea {
  min-height: 200px;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #0066FF;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #999;
}

.category-select {
  width: 100%;
}

.submit-button {
  background: #0066FF;
  color: white;
  border: none;
  border-radius: 16px;
  padding: 20px;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-button:hover {
  background: #0052cc;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}
</style> 