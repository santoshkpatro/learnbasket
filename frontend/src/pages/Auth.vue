<script>
import Navbar from '../components/Navbar.vue'
export default {
    name: 'Auth',
    components: {
        Navbar
    }
}
</script>

<template>
    <Navbar />
    <router-view></router-view>
</template>