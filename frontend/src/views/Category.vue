<template>
  <div class="category">
    <van-nav-bar 
      :title="$t('common.allCategories')" 
      :left-text="$t('common.back')"
      left-arrow
      @click-left="onClickLeft"
      fixed 
    />
    
    <div class="category-container">
      <van-grid :column-num="3" :border="false">
        <van-grid-item 
          v-for="category in displayCategories" 
          :key="category.id"
          :text="getCategoryTranslation(category.name)"
          icon="newspaper-o"
          @click="goToCategoryNews(category.id)"
        />
      </van-grid>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { useNewsStore } from '../store/modules/news'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import TabBar from '../components/TabBar.vue'
import { computed } from 'vue'

const newsStore = useNewsStore()
const router = useRouter()
const { t } = useI18n()

// Computed property: displayed categories excluding More
const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== 'More');
})

// Go back
const onClickLeft = () => {
  router.back()
}

// Go to the news list for the selected category
const goToCategoryNews = (categoryId) => {
  // Switch category first
  newsStore.changeCategory(categoryId)
  
  // Pass category ID through route params
  router.push({
    path: '/home',
    query: { categoryId: categoryId }
  })
}

// Get category name translation
const getCategoryTranslation = (categoryName) => {
  const categoryMap = {
    'Headline': 'headline',
    'Society': 'society',
    'Domestic': 'domestic',
    'International': 'international',
    'Entertainment': 'entertainment',
    'Sports': 'sports',
    'Military': 'military',
    'Technology': 'technology',
    'Finance': 'finance',
    'More': 'more'
  };
  
  const key = categoryMap[categoryName];
  return key ? t(`home.categories.${key}`) : categoryName;
}
</script>

<style scoped>
.category {
  padding-top: 46px;
  padding-bottom: 50px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.category-container {
  padding: 16px;
  background-color: #fff;
  margin-top: 12px;
  border-radius: 8px;
}

:deep(.van-grid-item__content) {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 20px 0;
}

:deep(.van-grid-item__icon) {
  font-size: 28px;
  color: #1989fa;
}

:deep(.van-grid-item__text) {
  margin-top: 8px;
  color: #333;
  font-size: 14px;
}
</style>