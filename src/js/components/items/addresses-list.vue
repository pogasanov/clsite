<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showLanguageModal"
                label="Addresses"
                new-item-label="Add new address"
                v-model="value"
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
                :deletable="selectedAddress !== null"
                @cancel="hideModal"

                @delete="deleteLanguageModal"
                @ok="confirmLanguageModal"
                v-if="selectedAddress !== undefined"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Country</label>
                <input id="country" type="text" v-model="selectedAddress.country">

                <label for="state">State</label>
                <input id="state" type="text" v-model="selectedAddress.state">

                <label for="city">City</label>
                <input id="city" type="text" v-model="selectedAddress.city">
            </div>
        </modal>
    </div>
</template>

<script>
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import Vue from 'vue'

    export default {
        name: "addresses-list",
        components: {
            viewableList,
            modal
        },
        model: {
            prop: 'value',
            event: 'change'
        },
        props: {
            value: Array,
            editState: Boolean,
        },
        data() {
            return {
                selectedAddress: undefined,
                index: undefined,
            }
        },
        methods: {
            showLanguageModal(index) {
                if (index === undefined) {
                    this.selectedAddress = undefined
                } else if (index === null) {
                    this.selectedAddress = {
                        country: '',
                        state: '',
                        city: '',
                    }
                } else {
                    this.selectedAddress = Object.assign({}, this.value[index])
                }
                this.index = index
            },
            confirmLanguageModal() {
                if (this.index === null) {
                    this.value.push(this.selectedAddress)
                } else {
                    Vue.set(this.value, this.index, this.selectedAddress)
                }
                this.hideModal()
            },
            deleteLanguageModal() {
                this.value.splice(this.index, 1);
                this.hideModal()
            },
            hideModal() {
                this.selectedAddress = undefined
            },
        }
    }
</script>

<style scoped>

</style>