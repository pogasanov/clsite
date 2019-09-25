import Vue from 'vue'
import ProfileBlock from './components/profile-block.vue'

var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    },
    components: {
        ProfileBlock
    }
})