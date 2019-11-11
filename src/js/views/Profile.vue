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

            <profile-work-experiences :about="about" @update="updateHandler">
            </profile-work-experiences>

            <profile-associations :about="about" @update="updateHandler">
            </profile-associations>

            <profile-awards :about="about" @update="updateHandler">
            </profile-awards>
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
    import profileWorkExperiences from '@/components/profile/profile-work-experiences.vue'
    import profileAssociations from '@/components/profile/profile-associations.vue'
    import profileAwards from '@/components/profile/profile-awards.vue'
    import {getCookie} from "@/utils";
    import {scrollspy} from "@/profile";

    export default {
        name: "Profile",
        components: {
            profileAbout,
            profileDetails,
            profileContacts,
            profileSocials,
            profileLocations,
            profileEducations,
            profileWorkExperiences,
            profileAssociations,
            profileAwards,
        },
        data() {
            return {
                about: {}
            }
        },
        mounted() {
            fetch('/api/profile')
                .then(stream => stream.json())
                .then(data => this.about = data)
                .then(scrollspy.update_sections_id_with_position())
                .catch(error => console.error(error))
        },
        methods: {
            updateHandler(newAbout) {
                fetch('/api/profile', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(newAbout)
                })
                    .then(stream => stream.json())
                    .then(data => this.about = data)
                    .then(scrollspy.update_sections_id_with_position())
                    .catch(error => console.error(error))
            }
        }
    }
</script>