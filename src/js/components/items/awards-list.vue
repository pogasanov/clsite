<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Awards"
                new-item-label="Add new award"
                v-model="modalItems"
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
                :deletable="!isNew"
                @cancel="hideModal"

                @delete="deleteModal"
                @ok="confirmModal"
                v-if="isModalDisplayed"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Title</label>
                <input id="country" type="text" v-model="modalSelectedItem.title">

                <label for="state">Presented by</label>
                <input id="state" type="text" v-model="modalSelectedItem.presented_by">

                <label for="year">Year</label>
                <input id="year" type="number" v-model="modalSelectedItem.year">
            </div>
        </modal>
    </div>
</template>

<script>
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import {modalManipulation} from "@/mixins";

    export default {
        name: "awards-list",
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
                return {}
            },
        },
    }
</script>