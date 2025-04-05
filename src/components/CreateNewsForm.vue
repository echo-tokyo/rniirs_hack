<script setup>
import { ref } from 'vue'
import { CustomSelect } from '@/components'
import { testCategories } from '@/pages/main/testCategories'

const title = ref('')
const content = ref('')
const selectedCategory = ref('')

const emit = defineEmits(['submit'])

const categoryOptions = testCategories.map(cat => cat.data)

const handleSubmit = () => {
  emit('submit', {
    title: title.value,
    content: content.value,
    category: selectedCategory.value
  })
  title.value = ''
  content.value = ''
  selectedCategory.value = ''
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="create-news-form">
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
        :options="categoryOptions"
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
</style> 