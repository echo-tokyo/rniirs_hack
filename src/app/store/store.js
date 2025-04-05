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