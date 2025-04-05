<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const isAdmin = localStorage.getItem('isAdmin')
const route = useRoute()
const router = useRouter()
const id = route.params.id // Use route here
const newsData = ref({
  header: '',
  description: '',
  date: '',
  category: '',
  status: 'pending'
})

// Настраиваем marked для обработки ссылок и изображений
marked.use({
  gfm: true,
  breaks: true,
  mangle: false,
  headerIds: false
})

// Создаем вычисляемое свойство для преобразованного HTML
const parsedContent = computed(() => {
  if (!newsData.value.description) return ''
  // Преобразуем Markdown в HTML и очищаем его
  const html = marked(newsData.value.description)
  return DOMPurify.sanitize(html)
})

onMounted(() => {
  // получили данные по id
  // const mockData = {
  //   header: "НОУ ВЭЙ, ЧИКИПИКИ",
  //   description: "АЛИНЫ ЧИКИ ПИКИ ГЕТ ДИС ВОРЛД АУТ, НО ВЭЙ ВАТАКАК СМОТРИТЕ",
  //   date: "03.05.2024",
  //   category: "Спортивный интерес",
  //   author: "ФНР"
  // }
  
  const mockData = {
      header: "Прорыв в квантовых вычислениях: новая эра в IT",
      description: `![image](https://rscf.ru/upload/iblock/def/5myvev5k88gzb29l9otn1y5kpq2uxy1y.jpeg)\n\n**Российские ученые совместно с иностранными коллегами нашли способ [повысить](http://doi.org/10.1016/j.jip.2025.108301) вирулентность полезных бактерий Bacillus thuringiensis. Эти микроорганизмы применяются в сельском хозяйстве для уничтожения вредителей — колорадского жука, личинок мух, капустной моли и т. д. Авторы исследования подобрали такие условия культивации бактерий, которые делают микроорганизмы более агрессивными к вредным насекомым. Полученные данные помогут создать более эффективные биопестициды — экологически безопасные препараты.**\n\nРоссийские ученые из [Новосибирского государственного аграрного университета](http://edubiotech.ru) совместно со специалистами из [Университета Голуэя](http://www.universityofgalway.ie) (Ирландия) и [Университета Суонси](http://www.swansea.ac.uk) (Великобритания) изучили условия роста бактерий Bacillus thuringiensis. Эти микроорганизмы могут применяться против сельскохозяйственных насекомых-вредителей. Об этом RT сообщили в пресс-службе Российского научного фонда, при [поддержке](http://rscf.ru/project/24-16-00113/) которого была проведена работа. Результаты [опубликованы](http://doi.org/10.1016/j.jip.2025.108301) в Journal of Invertebrate Pathology.\n\nБактерии Bacillus thuringiensis безопасны для человека и полезных насекомых, таких как пчелы или божьи коровки. Зато успешно уничтожают вредителей: личинок мух, комаров, колорадского жука и бабочек — капустной совки, капустной моли, а также вощинной огневки (вредителя пчеловодства, который поедает мед, соты и пергу).\n\nУченые задались целью выяснить, в каких условиях культивируются наиболее эффективные в борьбе с вредителями бактерии. Для этого исследователи вырастили колонии микроорганизмов в жидкой среде, которая имитировала гемолимфу насекомых, а другие колонии бактерий — на плотной среде, похожей на кишечник насекомых, поверхность листьев растений или почву.\n\n\n\n\n\nБактерии в термошейкере. Источник: Пресс-центр НГАУ\n\n\n\nВыяснилось, что бактерии, растущие на плотной среде, убивали личинок насекомых-вредителей в два раза быстрее и эффективнее, чем те, которые росли в жидкости.\n\nБиологи объяснили эту разницу тем, что на твердой поверхности в отсутствие питательных веществ у бактерий Bacillus thuringiensis иначе работают гены, контролирующие их жизненный цикл. Так, в суровых условиях у микроорганизмов раньше запускается процесс образования спор, которые помогают бактериям сохраняться в неблагоприятных условиях, и выработка Cry-токсинов, повышающих вирулентность патогенов, то есть их способность убивать насекомых.\n\nПолученные учеными данные помогут создать эффективные биологические инсектициды — препараты на основе микроорганизмов для защиты растений от вредителей.\n\n> «В будущих исследованиях мы планируем изучить жизненный цикл популяций бактерий Bacillus thuringiensis в организме насекомых после инъекции, что поможет лучше понять, как бактерии адаптируются к различным условиям внутри хозяина и как сделать биопрепараты более эффективными», — рассказала RT ведущий научный сотрудник, доцент кафедры защиты растений Новосибирского государственного аграрного университета Екатерина Гризанова.\n\n\n\n
`,
      date: "15.03.2024",
      category: "Технологии",
      author: "Квантовая лаборатория",
      status: 'pending'
  }
  newsData.value = mockData
})

