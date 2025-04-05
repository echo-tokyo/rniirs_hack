<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Выберите категорию'
  }
})

const isOpen = ref(false)
const selectedOption = ref(props.placeholder)
const selectRef = ref(null)

const handleClickOutside = (event) => {
  if (selectRef.value && !selectRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const selectOption = (option) => {
  selectedOption.value = option
  isOpen.value = false
}

const toggleSelect = (event) => {
  event.stopPropagation()
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div class="custom-select" ref="selectRef" @click="toggleSelect">
    <div class="select-header">
      <span>{{ selectedOption }}</span>
      <svg 
        class="arrow"
        :class="{ 'arrow-up': isOpen }"
        width="24" 
        height="24" 
        viewBox="0 0 24 24" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    <div v-if="isOpen" class="select-options">
      <div 
        v-for="option in options" 
        :key="option"
        class="option"
        @click="selectOption(option)"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-select {
  position: relative;
  width: 100%;
  min-width: 150px;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

.select-header {
  height: 65px;
  background: white;
  border-radius: 20px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.arrow {
  transition: transform 0.2s ease;
  color: #666;
}

.arrow-up {
  transform: rotate(180deg);
}

.select-options {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 100%;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  z-index: 10;
  padding: 12px 0;
  max-height: 300px;
  overflow-y: auto;
}

.option {
  padding: 12px 20px;
  transition: background-color 0.2s ease;
}

.option:hover {
  background-color: #f5f5f5;
}

/* Стилизация скроллбара */
.select-options::-webkit-scrollbar {
  width: 4px;
  margin-right: 4px;
}

.select-options::-webkit-scrollbar-track {
  background: transparent;
}

.select-options::-webkit-scrollbar-thumb {
  background: #0066FF;
  border-radius: 2px;
}
</style> 