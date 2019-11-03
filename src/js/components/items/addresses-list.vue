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
                <input id="country" type="text" v-model="modalSelectedItem.country">

                <label for="state">State</label>
                <input id="state" type="text" v-model="modalSelectedItem.state">

                <label for="city">City</label>
                <input id="city" type="text" v-model="modalSelectedItem.city">
            </div>
        </modal>
    </div>
</template>

<script>
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
                    country: '',
                    state: '',
                    city: '',
                }
            },
            existingItem() {
                return Object.assign({}, this.modalItems[this.modalIndex])
            },
        }
    }
</script>

<style scoped>

</style>