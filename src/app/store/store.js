import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://109.73.194.154:81/api'

export const useNewsDataStore = defineStore('counter', {
  state: () => {
    return { 
      news: null
    }
  },
  actions: {
    updateNews(newNews) {
      this.news = newNews
    },

    // Получение случайных новостей
    getRandomNews(count = 3) {
      if (!this.news || !Array.isArray(this.news) || this.news.length === 0) {
        console.log('Нет доступных новостей')
        return []
      }
      
      const shuffled = [...this.news].sort(() => 0.5 - Math.random())
      const selected = shuffled.slice(0, count)
      return selected
    }
  },
})

export const useCategoriesStore = defineStore('categories', {
  state: () => {
    // Получаем сохраненные категории из localStorage или используем значения по умолчанию
    const savedCategories = localStorage.getItem('newsCategories')
    const savedCategoriesList = localStorage.getItem('categoriesList')
    return {
      categories: savedCategories ? JSON.parse(savedCategories) : {
        category: null,
        city: null,
        sort: null,
      },
      categoriesList: savedCategoriesList ? JSON.parse(savedCategoriesList) : []
    }
  },
  actions: {
    updateCategories(newCategories) {
      this.categories = newCategories
      // Сохраняем в localStorage при каждом обновлении
      localStorage.setItem('newsCategories', JSON.stringify(newCategories))
    },
    updateCategoriesList(newCategoriesList) {
      this.categoriesList = newCategoriesList
      // Сохраняем список категорий в localStorage
      localStorage.setItem('categoriesList', JSON.stringify(newCategoriesList))
    },
  },
})
