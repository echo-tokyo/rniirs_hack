<template>
  <div class="item">
    <h1>Регистрация</h1>
    <form action="" @submit='e.preventDefault()'> 
      <input type="text" placeholder='Логин' v-model='loginValue'>
      <input type="password" placeholder='Пароль' v-model='passValue'>
      <input type="button" value='Войти'
    </form>
    <h3>Есть аккаунт ? <span @click='routing()'>Войдите</span></h3>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const routing = () => {
  router.push({ name: 'signin' })
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