import Vue from 'vue'
import profileAbout from './components/profile-about.vue'

var app = new Vue({
    el: '#profile-edit',
    components: {
        profileAbout
    },
    mounted() {
        fetch('http://127.0.0.1:8000/users')
            .then(stream => stream.json())
            .then(data => console.log(data))
            .catch(error => console.error(error))
    }
})