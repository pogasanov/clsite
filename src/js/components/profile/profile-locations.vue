<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-addresses"
            title="Physical locations"
    >
        <viewable-select
                :edit-state="editState"
                label="Country"
                v-model="country"
                :options="allCountries"
        >
        </viewable-select>

        <viewable-select
                :edit-state="editState"
                label="State"
                v-model="state"
                :options="getStatesByCountry"
        >
        </viewable-select>

        <viewable-input
                :edit-state="editState"
                label="City"
                v-model="city"
        >
        </viewable-input>
    </profile-block>
</template>

<script>
    import languages_states_choices from '../../../../app/clsite/choices/countries+states'
    import profileBlock from '@/components/commons/profile-block.vue'
    import viewableSelect from '@/components/inputs/viewable-select.vue'
    import viewableInput from '@/components/inputs/viewable-input.vue'

    export default {
        name: "profile-locations",
        components: {
            profileBlock,
            viewableSelect,
            viewableInput,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                country: "",
                state: "",
                city: "",
            }
        },
        methods: {
            updateData(data) {
                if (data.address) {
                    this.country = data.address.country
                    this.state = data.address.state
                    this.city = data.address.city
                }
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        address: {
                            country: this.country,
                            state: this.state,
                            city: this.city,
                        },
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about);
                this.editState = !this.editState
            },
        },
        computed: {
            allCountries() {
                return languages_states_choices.map(el => el.name)
            },
            getStatesByCountry() {
                const choice = languages_states_choices.find(el => {
                    return el.name === this.country
                })
                return choice ? choice.states : []
            },
        },
        created() {
            this.updateData(this.about)
        },
        watch: {
            about(newAbout, oldAbout) {
                this.updateData(newAbout)
            },
            country(newCountry, oldCountry) {
                if (this.getStatesByCountry.indexOf(this.state) === -1) {
                    this.state = this.getStatesByCountry[0]
                }
            }
        }
    }
</script>