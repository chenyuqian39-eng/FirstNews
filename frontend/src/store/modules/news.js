import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

const defaultCategories = [
  { id: 1, name: 'Headline' },
  { id: 2, name: 'Society' },
  { id: 3, name: 'Domestic' },
  { id: 4, name: 'International' },
  { id: 5, name: 'Entertainment' },
  { id: 6, name: 'Sports' },
  { id: 7, name: 'Technology' }
]

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    newsDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false
  }),

  actions: {
    createMockNewsList(page = 1, pageSize = 10) {
      const categoryName = this.getCategoryName(this.currentCategory)
      const startId = (page - 1) * pageSize + 1

      return Array.from({ length: pageSize }, (_, index) => {
        const id = startId + index

        return {
          id,
          title: `${categoryName} News ${id}`,
          description: `This is a short ${categoryName} news summary with the main details and highlights.`,
          image: `https://picsum.photos/seed/news-${this.currentCategory}-${id}/220/160`,
          author: 'News Desk',
          publishTime: new Date().toLocaleString(),
          categoryId: this.currentCategory,
          views: Math.floor(Math.random() * 10000)
        }
      })
    },

    createMockNewsDetail(id) {
      const categoryName = this.getCategoryName(this.currentCategory)

      return {
        id: Number(id),
        title: `${categoryName} News ${id}`,
        description: `This is a short ${categoryName} news summary with the main details and highlights.`,
        image: `https://picsum.photos/seed/news-detail-${id}/420/280`,
        author: 'News Desk',
        publishTime: new Date().toLocaleString(),
        categoryId: this.currentCategory,
        views: Math.floor(Math.random() * 10000),
        content: `This is the full story for ${categoryName} News ${id}.\n\nThe event has attracted attention and continues to develop.\n\nMore details will be updated as additional information becomes available.`,
        relatedNews: Array.from({ length: 3 }, (_, index) => ({
          id: 1000 + index,
          title: `Related ${categoryName} News ${index + 1}`,
          image: `https://picsum.photos/seed/related-${id}-${index}/220/160`
        }))
      }
    },

    async getCategories() {
      if (this.categoriesLoading) return

      this.categoriesLoading = true

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/categories`)

        if (response.data && response.data.code === 200) {
          this.categories = [...response.data.data, { id: 10, name: 'More' }]

          if (!this.currentCategory && this.categories.length > 0) {
            this.currentCategory = this.categories[0].id
          }
        }
      } catch (error) {
        console.error('Failed to get news categories:', error)
        this.categories = defaultCategories
      } finally {
        this.categoriesLoading = false
      }
    },

    changeCategory(categoryId) {
      if (this.currentCategory !== categoryId) {
        this.currentCategory = categoryId
        this.newsList = []
        this.finished = false
        this.getNewsList(true)
      }
    },

    async getNewsList(isRefresh = false) {
      if (isRefresh) {
        this.refreshing = true
        this.newsList = []
        this.finished = false
      }

      this.loading = true

      const params = {
        categoryId: this.currentCategory,
        page: isRefresh ? 1 : Math.ceil(this.newsList.length / 10) + 1,
        pageSize: 10
      }

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/list`, {
          params,
          timeout: 5000
        })

        if (response.data && response.data.code === 200) {
          const newsData = response.data.data.list
          this.newsList = isRefresh ? newsData : [...this.newsList, ...newsData]

          if (newsData.length < params.pageSize) {
            this.finished = true
          }
        } else {
          const mockData = this.createMockNewsList(params.page, params.pageSize)
          this.newsList = isRefresh ? mockData : [...this.newsList, ...mockData]
        }
      } catch (error) {
        console.error('Failed to get news list:', error)
        const mockData = this.createMockNewsList(params.page, params.pageSize)
        this.newsList = isRefresh ? mockData : [...this.newsList, ...mockData]
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },

    async getNewsDetail(id) {
      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/detail?id=${id}`)

        if (response.data && response.data.code === 200) {
          this.newsDetail = response.data.data
          return
        }

        console.error('Failed to get news details: API returned an error')
      } catch (error) {
        console.error('Failed to get news details:', error)
      }

      this.newsDetail = this.createMockNewsDetail(id)
    },

    getCategoryName(categoryId) {
      const category = this.categories.find((item) => item.id === categoryId)
      return category ? category.name : 'Unknown'
    }
  }
})
