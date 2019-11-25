<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Jurisdictions"
                new-item-label="Add new jurisdiction"
                v-model="modalItems"
        >
            <template v-slot:default="slotProps">
                <ul class="list list--condensed">
                    <li class="list__item"><span class="muted">Country:</span> {{ slotProps.item.country }}</li>
                    <li class="list__item"><span class="muted">State:</span> {{ slotProps.item.state }}</li>
                    <li class="list__item"><span class="muted">City:</span> {{ slotProps.item.city }}</li>
                </ul>
            </template>
        </viewable-list>

        <modal
                :deletable="!isNew"
                @cancel="hideModal"

                @delete="deleteModal"
                @ok="confirmModal"
                v-if="isModalDisplayed"
        >
            <h3 slot="header">Edit jurisdiction</h3>
            <div slot="body">
                <label for="country">Country</label>
                <select
                        id="country"
                        v-model="modalSelectedItem.country"
                >
                    <option :value="option" v-for="option in allCountries">{{option}}</option>
                </select>

                <label for="state">State</label>
                <select
                        id="state"
                        v-model="modalSelectedItem.state"
                >
                    <option :value="option" v-for="option in statesByCountry">{{option}}</option>
                </select>

                <label for="city">City</label>
                <input id="city" type="text" v-model="modalSelectedItem.city">
            </div>
        </modal>
    </div>
</template>

<script>
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import DatePicker from 'v-calendar/lib/components/date-picker.umd'
    import {modalManipulation} from "@/mixins";
    import {getAllCountries, getStatesByCountry} from "@/utils";

    export default {
        name: "jurisdictions-list",
        mixins: [modalManipulation],
        components: {
            DatePicker,
            viewableList,
            modal
        },
        props: {
            editState: Boolean,
        },
        data() {
            return {
                allCountries: getAllCountries()
            }
        },
        methods: {
            emptyItem() {
                return {
                    country: '',
                    state: '',
                    city: ''
                }
            },
        },
        computed: {
            statesByCountry() {
                return getStatesByCountry(this.modalSelectedItem.country)
            }
        },
        watch: {
            'modalSelectedItem.country': function() {
                if (this.modalSelectedItem && this.statesByCountry.indexOf(this.modalSelectedItem.state) === -1) {
                    this.modalSelectedItem.state = this.statesByCountry[0]
                }
            }
        }
    }
</script>