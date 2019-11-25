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
                :options="statesByCountry"
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
    import profileBlock from '@/components/commons/profile-block.vue'
    import viewableSelect from '@/components/inputs/viewable-select.vue'
    import viewableInput from '@/components/inputs/viewable-input.vue'
    import {getAllCountries, getStatesByCountry} from "@/utils";

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

                allCountries: getAllCountries()
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
        created() {
            this.updateData(this.about)
        },
        computed: {
            statesByCountry() {
                return getStatesByCountry(this.country)
            }
        },
        watch: {
            about(newAbout, oldAbout) {
                this.updateData(newAbout)
            },
            country(newCountry, oldCountry) {
                if (this.statesByCountry.indexOf(this.state) === -1) {
                    this.state = this.statesByCountry[0]
                }
            }
        }
    }
</script>