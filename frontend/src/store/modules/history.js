import { defineStore } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../user';
import { apiConfig } from '../../config/api';

export const useHistoryStore = defineStore('history', {
  state: () => ({
    history: [],
  }),
  
  getters: {
    getHistory: (state) => state.history,
  },
  
  actions: {
    // Add browsing history through API
    async addHistoryApi(newsId) {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        return { success: false, message: 'Please log in first' };
      }
      
      try {
        const response = await axios.post(`${apiConfig.baseURL}/api/history/add`, 
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
          return { success: false, message: response.data.message || 'Failed to add browsing history' };
        }
      } catch (error) {
        console.error('Failed to request adding browsing history:', error);
        return { success: false, message: 'Network request failed' };
      }
    },
    
    // Add browsing history locally
    addHistory(news) {
      // Check whether news with the same ID already exists
      const existingIndex = this.history.findIndex(item => item.id === news.id);
      
      // If it already exists, remove the old record first
      if (existingIndex !== -1) {
        this.history.splice(existingIndex, 1);
      }
      
      // Add to the front of history so the latest item appears first
      this.history.unshift({
        ...news,
        viewTime: new Date().toLocaleString()
      });
      
      // Limit history to a maximum of 50 items
      if (this.history.length > 50) {
        this.history.pop();
      }
      
      // Save to local storage
      this.saveHistory();
    },
    
    // Clear browsing history
    clearHistory() {
      this.history = [];
      this.saveHistory();
    },
    
    // Clear browsing history through API
    async clearHistoryApi() {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        console.log('Clear browsing history API: user is not logged in, using local operation');
        this.clearHistory();
        return { success: true, isLocal: true };
      }
      
      try {
        console.log('Clear browsing history API: request started');
        const response = await axios.delete(`${apiConfig.baseURL}/api/history/clear`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          console.log('Clear browsing history API: cleared successfully');
          // Update local history
          this.clearHistory();
          return { success: true };
        } else {
          console.error('Clear browsing history API: request failed', response.data.message);
          return { success: false, message: response.data.message || 'Failed to clear browsing history' };
        }
      } catch (error) {
        console.error('Clear browsing history API: request error', error);
        return { success: false, message: 'Network request failed' };
      }
    },
    
    // Delete one browsing history item
    removeHistory(id) {
      this.history = this.history.filter(item => item.id !== id);
      this.saveHistory();
    },
    
    // Delete one browsing history item through API
    async removeHistoryApi(id) {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        console.log('Delete history API: user is not logged in, using local operation');
        this.removeHistory(id);
        return { success: true, isLocal: true };
      }
      
      try {
        console.log('Delete history API: request started', id);
        const response = await axios.delete(`${apiConfig.baseURL}/api/history/delete/${id}`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          console.log('Delete history API: deleted successfully');
          // Update local history
          this.removeHistory(id);
          return { success: true };
        } else {
          console.error('Delete history API: request failed', response.data.message);
          return { success: false, message: response.data.message || 'Failed to delete browsing history' };
        }
      } catch (error) {
        console.error('Delete history API: request error', error);
        return { success: false, message: 'Network request failed' };
      }
    },
    
    // Save to local storage
    saveHistory() {
      localStorage.setItem('news_history', JSON.stringify(this.history));
    },
    
    // Load from local storage
    loadHistory() {
      const savedHistory = localStorage.getItem('news_history');
      if (savedHistory) {
        this.history = JSON.parse(savedHistory);
      }
    },
    
    // Get browsing history through API
    async getHistoryListApi() {
      const userStore = useUserStore();
      
      // Check whether the user is logged in
      if (!userStore.getLoginStatus) {
        console.log('Get history API: user is not logged in, using local data');
        return { success: false, message: 'Please log in first', isLocal: true };
      }
      
      try {
        console.log('Get history API: request started');
        const response = await axios.get(`${apiConfig.baseURL}/api/history/list`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          // Read the list array correctly
          const historyList = response.data.data.list || [];
          // console.log(`Get history API: successfully got ${historyList.length} records`, response.data.data);
          // Update local history
          this.history = historyList;
          // Save to local storage
          this.saveHistory();
          return { success: true, data: historyList };
        } else {
          // console.error('Get history API: request failed', response.data.message);
          return { success: false, message: response.data.message || 'Failed to get browsing history' };
        }
      } catch (error) {
        // console.error('Get history API: request error', error);
        return { success: false, message: 'Network request failed' };
      }
    },
  },
});