const handleApprove = () => {
  // Здесь будет логика одобрения новости
  console.log('Новость одобрена')
  router.push('/requests')
}

const handleReject = () => {
  // Здесь будет логика отклонения новости
  console.log('Новость отклонена')
  router.push('/requests')
}

const newsDelete = () => {
  router.push({name: 'main'})
}
</script>

<template>
  <div class="news-page">
    <div class="news-container">
      <div class="btns-container">
        <button class="back-button" @click="$router.back()">
          <span>←</span> Назад
        </button>
        <div v-if="isAdmin && newsData.status === 'pending'" class="admin-controls">
          <button class="action-button approve" @click="handleApprove">
            Принять
          </button>
          <button class="action-button reject" @click="handleReject">
            Отклонить
          </button>
        </div>
      </div>
      
      <div class="news-header">
        <h1 class="title">{{ newsData.header }}</h1>
        <div class="meta-info">
          <span class="date">{{ newsData.date }}</span>
          <span class="date">{{ newsData.author }}</span>
          <span class="category">{{ newsData.category }}</span>
        </div>
      </div>

      <div class="news-content markdown-body" v-html="parsedContent"></div>
    </div>

    <button v-if='!isAdmin' class="delete-button" @click="newsDelete">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
      </svg>
      Удалить
    </button>
  </div>
</template>

<style>
img{
  width: 40vw;
}
.news-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.news-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.btns-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 2rem;
}

.admin-controls {
  display: flex;
  gap: 12px;
}

.action-button {
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button.approve {
  background: #4CAF50;
  color: white;
}

.action-button.approve:hover {
  background: #43A047;
}

.action-button.reject {
  background: #FF5252;
  color: white;
}

.action-button.reject:hover {
  background: #D32F2F;
}

.delete-button {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  border: 1px solid #FF5252;
  background: white;
  color: #FF5252;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 100;
}

.delete-button:hover {
  background: rgba(255, 82, 82, 0.1);
  transform: translateY(-2px);
}

.delete-button:active {
  transform: translateY(0);
}

.back-button {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  padding: 0;
}

.back-button:hover {
  color: #0066FF;
}

.news-header {
  margin-bottom: 2rem;
}

.title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #333;
}

.meta-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.date {
  color: #666;
  font-size: 14px;
}

.category {
  background: rgba(0, 102, 255, 0.1);
  color: #0066FF;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 14px;
}

@media (max-width: 767px) {
  .news-container {
    padding: 0 1rem;
  }

  .title {
    font-size: 24px;
  }

  .btns-container {
    flex-wrap: wrap;
  }

  .admin-controls {
    width: 100%;
  }

  .action-button {
    flex: 1;
  }

  .delete-button {
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
  }
}
</style>

<style>
.markdown-body {
  font-size: 18px;
  line-height: 1.6;
  color: #333;
}

.markdown-body h1 {
  font-size: 2.5em;
  margin: 24px 0;
  font-weight: 600;
}

.markdown-body h2 {
  font-size: 2em;
  margin: 20px 0;
  font-weight: 600;
}

.markdown-body h3 {
  font-size: 1.5em;
  margin: 16px 0;
  font-weight: 600;
}

.markdown-body img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 24px 0;
}

.markdown-body p {
  margin: 16px 0;
}

.markdown-body a {
  color: #0066FF;
  text-decoration: none;
  transition: color 0.2s ease;
}

.markdown-body a:hover {
  color: #0052CC;
  text-decoration: underline;
}

.markdown-body strong {
  font-weight: 600;
}

.markdown-body blockquote {
  margin: 24px 0;
  padding: 16px 24px;
  border-left: 4px solid #0066FF;
  background: rgba(0, 102, 255, 0.05);
  border-radius: 4px;
  font-style: italic;
}

.markdown-body blockquote p {
  margin: 0;
}

.markdown-body ul, .markdown-body ol {
  margin: 16px 0;
  padding-left: 24px;
}

.markdown-body li {
  margin: 8px 0;
}

.markdown-body code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

.markdown-body pre {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-body pre code {
  background: none;
  padding: 0;
  font-size: 14px;
  line-height: 1.5;
}

.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.markdown-body table th,
.markdown-body table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.markdown-body table th {
  background: #f5f5f5;
  font-weight: 600;
}

.markdown-body hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 32px 0;
}

@media (max-width: 767px) {
  .markdown-body {
    font-size: 16px;
  }

  .markdown-body h1 {
    font-size: 2em;
  }

  .markdown-body h2 {
    font-size: 1.5em;
  }

  .markdown-body h3 {
    font-size: 1.25em;
  }

  .markdown-body blockquote {
    padding: 12px 16px;
    margin: 16px 0;
  }

  .markdown-body pre {
    padding: 12px;
  }

  .markdown-body table th,
  .markdown-body table td {
    padding: 8px;
  }
}
</style> 