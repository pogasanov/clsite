<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-workexperiences"
            title="Professional Associations"
    >
        <associations-list
                :edit-state="editState"
                v-model="associations"
        >
        </associations-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import associationsList from '@/components/items/associations-list.vue'

    export default {
        name: "profile-associations",
        components: {
            profileBlock,
            associationsList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                associations: [
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
                this.associations = data.organizations
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        organizations: this.associations,
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