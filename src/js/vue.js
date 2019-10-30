import Vue from 'vue'
import Profile from '@/views/Profile.vue'
import moment from 'moment'

Vue.filter('dateToString', function (value) {
    return moment(value).format('YYYY-MM-DD')
});
Vue.filter('stringToDate', function (value) {
    return moment(value).toDate()
});

new Vue({
    render: h => h(Profile),
    components: {Profile}
}).$mount('#profile-edit');