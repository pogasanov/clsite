<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-workexperiences"
            title="Work experience"
    >
        <work-experiences-list
                :edit-state="editState"
                v-model="workExperiences"
        >
        </work-experiences-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import workExperiencesList from '@/components/items/work-experiences-list.vue'

    export default {
        name: "profile-work-experiences",
        components: {
            profileBlock,
            workExperiencesList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                workExperiences: [
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
                this.workExperiences = data.work_experiences
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        work_experiences: this.workExperiences,
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