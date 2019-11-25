<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-awards"
            title="Awards"
    >
        <awards-list
                :edit-state="editState"
                v-model="awards"
        >
        </awards-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import awardsList from '@/components/items/awards-list.vue'

    export default {
        name: "profile-awards",
        components: {
            profileBlock,
            awardsList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                awards: [
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
                this.awards = data.awards
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        awards: this.awards,
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