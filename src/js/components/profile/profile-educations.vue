<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-educations"
            title="Educations"
    >
        <educations-list
                :edit-state="editState"
                v-model="educations"
        >
        </educations-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import educationsList from '@/components/items/educations-list.vue'

    export default {
        name: "profile-educations",
        components: {
            profileBlock,
            educationsList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                educations: [
                    {
                        name: 'dummy',
                        proficiency_level: 'dunno'
                    }, {
                        name: 'language',
                        proficiency_level: 'dunno'
                    }
                ],
            }
        },
        methods: {
            updateData(data) {
                this.educations = data.educations
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        educations: this.educations,
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about);
                this.editState = !this.editState
            },
        },
        created() {
            this.updateData(this.about)
        },
        watch: {
            about(newAbout, oldAbout) {
                this.updateData(newAbout)
            }
        }
    }
</script>