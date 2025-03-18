import { createApp } from 'vue'
import App from './App.vue'
import 'uikit/dist/css/uikit.min.css';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons.min.js';

UIkit.use(Icons);
createApp(App).mount('#app')
