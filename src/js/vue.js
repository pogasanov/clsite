import Vue from 'vue'
import profileAbout from './components/profile-about.vue'

var app = new Vue({
    el: '#profile-edit',
    components: {
        profileAbout
    },
    data() {
        return {
            about: {}
        }
    },
    mounted() {
        fetch('http://127.0.0.1:8000/api/profiles/admin/')
            .then(stream => stream.json())
            .then(data => this.about = data)
            .catch(error => console.error(error))
    },
    methods: {
        updateHandler(newAbout) {
            fetch('http://127.0.0.1:8000/api/profiles/admin/', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(newAbout)
            })
                .then(stream => stream.json())
                .then(data => this.about = data)
                .catch(error => console.error(error))
        }
    }
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');