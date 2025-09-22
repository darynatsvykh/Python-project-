// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import LoginPage from '../pages/LoginPage.vue';
import SignPage from '../pages/SignUpPage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Login Page', component: LoginPage },
        { path: '/other/', name: 'Other Page', component: OtherPage },
        { path: '/home/', name: 'Main Page', component: MainPage },
        { path: '/signup/', name: 'Sign Page', component: SignPage },
        { path: '/hobbies', name: 'Hobbies Page', component: HobbiesPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
    ]
})

export default router
