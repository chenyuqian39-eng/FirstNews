<template>
  <div class="home">
    <van-nav-bar :title="$t('home.title')" fixed />
    
    <!-- Independent More options div -->
    <div class="more-options">
      <div class="more-tab" @click="goToCategory">
        {{ $t('home.more') }} <van-icon name="arrow" />
      </div>
    </div>
    
    <div class="category-tabs">
      <van-tabs v-model:active="activeTab" sticky swipeable animated>
        <van-tab 
          v-for="(category, index) in displayCategories" 
          :key="category.id" 
          :title="getCategoryTranslation(category.name)"
          @click="newsStore.changeCategory(category.id)"
        >
          <van-pull-refresh v-model="newsStore.refreshing" @refresh="onRefresh">
            <van-list
              v-model:loading="newsStore.loading"
              :finished="newsStore.finished"
              :finished-text="$t('home.noMore')"
              @load="onLoad"
            >
              <news-item 
                v-for="item in newsStore.newsList" 
                :key="item.id" 
                :news="item" 
              />
            </van-list>
          </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue'
import { useNewsStore } from '../store/modules/news'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import NewsItem from '../components/NewsItem.vue'
import TabBar from '../components/TabBar.vue'

const newsStore = useNewsStore()
const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const activeTab = ref(0)
const tabsTop = ref(0)

// Watch route changes
watch(
  () => route.query.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      const categoryId = parseInt(newCategoryId)
      // Find the index matching the category ID
      const filteredCategories = newsStore.categories.filter(category => category.name !== 'More')
      const index = filteredCategories.findIndex(cat => cat.id === categoryId)
      
      if (index !== -1) {
        // Set activeTab to the matching index
        activeTab.value = index
        // Switch categories
        newsStore.changeCategory(categoryId)
      }
    }
  },
  { immediate: true }
)

onMounted(() => {
  // Get news categories
  newsStore.getCategories().then(() => {
    // Get news list
    newsStore.getNewsList()
  })
  
  // Initialize position
  setTimeout(updateTabsPosition, 300)
  
  // Add scroll event listener
  window.addEventListener('scroll', handleScroll)
})

// Computed property: displayed categories excluding More
const displayCategories = computed(() => {
  // Get all categories except More
  return newsStore.categories.filter(category => category.name !== 'More');
})

// Computed property: categories shown in the More menu, limited to Military, Technology, and Finance
const moreCategories = computed(() => {
  return newsStore.categories.filter(category => 
    category.name === 'Military' || 
    category.name === 'Technology' || 
    category.name === 'Finance'
  );
})

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
    

// Go to category page
const goToCategory = () => {
  router.push('/category')
}

// Handle tab click event
const handleTabClick = (index) => {
  // If the clicked option is not More, close the dropdown menu
  if (displayCategories.value[index].name !== 'More') {
    showDropdown.value = false
    newsStore.changeCategory(displayCategories.value[index].id)
  }
}

// Select a category from More categories
const selectMoreCategory = (category) => {
  showDropdown.value = false
  newsStore.changeCategory(category.id)
  
  // Find the selected category index in the original category list
  const index = newsStore.categories.findIndex(cat => cat.id === category.id)
  if (index !== -1) {
    // Directly set activeTab to the matching index
    activeTab.value = index
  }
}
// Get category tab position and set up scroll listener
const updateTabsPosition = () => {
  const tabsElement = document.querySelector('.van-tabs__wrap')
  if (tabsElement) {
    tabsTop.value = tabsElement.getBoundingClientRect().top
  }
}

// Handle scroll event
const handleScroll = () => {
  updateTabsPosition()
}

// Remove event listener before component unmount
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Watch category changes
watch(activeTab, (newVal) => {
  const categoryId = displayCategories.value[newVal]?.id
  if (!categoryId) return

  newsStore.changeCategory(categoryId)
})

// Pull to refresh
const onRefresh = () => {
  newsStore.getNewsList(true)
}

// Load more on scroll
const onLoad = () => {
  newsStore.getNewsList()
}

// Switch categories
const changeCategory = (categoryId) => {
  // If the clicked option is More
  if (categoryId === 10) {
    goToCategory()
    return
  }
  
  newsStore.changeCategory(categoryId)
}
</script>

<style scoped>
.home {
  padding-top: 46px;
  padding-bottom: 50px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.category-tabs {
  margin-bottom: 10px;
  position: relative;
}

:deep(.van-tabs__wrap) {
  background-color: #fff;
}

:deep(.van-tab) {
  font-size: 14px;
}

:deep(.van-tab--active) {
  font-weight: bold;
  color: #1989fa;
}

.more-options {
  position: fixed;
  right: 0;
  background-color: #fff;
  padding: 0;
  border-radius: 4px 0 0 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  /* Set top dynamically through computed binding */
  top: v-bind('tabsTop + "px"');
  height: 44px; /* Match the height of van-tabs__wrap */
  display: flex;
  align-items: center;
}

.more-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #1989fa;
  font-weight: bold;
  height: 100%;
  padding: 0 10px;
}

.dropdown-menu {
  position: absolute;
  right: 15px;
  top: 40px;
  min-width: 100px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 4px;
  z-index: 999;
}

.dropdown-item {
  padding: 10px 15px;
  text-align: center;
  border-bottom: 1px solid #f5f5f5;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}
</style>
