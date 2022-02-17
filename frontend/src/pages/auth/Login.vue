<script>
import useVuelidate from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'
import { login } from '../../api/index'
import { store } from '../../store'

export default {
    setup() {
        return {
            v$: useVuelidate()
        }
    },
    name: 'Login',
    data() {
        return {
            store,
            email: '',
            password: '',
            formError: false,
            isLoading: false,
            google_client_id: '',
            google_redirect_uri: '',
            scope: ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
            google_url: 'https://accounts.google.com/o/oauth2/v2/auth'
        }
    },
    mounted() {
        this.google_client_id = import.meta.env.VITE_GOOGLE_CLIENT_ID
        this.google_redirect_uri = import.meta.env.VITE_GOOGLE_OAUTH_REDIRECT_URI
    },
    computed: {
        google_oauth_url() {
            const gURL = new URL(this.google_url)
            gURL.searchParams.append('client_id', this.google_client_id)
            gURL.searchParams.append('redirect_uri', this.google_redirect_uri)
            gURL.searchParams.append('response_type', 'code')
            gURL.searchParams.append('scope', this.scope.join(' '))
            gURL.searchParams.append('access_type', 'offline')
            gURL.searchParams.append('state', JSON.stringify({
                mode: 'login',
                redirect: this.$route.query.redirect
            }))

            return gURL.href
        }
    },
    validations() {
        return {
            email: {
                required,
                email
            },
            password: {
                required
            }
        }
    },
    methods: {
        async handleSubmit() {
            const isFormCorrect = await this.v$.$validate()

            if (!isFormCorrect) {
                return
            }

            login({
                email: this.email,
                password: this.password,
            })
                .then(({ data }) => {
                    const { access_token } = data
                    this.store.setAuthentication(access_token)

                    if (this.$route.query.redirect) {
                        const redirect_url = this.$route.query.redirect
                        this.$router.push({ path: redirect_url })
                    } else {
                        this.$router.push({ name: 'Home' })
                    }
                })
                .catch((e) => {
                    this.formError = true
                })
        },
    },
}
</script>

<template>
    <div class="container">
        <div class="d-flex justify-content-center align-items-center" style="height: 70vh;">
            <form @submit.prevent="handleSubmit">
                <div class="alert alert-danger" v-if="formError" role="alert">Invalid credentials</div>
                <h1>Login</h1>
                <div class="d-grid gap-2">
                    <a class="btn btn-danger" :href="google_oauth_url" target="_blank">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            fill="currentColor"
                            class="bi bi-google mb-1 me-1"
                            viewBox="0 0 16 16"
                        >
                            <path
                                d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z"
                            />
                        </svg>
                        Login with Google
                    </a>
                </div>
                <hr />
                <BaseFloatingInput
                    label="Email Address"
                    v-model="email"
                    :message="v$.email.$error ? v$.email.$errors[0].$message : ''"
                />
                <BaseFloatingInput
                    label="Password"
                    v-model="password"
                    type="password"
                    :message="v$.password.$error ? v$.password.$errors[0].$message : ''"
                />
                <div class="d-grid gap-2">
                    <button class="btn btn-primary">Login</button>
                </div>
            </form>
        </div>
    </div>
</template>
