<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Experience"
                new-item-label="Add new experience"
                v-model="modalItems"
        >
            <template v-slot:default="slotProps">
                <ul class="list list--condensed">
                    <li class="list__item"><span class="muted">Company:</span> {{ slotProps.item.company_name }}</li>
                    <li class="list__item"><span class="muted">Position:</span> {{ slotProps.item.position }}</li>
                    <li class="list__item"><span class="muted">Duration:</span> {{ slotProps.item.duration.lower }} - {{
                        slotProps.item.duration.upper }}
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
            <h3 slot="header">Edit work experience</h3>
            <div slot="body">
                <label for="country">Company</label>
                <input id="country" type="text" v-model="modalSelectedItem.company_name">

                <label for="state">Position</label>
                <input id="state" type="text" v-model="modalSelectedItem.position">

                <label for="duration">Duration</label>
                <date-picker
                        id="duration"
                        mode="range"
                        v-model="duration"
                />
            </div>
        </modal>
    </div>
</template>

<script>
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue"
    import DatePicker from 'v-calendar/lib/components/date-picker.umd'
    import {modalManipulation} from "@/mixins";
    import Vue from 'vue'

    Vue.component('date-picker', DatePicker);

    export default {
        name: "educations-list",
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
                duration: {
                    start: new Date(2016, 9, 16),
                    end: new Date(2016, 9, 17)
                },
            }
        },
        methods: {
            emptyItem() {
                return {
                    company_name: '',
                    position: '',
                    duration: {
                        lower: new Date(2016, 9, 16),
                        upper: new Date(2016, 9, 17),
                    }
                }
            },
            showModal(index) {
                modalManipulation.methods.showModal.call(this, index);
                if (!this.isNew) {
                    this.duration = {
                        start: this.$options.filters.stringToDate(this.modalSelectedItem.duration.lower),
                        end: this.$options.filters.stringToDate(this.modalSelectedItem.duration.upper)
                    }
                } else {
                    this.duration = {
                        start: new Date(2016, 9, 16),
                        end: new Date(2016, 9, 17),
                    }
                }
            },
            confirmModal() {
                this.modalSelectedItem.duration.lower = this.$options.filters.dateToString(this.duration.start);
                this.modalSelectedItem.duration.upper = this.$options.filters.dateToString(this.duration.end);
                modalManipulation.methods.confirmModal.call(this)
            },
        },
    }
</script>