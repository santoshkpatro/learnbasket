<script>
import Navbar from '../components/Navbar.vue'
export default {
    name: 'Home',
    components: {
        Navbar
    }
}
</script>

<template>
    <Navbar />
    <div class="container">
        <h1>Home Page</h1>
        <button class="btn btn-primary">Click me</button>
        <p class="text-primary">Click me</p>
    </div>
</template>