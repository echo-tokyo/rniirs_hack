<template>
  <div class="item">
    <form action="" @submit.prevent='handleSubmit()'> 
      <h1>Вход</h1>
      <input 
        type="text" 
        placeholder='Логин' 
        v-model='loginValue'
      >
      <input 
        type="password" 
        placeholder='Пароль' 
        v-model='passValue'
      >
      <input type="submit" value='Войти'>
    </form>
    <p>Еще нет аккаунта ? <span class='form-span' @click='routing()'>Зарегистрируйтесь</span></p>

    <!-- Попап с ошибкой -->
    <Transition name="slide-fade">
      <div v-if="errorMessage" class="error-popup">
        {{ errorMessage }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginValue = ref('')
const passValue = ref('')
const errorMessage = ref('')
let errorTimeout = null

const showError = (message) => {
  errorMessage.value = message
  // Очищаем предыдущий таймер если он есть
  if (errorTimeout) clearTimeout(errorTimeout)
  // Устанавливаем новый таймер на скрытие ошибки
  errorTimeout = setTimeout(() => {
    errorMessage.value = ''
  }, 3000)
}

const validateForm = () => {
  if (!loginValue.value) {
    showError('Введите логин')
    return false
  }
  if (loginValue.value.length < 3) {
    showError('Логин должен быть не менее 3 символов')
    return false
  }
  if (!passValue.value) {
    showError('Введите пароль')
    return false
  }
  if (passValue.value.length < 6) {
    showError('Пароль должен быть не менее 6 символов')
    return false
  }
  return true
}

const handleSubmit = (e) => {
  if (e && e.preventDefault) {
    e.preventDefault()
  }
  
  if (validateForm()) {
    localStorage.setItem('token', 'token')
    router.push({ name: 'main' })
  }
}

const routing = () => {
  router.push({ name: 'signup' })
}
</script>

<style lang="scss" scoped>
.item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
  gap: 20px;
  form{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px
  }
}

.error-popup {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #0066FF;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.2);
  z-index: 1000;
}

// Анимации
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-50%) translateY(20px);
  opacity: 0;
}
</style>