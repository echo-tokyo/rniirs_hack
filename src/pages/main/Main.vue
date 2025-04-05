<script setup>

const selectOptions = [
  'Все категории',
  'Название категории',
  'Избранное',
  'Другое'
]

const cityOptions = [
  'Москва',
  'Санкт-Петербург',
  'Новосибирск',
  'Екатеринбург',
  'Казань',
  'Нижний Новгород'
]

const sortOptions = [
  'По популярности',
  'По возрастанию цены',
  'По убыванию цены',
  'По рейтингу',
  'По отзывам'
]
</script>

<template>
  <div class="app">
    <div class="container">
      <div class="selects-container">
        <CustomSelect 
          :options="selectOptions"
          placeholder="Выберите категорию"
        />
        <CustomSelect 
          :options="cityOptions"
          placeholder="Выберите город"
        />
        <CustomSelect 
          :options="sortOptions"
          placeholder="Сортировка"
        />
      </div>
      <button class="create-button">Создать новость</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.selects-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  width: 100%;
}

.selects-container > * {
  flex: 1;
}

.create-button {
  height: 65px;
  border: none;
  border-radius: 20px;
  background: #0066FF;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 100%;
}

.create-button:hover {
  background: #0052cc;
}

@media (min-width: 768px) {
  .container {

  }

  .selects-container {
    gap: 30px;
  }
}

@media (max-width: 767px) {
  .container {
    padding: 1rem;
  }

  .selects-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .selects-container > * {
    width: 100%;
  }
}
</style>
