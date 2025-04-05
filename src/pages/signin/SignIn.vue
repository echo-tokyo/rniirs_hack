<template>
  <div class="item">
    <form action="" @submit.prevent='handleSubmit()'> 
      <h1>Вход</h1>
      <input type="text" placeholder='Логин' v-model='loginValue'>
      <input type="password" placeholder='Пароль' v-model='passValue'>
      <input type="submit" value='Зарегистрироваться'>
    </form>
    <p>Еще нет аккаунта ? <span class='form-span' @click='routing()'>Зарегистрируйтесь</span></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleSubmit = (e) => {
  if (e && e.preventDefault) {
    e.preventDefault()
  }
  localStorage.setItem('token', 'token')
  router.push( { name: 'main' } )
}

const routing = (e) => {
  router.push({ name: 'signup' })
}
const loginValue = ref('')
const passValue = ref('')
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
</style>