<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Awards"
                new-item-label="Add new award"
                v-model="value"
        >
            <template v-slot:default="slotProps">
                <ul class="list list--condensed">
                    <li class="list__item"><span class="muted">Title:</span> {{ slotProps.item.title }}</li>
                    <li class="list__item"><span class="muted">Presented by:</span> {{ slotProps.item.presented_by }}
                    </li>
                    <li class="list__item"><span class="muted">Year:</span> {{
                        slotProps.item.year }}
                    </li>
                </ul>
            </template>
        </viewable-list>

        <modal
                :deletable="selectedEducation !== null"
                @cancel="hideModal"

                @delete="modalDeleteHandle"
                @ok="modalConfirmHandle"
                v-if="selectedEducation !== undefined"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Title</label>
                <input id="country" type="text" v-model="selectedEducation.title">

                <label for="state">Presented by</label>
                <input id="state" type="text" v-model="selectedEducation.presented_by">

                <label for="year">Year</label>
                <input id="year" type="number" v-model="selectedEducation.year">
            </div>
        </modal>
    </div>
</template>

<script>
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import Vue from 'vue'

    export default {
        name: "awards-list",
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
                selectedEducation: undefined,
                index: undefined,
            }
        },
        methods: {
            showModal(index) {
                if (index === undefined) {
                    this.selectedEducation = undefined
                } else if (index === null) {
                    this.selectedEducation = {};
                } else {
                    this.selectedEducation = Object.assign({}, this.value[index]);
                }
                this.index = index
            },
            modalConfirmHandle() {
                if (this.index === null) {
                    this.value.push(this.selectedEducation)
                } else {
                    Vue.set(this.value, this.index, this.selectedEducation)
                }
                this.hideModal()
            },
            modalDeleteHandle() {
                this.value.splice(this.index, 1);
                this.hideModal()
            },
            hideModal() {
                this.selectedEducation = undefined
            },
        },
    }
</script>