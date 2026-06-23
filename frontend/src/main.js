import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'

// Import Vant component library
import { 
  Button, 
  NavBar, 
  Tabbar, 
  TabbarItem, 
  Tab, 
  Tabs, 
  List, 
  PullRefresh, 
  Cell, 
  CellGroup,
  Grid,
  GridItem,
  Empty,
  Form,
  Field,
  Image,
  Toast,
  Icon,
  Popup
} from 'vant'

// Import Vant styles
import 'vant/lib/index.css'

// Import global styles
import './style.css'

// Import internationalization
import { setupI18n } from './i18n'

const app = createApp(App)

// Settingsi18n
const i18n = setupI18n()
app.use(i18n)

// Register Vant components
app.use(Button)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Tab)
app.use(Tabs)
app.use(List)
app.use(PullRefresh)
app.use(Cell)
app.use(CellGroup)
app.use(Grid)
app.use(GridItem)
app.use(Empty)
app.use(Form)
app.use(Field)
app.use(Image)
app.use(Toast)
app.use(Icon)
app.use(Popup)

// Use router and state management
app.use(router)
app.use(pinia)

app.mount('#app')

// Initialize theme
import { useThemeStore } from './store/theme'
const themeStore = useThemeStore()
themeStore.initTheme()
