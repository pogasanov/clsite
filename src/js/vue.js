import Vue from 'vue'
import Profile from '@/views/Profile.vue'

new Vue({
    render: h => h(Profile),
    components: {Profile}
}).$mount('#profile-edit');