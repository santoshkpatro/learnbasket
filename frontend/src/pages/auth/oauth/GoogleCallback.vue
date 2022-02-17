<script>
import { googleCallback } from '../../../api/index.js'
import { store } from '../../../store.js'

export default {
    name: 'GoogleCallbackHandle',
    data() {
        return {
            code: '',
            showLogin: false
        }
    },
    methods: {
        login(redirect = null) {
            googleCallback(this.code, 'login')
                .then(({ data }) => {
                    console.log(redirect)
                    store.setAuthentication(data.access_token)
                    if (redirect) {
                        this.$router.push({ path: redirect })
                    } else {
                        this.$router.push({ name: 'Home' })
                    }

                })
                .catch(e => console.log(e))
        },
        register() {
            googleCallback(this.code, 'register')
                .then(({ data }) => {
                    this.showLogin = true
                })
                .catch(e => console.log(e))
        }
    },
    mounted() {
        this.code = this.$route.query.code
        const options = JSON.parse(this.$route.query.state)

        if (options.mode === 'login') {
            if ('redirect' in options) {
                this.login(options.redirect)
            } else {
                this.login()
            }
        } else {
            this.register()
        }
    }
}
</script>

<template>
    <div
        class="d-flex justify-content-center align-items-center"
        style="height: 70vh"
        v-if="!showLogin"
    >
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div class="container" v-else>
        <div class="alert alert-success" role="alert">
            <h4 class="alert-heading">Well done!</h4>
            <p>Aww yes, You have created your account!</p>
            <hr />
            <router-link class="btn btn-sm btn-primary" :to="{ name: 'Login' }">Click here to login</router-link>
        </div>
    </div>
</template>