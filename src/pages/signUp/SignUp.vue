<template>
  <div class="item">
    <h1>Регистрация</h1>
    <form action="" @submit.prevent='handleSubmit()'> 
      <input type="text" placeholder='Логин' v-model='loginValue'>
      <input type="password" placeholder='Пароль' v-model='passValue'>
      <input type="submit" value='Войти'>
    </form>
    <h3>Есть аккаунт ? <span @click='routing()'>Войдите</span></h3>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const loginValue = ref('')
const passValue = ref('')

const router = useRouter()

const handleSubmit = (e) => {
  if (e && e.preventDefault) {
    e.preventDefault()
  }
  router.push( { name: 'main' } )
}

const routing = (e) => {
  if (e && e.preventDefault) {
    e.preventDefault()
  }
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
</style>