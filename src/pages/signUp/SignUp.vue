<template>
  <div class="item">
    <h1>Регистрация</h1>
    <form action="" @submit.prevent="handleSubmit"> 
      <input 
        type="text" 
        placeholder="Логин" 
        v-model="loginValue"
        :disabled="isLoading"
      >
      <input 
        type="password" 
        placeholder="Пароль" 
        v-model="passValue"
        :disabled="isLoading"
      >
      <input 
        type="submit" 
        :value="isLoading ? 'Регистрация...' : 'Зарегистрироваться'"
        :disabled="isLoading"
      >
    </form>
    <h3>Есть аккаунт ? <span class="form-span" @click="routing">Войдите</span></h3>

    <!-- Попап с ошибкой -->
    <Transition name="slide-fade">
      <div v-if="errorMessage" class="error-popup">
        {{ errorMessage }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loginValue = ref('')
const passValue = ref('')
const errorMessage = ref('')
let errorTimeout = null
const isLoading = ref(false)

const API_URL = 'http://109.73.194.154:81/api/users/'

onMounted(async () => {
  const token = localStorage.getItem('access')
  if (token) {
    try {
      const response = await axios.post("http://109.73.194.154:81/api/token/verify/", {
        token: token
      })
      
      if (response.status === 200) {
        router.push({ name: 'main' })
      }
    } catch (error) {
      // Если токен невалидный, удаляем его
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    }
  }
})

const showError = (message) => {
  errorMessage.value = message
  if (errorTimeout) clearTimeout(errorTimeout)
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

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  try {
    const response = await axios.post(API_URL, {
      login: loginValue.value,
      password: passValue.value
    })

    if (response.status === 201 || response.status === 200) {
      // После успешной регистрации выполняем вход
      try {
        const loginResponse = await axios.post('http://109.73.194.154:81/api/token/', {
          login: loginValue.value,
          password: passValue.value
        })

        if (loginResponse.data.access) {
          localStorage.setItem('access', loginResponse.data.access)
          localStorage.setItem('refresh', loginResponse.data.refresh)
          router.push({ name: 'main' })
        }
      } catch (loginError) {
        showError('Регистрация успешна, но возникла ошибка при входе. Пожалуйста, войдите вручную.')
        router.push({ name: 'signin' })
      }
    }
  } catch (error) {
    console.log(error)
    if (error.response) {
      if (error.response.status === 400) {
        showError('Пользователь с таким логином уже существует')
      } else {
        showError('Ошибка сервера: ' + error.response.status)
      }
    } else if (error.request) {
      showError('Ошибка сети. Проверьте подключение')
    } else {
      showError('Произошла ошибка при регистрации')
    }
  } finally {
    isLoading.value = false
  }
}

const routing = () => {
  router.push({ name: 'signin' })
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