import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import 'bootstrap/dist/js/bootstrap.min.js'
import './assets/main.scss'

const app = createApp(App)

const components = import.meta.globEager('./components/base/*.vue')

Object.entries(components).forEach(([path, definition]) => {
  // Get name of component, based on filename
  // "./components/Fruits.vue" will become "Fruits"
  const componentName = path
    .split('/')
    .pop()
    .replace(/\.\w+$/, '')

  // Register component on this Vue instance
  app.component(componentName, definition.default)
})

app.use(router)
app.use(createPinia())

app.mount('#app')
