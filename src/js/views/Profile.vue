<template>
    <main class="profile" id="profile-edit">
        <div class="container">
            <profile-about :about="about" @update="updateHandler">
            </profile-about>
        </div>
    </main>
</template>

<script>
    import profileAbout from '@/components/profile-about.vue'
    import {getCookie} from "@/utils";

    export default {
        name: "Profile",
        components: {
            profileAbout
        },
        data() {
            return {
                about: {}
            }
        },
        mounted() {
            fetch('/api/profiles/admin/')
                .then(stream => stream.json())
                .then(data => this.about = data)
                .catch(error => console.error(error))
        },
        methods: {
            updateHandler(newAbout) {
                fetch('/api/profiles/admin/', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(newAbout)
                })
                    .then(stream => stream.json())
                    .then(data => this.about = data)
                    .catch(error => console.error(error))
            }
        }
    }
</script>