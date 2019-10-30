import Vue from 'vue'
import Profile from '@/views/Profile.vue'
import moment from 'moment'

Vue.filter('formatDate', function (value) {
    return moment(value).format('YYYY-MM-DD')
});

new Vue({
    render: h => h(Profile),
    components: {Profile}
}).$mount('#profile-edit');