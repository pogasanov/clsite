<template>
    <main class="profile" id="profile-edit">
        <div class="container">
            <profile-about :about="about" @update="updateHandler">
            </profile-about>

            <profile-details :about="about" @update="updateHandler">
            </profile-details>

            <profile-contacts :about="about" @update="updateHandler">
            </profile-contacts>

            <profile-socials :about="about" @update="updateHandler">
            </profile-socials>

            <profile-locations :about="about" @update="updateHandler">
            </profile-locations>

            <profile-educations :about="about" @update="updateHandler">
            </profile-educations>
        </div>
    </main>
</template>

<script>
    import profileAbout from '@/components/profile/profile-about.vue'
    import profileDetails from '@/components/profile/profile-details.vue'
    import profileContacts from '@/components/profile/profile-contacts.vue'
    import profileSocials from '@/components/profile/profile-socials.vue'
    import profileLocations from '@/components/profile/profile-locations.vue'
    import profileEducations from '@/components/profile/profile-educations.vue'
    import {getCookie} from "@/utils";

    export default {
        name: "Profile",
        components: {
            profileAbout,
            profileDetails,
            profileContacts,
            profileSocials,
            profileLocations,
            profileEducations,
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