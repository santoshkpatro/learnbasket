<script>
import { store } from '../store'

export default {
    data() {
        return {
            store
        }
    },
    methods: {
        handleLogout() {
            store.removeAuthentication()
        }
    }
}
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <router-link class="navbar-brand" :to="{ name: 'Home' }">Learn Basket</router-link>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'About' }">About</router-link>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled">Disabled</a>
                    </li>
                </ul>
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'Overview' }">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="btn btn-primary mx-2"
                            v-if="!store.isAuthenticated"
                            :to="{ name: 'Register' }"
                        >Register</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="btn btn-primary mx-2"
                            v-if="!store.isAuthenticated"
                            :to="{ name: 'Login' }"
                        >Login</router-link>
                    </li>
                    <li class="nav-item dropdown" v-if="store.isAuthenticated">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="navbarDropdown"
                            role="button"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            <img
                                src="https://avatars.dicebear.com/api/identicon/skpatro23.svg"
                                alt="NA"
                                height="30"
                                width="30"
                                style="border-radius: 50%; border: 1px solid;"
                            />
                        </a>
                        <ul
                            class="dropdown-menu dropdown-menu-end"
                            aria-labelledby="navbarDropdown"
                        >
                            <li>
                                <router-link class="dropdown-item" :to="{ name: 'Profile' }">Profile</router-link>
                            </li>
                            <li>
                                <router-link
                                    class="dropdown-item"
                                    :to="{ name: 'Profile' }"
                                >Password Change</router-link>
                            </li>
                            <li>
                                <hr class="dropdown-divider" />
                            </li>
                            <li>
                                <a class="dropdown-item" href="#" @click="handleLogout">Logout</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style>
/* .router-link-active {
    border: 1px solid;
    border-radius: 8px;
} */
</style>