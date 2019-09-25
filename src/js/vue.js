import Vue from 'vue'
import profileAbout from './components/profile-about.vue'

var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    },
    components: {
        profileAbout
    }
})