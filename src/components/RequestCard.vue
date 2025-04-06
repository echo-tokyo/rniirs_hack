<script setup>
import { ref } from 'vue'

const props = defineProps({
    header: String,
    description: String,
    date: String,
    category: String,
    id: {
        type: [String, Number],
        required: true
    }
})

const emit = defineEmits(['approve', 'reject'])

const handleApprove = (e) => {
    e.stopPropagation()
    emit('approve', {
        id: props.id,
        header: props.header,
        description: props.description,
        date: props.date,
        category: props.category
    })
}

const handleReject = (e) => {
    e.stopPropagation()
    emit('reject', {
        id: props.id,
        header: props.header,
        description: props.description,
        date: props.date,
        category: props.category
    })
}
</script>

<template>
<div class="NewsCard-container" @click="$router.push(`/requests/${props.id}`)">
    <div class="NewsCard-information">
        <div class="News-information__text">
            <h2 class="NewsCard-information__header">{{ props.header }}</h2>
            <h2 class="NewsCard-information__description">{{ props.description }}</h2>
        </div>

        <div class="NewsCard-bottom">
            <h2 class="NewsCard-information__date">{{ props.date }}</h2>
            <div class="action-buttons">
                <button class="action-button approve" @click="handleApprove">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
                    </svg>
                </button>
                <button class="action-button reject" @click="handleReject">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" fill="currentColor"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    <div class="NewsCard-category">
        <h2 class="NewsCard-category__category">{{ props.category }}</h2>
    </div>
</div>
</template>

<style scoped>
.NewsCard-container {
    background: #FFFFFF;
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

.action-buttons {
    display: flex;
    gap: 8px;
}

.action-button {
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    border-radius: 50%;
}

.action-button:active {
    transform: scale(0.85);
}

.action-button.approve {
    color: #4CAF50;
}

.action-button.approve:hover {
    background: rgba(76, 175, 80, 0.1);
}

.action-button.reject {
    color: #FF5252;
}

.action-button.reject:hover {
    background: rgba(255, 82, 82, 0.1);
}

.NewsCard-category {
    position: absolute;
    top: 20px;
    right: 20px;
}

.NewsCard-category__category {
    font-size: 14px;
    color: #0066FF;
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