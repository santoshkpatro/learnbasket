<script>
import { store } from './store'
import { authStatus } from './api/index'

export default {
  mounted() {
    const access_token_string = localStorage.getItem('access_token')
    if (access_token_string) {
      const access_token = JSON.parse(access_token_string)
      authStatus(access_token)
        .then(({ data }) => {
          store.setAuthentication(access_token)
        })
        .catch(err => {
          localStorage.removeItem('access_token')
        })
    }
  }
}
</script>

<template>
  <router-view></router-view>
</template>

<style>
</style>
