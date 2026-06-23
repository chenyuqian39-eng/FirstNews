<template>
  <div class="favorite-container">
    <van-nav-bar
      title="My Favorites"
      left-text="Back"
      left-arrow
      @click-left="onClickLeft"
      right-text="Clear"
      @click-right="onClickClear"
      fixed
    />
    
    <div class="favorite-list" v-if="favoriteStore.getFavorites.length">
      <div class="favorite-item" v-for="item in favoriteStore.getFavorites" :key="item.id">
        <van-cell @click="goToNewsDetail(item.id)" :border="false">
          <template #title>
            <div class="news-item">
              <div class="news-image" v-if="item.image">
                <img :src="item.image" :alt="item.title">
              </div>
              <div class="news-info">
                <div class="news-title">{{ item.title }}</div>
                <div class="news-meta">
                  <span>{{ item.author }}</span>
                  <span>{{ item.publishTime }}</span>
                  <span>Favorite time: {{ item.favoriteTime }}</span>
                </div>
              </div>
            </div>
          </template>
        </van-cell>
        <van-button 
          class="delete-btn" 
          type="danger" 
          size="mini" 
          icon="cross"
          @click="confirmDelete(item.id)"
        ></van-button>
      </div>
    </div>
    
    <van-empty v-else description="No favorites yet" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useFavoriteStore } from '../store/modules/favorite';
import { showDialog } from 'vant';

const router = useRouter();
const favoriteStore = useFavoriteStore();

// Go back
const onClickLeft = () => {
  router.back();
};

// Go to news details
const goToNewsDetail = (id) => {
  router.push(`/news/detail/${id}`);
};

// Delete one favorite item
const removeFavorite = async (id) => {
  const result = await favoriteStore.removeFavoriteApi(id);
  if (result.success) {
    // Update local favorite list after the API request succeeds
    favoriteStore.removeFavorite(id);
  }
};

// Confirm deletion
const confirmDelete = (id) => {
  showDialog({
    title: 'Notice',
    message: 'Are you sure you want to delete this favorite?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeFavorite(id);
    }
  });
};

// Clear favorites
const onClickClear = async () => {
  showDialog({
    title: 'Notice',
    message: 'Are you sure you want to clear all favorites?',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      const result = await favoriteStore.clearFavoritesApi();
      if (!result || !result.success) {
        // If the API request fails, fall back to local clearing
        // favoriteStore.clearFavorites();
        console.log('Clear favorites list');
      }
    }
  });
};

// Load favorite data when the component mounts
onMounted(async () => {
  // Use API request to get favorite list
  try {

    const result = await favoriteStore.getFavoriteListApi();
    if (!result || !result.success) {
      // If the API request fails, fall back to local storage
      // favoriteStore.loadFavorites();
      console.log('Load favorite list from local storage');  
    }
  } catch (error) {
    favoriteStore.loadFavorites();
  }
});
</script>

<style scoped>
.favorite-container {
  padding-top: 46px;
  padding-bottom: 20px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.favorite-list {
  padding: 10px;
}

.news-item {
  display: flex;
  padding: 10px 0;
}

.news-image {
  width: 120px;
  height: 80px;
  margin-right: 12px;
  flex-shrink: 0;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.news-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.news-title {
  font-size: 16px;
  font-weight: bold;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  flex-wrap: wrap;
}

.news-meta span {
  margin-right: 10px;
}

.favorite-item {
  position: relative;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.delete-btn {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  z-index: 10;
  width: 24px;
  height: 24px;
  padding: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>