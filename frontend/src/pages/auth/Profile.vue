<script>
import { authProfile } from '../../api/index'
export default {
    name: 'Profile',
    data() {
        return {
            profile: {}
        }
    },
    mounted() {
        authProfile()
            .then(({ data }) => {
                this.profile = data
            })
            .catch(e => {
                console.log(e)
            })
    }
}
</script>

<template>
    <div class="container">
        <h3>Profile</h3>
    </div>
</template>