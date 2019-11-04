<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Addresses"
                new-item-label="Add new address"
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
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Country</label>
                <select id="country" v-model="modalSelectedItem.country">
                    <option :value="country" v-for="country in allCountries">{{country}}</option>
                </select>

                <label for="state">State</label>
                <select id="state" v-model="modalSelectedItem.state">
                    <option :value="state" v-for="state in getStatesByCountry(modalSelectedItem.country)">{{state}}
                    </option>
                </select>

                <label for="city">City</label>
                <input id="city" type="text" v-model="modalSelectedItem.city">
            </div>
        </modal>
    </div>
</template>

<script>
    import languages_states_choices from '../../../../app/clsite/choices/countries+states'
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import {modalManipulation} from "@/mixins";

    export default {
        name: "addresses-list",
        mixins: [modalManipulation],
        components: {
            viewableList,
            modal
        },
        props: {
            editState: Boolean,
        },
        methods: {
            emptyItem() {
                return {
                    country: 'United States of America',
                    state: '',
                    city: '',
                }
            },
            getStatesByCountry(country) {
                return languages_states_choices.find(el => {
                    return el.name === this.modalSelectedItem.country
                }).states
            }
        },
        computed: {
            allCountries() {
                return languages_states_choices.map(el => el.name)
            }
        }
    }
</script>