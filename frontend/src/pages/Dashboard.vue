<script>
import Navbar from "../components/Navbar.vue"

export default {
    name: 'Dashboard',
    components: {
        Navbar
    }
}
</script>

<template>
    <Navbar />
    <div class="container">
        <nav class="nav">
            <a class="nav-link active" aria-current="page" href="#">Overview</a>
            <a class="nav-link" href="#">Link</a>
            <a class="nav-link" href="#">Link</a>
            <a class="nav-link">Disabled</a>
        </nav>
        <router-view></router-view>
    </div>
</template>

<style>
.nav-link,
.nav-link:active,
.nav-link:hover {
    color: black;
}

.active {
    color: black;
    border-bottom: 2px solid black;
}
</style>