<script>
import { verifyEmail } from '../../api/index'

export default {
    name: 'EmailVerify',
    data() {
        return {
            isVerified: false
        }
    },
    mounted() {
        if (this.$route.query.verify_token) {
            verifyEmail(this.$route.query.verify_token)
                .then(({ data }) => {
                    this.isVerified = true
                })
                .catch(e => {
                    this.isVerified = false
                })
        }
    }
}
</script>

<template>
    <div class="alert alert-success mt-3 mx-3" role="alert" v-if="isVerified">
        <h4 class="alert-heading">Email verified!</h4>
        <p>Aww yes,</p>
        <p>Thankx, for verifying the email.</p>
        <hr />
        <p class="mb-0">
            <router-link :to="{ name: 'Login' }">Click Here</router-link>to login.
        </p>
    </div>
    <div class="alert alert-warning mt-3 mx-3" role="alert" v-else>
        <h4 class="alert-heading">Unable to verify!</h4>
        <p>Aww sorry,</p>
        <p>We are unable to verify as either the link is invalid or expired</p>
        <hr />
        <p class="mb-0">
            <router-link :to="{ name: 'Login' }">Click Here</router-link>to raise issue.
        </p>
    </div>
</template>