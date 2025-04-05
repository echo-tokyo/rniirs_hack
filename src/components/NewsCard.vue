<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useNewsDataStore } from '@/app/store/store'

const store = useNewsDataStore()

const props = defineProps({
  header: String,
  description: String,
  date: String,
  category: String,
  id: {
    type: [String, Number],
    required: true,
  },
  is_liked: Boolean,
})

const isFavorite = ref(props.is_liked)

onMounted(() => {
  // Проверяем, есть ли id в избранном при монтировании
  isFavorite.value = store.favorites.includes(props.id)
})

watch(
  () => props.is_liked,
  (newVal) => {
    isFavorite.value = newVal
  }
)

watch(
  () => store.favorites,
  () => {
    // Обновляем состояние при изменении favorites в store
    isFavorite.value = store.favorites.includes(props.id)
  }
)

const toggleFavorite = () => {
  // Вызываем метод toggleFavorite из стора
  store.toggleFavorite(props.id)
  isFavorite.value = store.favorites.includes(props.id)
}

const cleanDescription = computed(() => {
  if (!props.description) return ''
  return props.description
    .replace(/\*\*(.*?)\*\*/g, '$1') // Убираем жирный текст **
    .replace(/\*(.*?)\*/g, '$1') // Убираем курсив *
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Убираем ссылки [text](url)
    .replace(/\`(.*?)\`/g, '$1') // Убираем инлайн код
    .replace(/\#{1,6}\s/g, '') // Убираем заголовки #
    .replace(/\n\-\s/g, '\n') // Убираем маркеры списка
    .replace(/\n\d\.\s/g, '\n') // Убираем нумерованные списки
    .replace(/!\[(.*?)\]\(.*?\)/g, '') // Убираем картинки ![alt](url)
    .replace(/!image/g, '') // Убираем !image
})
</script>
<template>
  <div class="NewsCard-container" @click="$router.push(`/news/${props.id}`)">
    <div class="NewsCard-information">
      <div class="News-information__text">
        <h2 class="NewsCard-information__header">{{ props.header }}</h2>
        <h2 class="NewsCard-information__description">{{ cleanDescription }}</h2>
      </div>

      <div class="NewsCard-bottom">
        <h2 class="NewsCard-information__date">{{ props.date }}</h2>
        <button
          class="heart-button"
          :class="{ 'is-favorite': isFavorite }"
          @click.stop="toggleFavorite"
        >
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
      </div>
    </div>
    <div class="NewsCard-category">
      <h2 class="NewsCard-category__category">{{ props.category }}</h2>
    </div>
  </div>
</template>

<style scoped>
.NewsCard-container {
  background: #ffffff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 180px;
  display: flex;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.NewsCard-container:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.NewsCard-information {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
  overflow: hidden;
  height: 100%;
}

.News-information__text {
  flex: 1;
  overflow: hidden;
}

.NewsCard-information__header {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
}

.NewsCard-information__description {
  font-size: 14px;
  color: #666;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.NewsCard-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.NewsCard-information__date {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.heart-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border-radius: 50%;
}

.heart-button:hover {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
}

.heart-button.is-favorite {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
}

.heart-button.is-favorite:hover {
  background: rgba(255, 71, 87, 0.2);
}

.NewsCard-category {
  position: absolute;
  top: 20px;
  right: 20px;
}

.NewsCard-category__category {
  font-size: 14px;
  color: #0066ff;
  margin: 0;
  background: rgba(0, 102, 255, 0.1);
  padding: 6px 12px;
  border-radius: 10px;
}

@media (max-width: 767px) {
  .NewsCard-container {
    height: auto;
    min-height: 180px;
  }

  .NewsCard-category {
    position: static;
    margin-top: 10px;
  }

  .NewsCard-information {
    margin-right: 0;
  }
}
</style>
