import { defineStore } from 'pinia';
import axios from 'axios';
import { apiConfig } from '../config/api';

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    token: '',
    isLogin: false,
    userBio: 'This isMeBio'
  }),
  
  getters: {
    getUserInfo: (state) => state.userInfo,
    getToken: (state) => state.token,
    getLoginStatus: (state) => state.isLogin,
    getUserBio: (state) => state.userInfo?.bio || state.userBio
  },
  
  actions: {
    async login(userData) {
      try {
        // Send login request
        const response = await axios.post(`${apiConfig.baseURL}/api/user/login`, {
          username: userData.username,
          password: userData.password
        });
        
        // Check response status
        if (response.data && response.data.code === 200) {
          // Login succeeded
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: 'Login succeeded'
          };
        } else {
          // Login failed
          return {
            success: false,
            message: response.data.message || 'Login failed'
          };
        }
      } catch (error) {
        console.error('Login request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Login request failed. Please try again later'
        };
      }
    },
    
    async register(userData) {
      try {
        // Send register request
        const response = await axios.post(`${apiConfig.baseURL}/api/user/register`, {
          username: userData.username,
          password: userData.password
        });
        
        // Check response status
        if (response.data && response.data.code === 200) {
          // Registration succeeded; log in automatically
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: 'Registration succeeded'
          };
        } else {
          // Registration failed
          return {
            success: false,
            message: response.data.message || 'Registration failed'
          };
        }
      } catch (error) {
        console.error('Registration request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Registration request failed. Please try again later'
        };
      }
    },
    
    logout() {
      this.userInfo = null;
      this.token = '';
      this.isLogin = false;
    },
    
    // Get user information
    async getUserInfoDetail() {
      try {
        // Check whether a token exists
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        // Send get-user-information request
        const response = await axios.get(`${apiConfig.baseURL}/api/user/info`, {
          headers: {
            // Authorization: `Bearer ${this.token}`
            Authorization: this.token
          }
        });
        
        // Check response status
        if (response.data && response.data.code === 200) {
          // Update user information
          this.userInfo = response.data.data;
          
          return {
            success: true,
            message: 'Got user information successfully',
            data: response.data.data
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to get user information'
          };
        }
      } catch (error) {
        console.error('Failed to request user information:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Failed to request user information. Please try again later'
        };
      }
    },
    
    // Update bio
    async updateUserBio(bio) {
      try {
        // Check whether a token exists
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        // Send update-bio request
        const response = await axios.put(`${apiConfig.baseURL}/api/user/update`, 
          { bio },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        // Check response status
        if (response.data && response.data.code === 200) {
          // Update local user bio
          this.userInfo.bio = bio;
          
          return {
            success: true,
            message: 'Bio updated successfully'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to update bio'
          };
        }
      } catch (error) {
        console.error('Failed to request bio update:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Failed to request bio update. Please try again later'
        };
      }
    },
    
    // Change Password
    async updatePassword(oldPassword, newPassword) {
      try {
        // Check whether a token exists
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        // Send change-password request
        const response = await axios.put(`${apiConfig.baseURL}/api/user/password`, 
          { 
            oldPassword,
            newPassword 
          },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        // Check response status
        if (response.data && response.data.code === 200) {
          return {
            success: true,
            message: 'Password changed successfully'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to change password'
          };
        }
      } catch (error) {
        console.error('Change password request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Change password request failed. Please try again later'
        };
      }
    }
  },
  
  // Add persistence configuration
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user-store',
        storage: localStorage
      }
    ]
  }
});