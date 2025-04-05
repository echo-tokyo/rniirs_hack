import { defineStore } from 'pinia'

export const useNewsDataStore = defineStore('counter', {
  state: () => {
    return { news: null }
  },
  actions: {
    updateNews(newNews) {
      this.news = newNews
    },
  },
})

export const useCategoriesStore = defineStore('categories', {
  state: () => {
    // Получаем сохраненные категории из localStorage или используем значения по умолчанию
    const savedCategories = localStorage.getItem('newsCategories')
    return {
      categories: savedCategories ? JSON.parse(savedCategories) : {
        category: null,
        city: null,
        sort: null,
      }
    }
  },
  actions: {
    updateCategories(newCategories) {
      this.categories = newCategories
      // Сохраняем в localStorage при каждом обновлении
      localStorage.setItem('newsCategories', JSON.stringify(newCategories))
    },
  },
})
