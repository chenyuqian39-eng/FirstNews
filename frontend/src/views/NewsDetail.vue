<template>
  <div class="news-detail">
    <van-nav-bar
      title="News Details"
      left-text="Back"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="detail-content" v-if="newsStore.newsDetail.id">
      <div class="title-container">
        <h1 class="title">{{ newsStore.newsDetail.title }}</h1>
        <van-button 
          class="favorite-btn" 
          :icon="isFavorite ? 'star' : 'star-o'" 
          :class="{ 'is-favorite': isFavorite }"
          @click="toggleFavorite"
        />
      </div>
      
      <div class="info">
        <span>{{ newsStore.newsDetail.author }}</span>
        <span>{{ newsStore.newsDetail.publishTime }}</span>
        <span>{{ newsStore.newsDetail.views }} views</span>
      </div>
      
      <div class="cover" v-if="newsStore.newsDetail.image">
        <img :src="newsStore.newsDetail.image" :alt="newsStore.newsDetail.title">
      </div>
      
      <div class="content">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </div>
      
      <div class="related-news" v-if="newsStore.newsDetail.relatedNews?.length">
        <h3>Related News</h3>
        <div class="related-list">
          <div 
            class="related-item" 
            v-for="item in newsStore.newsDetail.relatedNews" 
            :key="item.id"
            @click="goToRelatedNews(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="item.title">
            </div>
            <div class="related-title">{{ item.title }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <van-empty v-else description="Loading..." />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../store/modules/news'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

// Get news ID from route params
const newsId = computed(() => Number(route.params.id))

// Split content into paragraphs
const contentParagraphs = computed(() => {
  if (!newsStore.newsDetail.content) return []
  return newsStore.newsDetail.content.split('\n\n').filter(p => p.trim())
})

// Go back
const onClickLeft = () => {
  router.back()
}

// Navigate to related news
const goToRelatedNews = (id) => {
  router.push(`/news/detail/${id}`)
}

// Check whether the current news item is favorited
const isFavorite = computed(() => {
  return favoriteStore.isFavorite(newsId.value)
})

// Toggle favorite status
const toggleFavorite = async () => {
  // Check whether the user is logged in
  if (!userStore.getLoginStatus) {
    // If not logged in, go to login page
    showToast({
      message: 'Please log in before adding favorites',
      position: 'bottom',
    })
    router.push('/login')
    return
  }
  
  // If logged in, call API to toggle favorite status
  const status = await favoriteStore.toggleFavorite(newsStore.newsDetail)
  
  if (status === true) {
    showToast({
      message: 'Added to favorites',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: 'Removed from favorites',
      position: 'bottom',
    })
  } else {
    // A null status means the operation failed
    showToast({
      message: 'Operation failed. Please try again later',
      position: 'bottom',
    })
  }
}

// Get news details and add browsing history when the component mounts
onMounted(async () => {
  await newsStore.getNewsDetail(newsId.value)
  
  // Add to browsing history
  if (newsStore.newsDetail.id) {
    // Call API to record browsing history first
    if (userStore.getLoginStatus) {
      try {
        const result = await historyStore.addHistoryApi(newsStore.newsDetail.id);
        console.log('Record history API result:', result);
      } catch (error) {
        console.error('Record history API failed:', error);
      }
    }
    
    // Add to local browsing history whether or not the API succeeds
    // historyStore.addHistory(newsStore.newsDetail);
  }
  
  // Load favorite data
  favoriteStore.loadFavorites()
  
  // Check article favorite status
  if (userStore.getLoginStatus && newsStore.newsDetail.id) {
    const result = await favoriteStore.checkFavoriteStatusApi(newsStore.newsDetail.id)
    if (result.success && !result.isLocal) {
      // If the API request succeeds and is not local state, update local favorite status
      if (result.isFavorite && !favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.addFavorite(newsStore.newsDetail)
      } else if (!result.isFavorite && favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.removeFavorite(newsStore.newsDetail.id)
      }
    }
  }
})
</script>

<style scoped>
.news-detail {
  padding-top: 46px;
  background-color: #fff;
  min-height: 100vh;
}

.detail-content {
  padding: 16px;
}

.title-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title {
  font-size: 22px;
  font-weight: bold;
  line-height: 1.4;
  margin: 0;
  flex: 1;
}

.favorite-btn {
  flex-shrink: 0;
  margin-left: 10px;
  padding: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.favorite-btn.is-favorite {
  color: #ff9500;
}

.info {
  display: flex;
  font-size: 12px;
  color: #999;
  margin-bottom: 16px;
}

.info span {
  margin-right: 12px;
}

.cover {
  margin-bottom: 16px;
}

.cover img {
  width: 100%;
  border-radius: 4px;
}

.content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
}

.content p {
  margin-bottom: 16px;
  text-align: justify;
}

.related-news {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 8px solid #f5f5f5;
}

.related-news h3 {
  font-size: 18px;
  margin: 0 0 16px;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  align-items: center;
}

.related-image {
  width: 80px;
  height: 60px;
  margin-right: 12px;
  flex-shrink: 0;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.related-title {
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}
</style>