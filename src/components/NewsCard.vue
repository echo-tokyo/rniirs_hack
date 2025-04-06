<script setup>
import { ref, computed } from 'vue'
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
  }
})

const cleanDescription = computed(() => {
  if (!props.description) return ''
  return props.description
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/\`(.*?)\`/g, '$1')
    .replace(/\#{1,6}\s/g, '')
    .replace(/\n\-\s/g, '\n')
    .replace(/\n\d\.\s/g, '\n')
    .replace(/!\[(.*?)\]\(.*?\)/g, '')
    .replace(/!image/g, '')
    + '...'
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
  font-size: 16px;
  font-weight: 600;
  width: 70%;
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
