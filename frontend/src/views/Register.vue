<template>
  <div class="register-page">
    <van-nav-bar
      title="User Registration"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="register-container">
      <div class="register-logo">
        <van-image
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          round
        />
        <h2>News</h2>
      </div>
      
      <van-form @submit="onSubmit" class="register-form">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="Username"
            placeholder="Please enter username"
            :rules="[{ required: true, message: 'Please enter username' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="Password"
            maxlength="72"
            placeholder="Please enter password"
            :rules="[{ required: true, message: 'Please enter password' }]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="ConfirmPassword"
            maxlength="72"
            placeholder="Please enter password again"
            :rules="[
              { required: true, message: 'Please confirm password' },
              { validator: validatePassword, message: 'The two passwords do not match' }
            ]"
          />
        </van-cell-group>
        
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            Register
          </van-button>
        </div>
        
        <div class="login-link">
          Already have an account?<span @click="goToLogin">Log in</span>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useUserStore } from '../store/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');

// Validate that the two passwords match
const validatePassword = () => {
  return password.value === confirmPassword.value;
};

const onSubmit = async () => {
  // Show loading toast
  showToast({
    type: 'loading',
    message: 'Registering...',
    forbidClick: true,
    duration: 0
  });
  
  try {
    // Call API to register
    const result = await userStore.register({
      username: username.value,
      password: password.value
    });
    
    if (result.success) {
      showToast({
        type: 'success',
        message: result.message
      });
      
      router.push('/');
    } else {
      showToast({
        type: 'fail',
        message: result.message
      });
    }
  } catch (error) {
    showToast({
      type: 'fail',
      message: 'Registration failed. Please try again later'
    });
  }
};

const onClickLeft = () => {
  router.back();
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.register-container {
  padding-top: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.register-logo {
  margin: 40px 0;
  text-align: center;
}

.register-logo h2 {
  margin-top: 16px;
  color: #323233;
  font-size: 22px;
}

.register-form {
  width: 100%;
  padding: 0 16px;
}

.submit-btn {
  margin: 24px 16px;
}

.login-link {
  text-align: center;
  margin-top: 16px;
  color: #969799;
  font-size: 14px;
}

.login-link span {
  color: #1989fa;
}
</style>
