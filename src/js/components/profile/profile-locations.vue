<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-addresses"
            title="Physical locations"
    >
        <addresses-list
                :edit-state="editState"
                v-model="addresses"
        >
        </addresses-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import addressesList from '@/components/items/addresses-list.vue'

    export default {
        name: "profile-locations",
        components: {
            profileBlock,
            addressesList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                addresses: [
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
                this.addresses = data.addresses
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        addresses: this.addresses,
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