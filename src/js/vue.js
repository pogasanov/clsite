import Vue from 'vue'
import Profile from '@/views/Profile.vue'
import moment from 'moment'

Vue.filter('dateToString', function (value) {
    return moment(value).format('YYYY-MM-DD')
});
Vue.filter('stringToDate', function (value) {
    return moment(value).toDate()
});
Vue.filter('dateDiff', function (date1, date2) {
    return moment.duration(moment(date1).diff(moment(date2))).humanize()
})

new Vue({
    render: h => h(Profile),
    components: {Profile}
}).$mount('#profile-edit');