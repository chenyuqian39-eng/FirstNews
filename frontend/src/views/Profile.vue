<template>
  <div class="profile-page">
    <van-nav-bar
      title="Profile"
      left-arrow
      @click-left="$router.back()"
      fixed
    />
    
    <div class="profile-container">
      <van-cell-group inset class="avatar-group">
        <van-cell title="Avatar" center>
          <template #right-icon>
            <van-image
              round
              width="60"
              height="60"
              src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
            />
          </template>
        </van-cell>
      </van-cell-group>
      
      <van-cell-group inset class="info-group">
        <van-cell title="Username" :value="userInfo.username || 'admin'" />
        <van-cell title="Account ID" :value="`ID: heima-${userId || 'N/A'}`" />
        <van-cell title="Bio" :value="userBio || 'No bio yet'" is-link @click="showBioDialog" />
      </van-cell-group>
      
      <van-cell-group inset class="security-group">
        <van-cell title="Change Password" is-link @click="showPasswordConfirm" />
      </van-cell-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { showDialog, showToast, showLoadingToast, showSuccessToast, showFailToast } from 'vant';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { apiConfig } from '../config/api';

const router = useRouter();
const userStore = useUserStore();

// Initialize user state
onMounted(async () => {
  // If the user is not logged in, go to login page
  if (!userStore.getLoginStatus) {
    router.push('/login');
    return;
  }
  
  // Get user information
  try {
    // Show loading toast
    const loadingInstance = showLoadingToast({
      message: 'Loading...',
      forbidClick: true,
      duration: 0
    });
    
    // console.log('Getting user information, current token:', userStore.token);
    
    // Use the new getUserInfoDetail method
    const result = await userStore.getUserInfoDetail();
    
    // Manually close loading toast
    loadingInstance.close();
    
    if (result.success) {
      console.log('Got user information successfully:', userStore.userInfo);
      // Show success toast
      // showSuccessToast('Got user information successfully');
    } else {
      console.error('Failed to get user information:', result.message);
      showFailToast(result.message || 'Failed to get user information');
    }
  } catch (error) {
    console.error('Failed to request user information:', error);
    // Ensure loading toast is closed
    showToast.clear();
    showToast.fail('Failed to get user information');
  }
});

const userInfo = computed(() => userStore.userInfo);
const userId = computed(() => userStore.token ? userStore.token.substring(0, 5) : '');
const userBio = computed(() => userStore.userInfo?.bio || 'No bio yet');

const showPasswordConfirm = () => {
  // Use ref to create reactive variables
  const oldPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');
  
  showDialog({
    title: 'Change Password',
    showCancelButton: true,
    className: 'password-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, 'Current password:'),
        h('input', {
          type: 'password',
          value: oldPassword.value,
          onInput: (e) => { oldPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, 'New password:'),
        h('input', {
          type: 'password',
          value: newPassword.value,
          onInput: (e) => { newPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, 'ConfirmPassword：'),
        h('input', {
          type: 'password',
          value: confirmPassword.value,
          onInput: (e) => { confirmPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ])
    ]),
  }).then(async () => {
    // Click confirm button
    if (!oldPassword.value) {
      showToast('Please enter your current password');
      return;
    }
    
    if (!newPassword.value) {
      showToast('Please enter a new password');
      return;
    }
    
    if (newPassword.value !== confirmPassword.value) {
      showToast('The two passwords do not match');
      return;
    }
    
    try {
      // Show loading toast
      const loadingInstance = showLoadingToast({
        message: 'Changing...',
        forbidClick: true,
        duration: 0
      });
      
      // Call API to update password
      const result = await userStore.updatePassword(oldPassword.value, newPassword.value);
      
      // Close loading toast
      loadingInstance.close();
      
      if (result && result.success) {
        showSuccessToast('Password changed successfully');
      } else {
        showFailToast((result && result.message) || 'Failed to change password');
      }
    } catch (error) {
      console.error('Failed to change password:', error);
      showToast.clear();
      showToast.fail('Failed to change password');
    }
  }).catch(() => {
    // Click cancel button
  });
};

const showBioDialog = () => {
  // Use ref to create reactive variables
  const newBioValue = ref(userBio.value);
  
  showDialog({
    title: 'Edit Bio',
    showCancelButton: true,
    confirmButtonText: 'Confirm',
    className: 'bio-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, 'Bio：'),
        h('textarea', {
          value: newBioValue.value,
          onInput: (e) => { newBioValue.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box; min-height: 100px; resize: vertical;'
        })
      ])
    ])
  }).then(async () => {
    // Click confirm button
    try {
      // Show loading toast
      const loadingInstance = showLoadingToast({
        message: 'Saving...',
        forbidClick: true,
        duration: 0
      });
      
      console.log('Update bio:', newBioValue.value);
      
      // Call API to update bio
      const result = await userStore.updateUserBio(newBioValue.value);
      
      // Close loading toast
      loadingInstance.close();
      
      if (result && result.success) {
        showSuccessToast('Bio updated successfully');
      } else {
        showFailToast((result && result.message) || 'Failed to update bio');
      }
    } catch (error) {
      console.error('Failed to update bio:', error);
      showToast.clear();
      showToast.fail('Failed to update bio');
    }
  }).catch(() => {
    // Click cancel button
  });
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.profile-container {
  padding-top: 56px;
  padding-bottom: 20px;
}

.avatar-group,
.info-group,
.security-group {
  margin-top: 12px;
}

.password-dialog .van-dialog__content {
  padding: 20px;
}

.password-form .form-item {
  margin-bottom: 15px;
  text-align: left;
}

.password-form .form-item span {
  display: block;
  margin-bottom: 5px;
  text-align: left;
}

.password-form .password-input {
  width: 100%;
  border: 1px solid #dcdee0;
  border-radius: 4px;
  padding: 8px;
  outline: none;
  box-sizing: border-box;
}
</style>