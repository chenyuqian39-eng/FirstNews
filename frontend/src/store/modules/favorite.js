import { defineStore } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../user';
import { apiConfig } from '../../config/api';

export const useFavoriteStore = defineStore('favorite', {
  state: () => ({
    favorites: [],
    loading: false,
  }),
  
  getters: {
    getFavorites: (state) => state.favorites,
    isFavorite: (state) => (id) => state.favorites.some(item => item.id === id),
  },
  
  actions: {
    // Check article favorite status through API
    async checkFavoriteStatusApi(newsId) {
      const userStore = useUserStore(); 
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        // return { success: false, message: 'Please log in first' };
        console.log('User is not logged in; returning local state');
        return { 
          success: true, 
          isFavorite: this.isFavorite(newsId),
          isLocal: true
        };
      }
      else{
      
        try {
          this.loading = true;
          const response = await axios.get(`${apiConfig.baseURL}/api/favorite/check`, { 
            headers: { 
              Authorization: userStore.token 
            },
            params: { newsId }
          });
          
          if (response.data.code === 200) {
            return { 
              success: true, 
              isFavorite: response.data.data.isFavorite 
            };
          } else {
            return { success: false, message: response.data.message || 'Failed to get favorite status' };
          }
        } catch (error) {
          console.error('Failed to request favorite status:', error);
          // If the API request fails, fall back to local state check
          return { 
            success: true, 
            isFavorite: this.isFavorite(newsId),
            isLocal: true
          };
        } finally {
          this.loading = false;
        }
    }
    },
    
    // Add favorite through API
    async addFavoriteApi(newsId) {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        return { success: false, message: 'Please log in first' };
      }
      
      try {
        this.loading = true;
        const response = await axios.post(`${apiConfig.baseURL}/api/favorite/add`, 
          { newsId },
          { 
            headers: { 
              Authorization: userStore.token 
            } 
          }
        );
        
        if (response.data.code === 200) {
          return { success: true, data: response.data.data };
        } else {
          return { success: false, message: response.data.message || 'Failed to add favorite' };
        }
      } catch (error) {
        console.error('Failed to request adding favorite:', error);
        return { success: false, message: 'Network request failed' };
      } finally {
        this.loading = false;
      }
    },
    
    // Remove favorite through API
    async removeFavoriteApi(newsId) {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        return { success: false, message: 'Please log in first' };
      }
      
      try {
        this.loading = true;
        const response = await axios.delete(`${apiConfig.baseURL}/api/favorite/remove?newsId=${newsId}`, { 
          headers: { 
            Authorization: userStore.token 
          }
        });
        
        if (response.data.code === 200) {
          return { success: true };
        } else {
          return { success: false, message: response.data.message || 'Failed to remove favorite' };
        }
      } catch (error) {
        console.error('Failed to request removing favorite:', error);
        return { success: false, message: 'Network request failed' };
      } finally {
        this.loading = false;
      }
    },
    
    // Add favorite locally
    addFavorite(news) {
      // Check whether news with the same ID already exists
      if (!this.isFavorite(news.id)) {
        // Add to favorite list
        this.favorites.unshift({
          ...news,
          favoriteTime: new Date().toLocaleString()
        });
        
        // Save to local storage
        this.saveFavorites();
      }
    },
    
    // Remove favorite locally
    removeFavorite(id) {
      this.favorites = this.favorites.filter(item => item.id !== id);
      this.saveFavorites();
    },
    
    // Toggle favorite status using API and local state
    async toggleFavorite(news) {
      // Ensure the news object exists and has an id field
      if (!news || !news.id) {
        console.error('Invalid news object:', news);
        return null;
      }
      
      if (this.isFavorite(news.id)) {
        // Remove favorite
        const result = await this.removeFavoriteApi(news.id);
        if (result.success) {
          this.removeFavorite(news.id);
          return false;
        } else {
          return null; // Return null to indicate operation failure
        }
      } else {
        // Add favorite
        const result = await this.addFavoriteApi(news.id);
        if (result.success) {
          this.addFavorite(news);
          return true;
        } else {
          return null; // Return null to indicate operation failure
        }
      }
    },
    
    
    // Clear favorites
    clearFavorites() {
      this.favorites = [];
      this.saveFavorites();
    },
    
    // Clear favorites through API
    async clearFavoritesApi() {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        return { success: false, message: 'Please log in first' };
      }
      
      try {
        this.loading = true;
        const response = await axios.delete(`${apiConfig.baseURL}/api/favorite/clear`, { 
          headers: { 
            Authorization: userStore.token 
          }
        });
        
        if (response.data.code === 200) {
          // Clear local favorite list
          this.clearFavorites();
          return { success: true };
        } else {
          return { success: false, message: response.data.message || 'Failed to clear favorites' };
        }
      } catch (error) {
        console.error('Failed to request clearing favorites:', error);
        return { success: false, message: 'Network request failed' };
      } finally {
        this.loading = false;
      }
    },
    
    // Save to local storage
    saveFavorites() {
      localStorage.setItem('news_favorites', JSON.stringify(this.favorites));
    },
    
    // Load from local storage
    loadFavorites() {
      const savedFavorites = localStorage.getItem('news_favorites');
      if (savedFavorites) {
        this.favorites = JSON.parse(savedFavorites);
      }
    },
    
    // Get favorite list through API
    async getFavoriteListApi(page = 1, pageSize = 10) {
      const userStore = useUserStore();
      
      console.log('getFavoriteListApistarted', {
        isLoggedIn: userStore.getLoginStatus,
        token: userStore.token ? 'exists' : 'does not exist'
      });
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        console.log('User is not logged in; cannot get favorite list');
        return { success: false, message: 'Please log in first' };
      }
      
      try {
        this.loading = true;
        console.log('Preparing to send API request', `${apiConfig.baseURL}/api/favorite/list`);
        const response = await axios.get(`${apiConfig.baseURL}/api/favorite/list`, { 
          headers: { 
            Authorization: userStore.token 
          },
          params: { page, pageSize }
        });
        
        console.log('API response data:', response.data);
        
        if (response.data.code === 200) {
          // Update local favorite list
          this.favorites = response.data.data.list;
          return { success: true, data: response.data.data };
        } else {
          return { success: false, message: response.data.message || 'Failed to get favorite list' };
        }
      } catch (error) {
        return { success: false, message: 'Network request failed' };
      } finally {
        this.loading = false;
      }
    },
  },
});