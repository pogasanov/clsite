<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Educations"
                new-item-label="Add new education"
                v-model="modalItems"
        >
            <template v-slot:default="slotProps">
                <ul class="list list--condensed">
                    <li class="list__item"><span class="muted">Name:</span> {{ slotProps.item.school }}</li>
                    <li class="list__item"><span class="muted">Degree:</span> {{ slotProps.item.degree }}</li>
                    <li class="list__item"><span class="muted">Date of graduation:</span> {{
                        slotProps.item.graduation_date }}
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
            <h3 slot="header">Edit education</h3>
            <div slot="body">
                <label for="country">Name</label>
                <input id="country" type="text" v-model="modalSelectedItem.school">

                <label for="state">Degree</label>
                <input id="state" type="text" v-model="modalSelectedItem.degree">

                <label for="graduation_date">Date of graduation</label>
                <date-picker
                        id="graduation_date"
                        v-model="graduation_date"
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
                graduation_date: new Date(2016, 9, 16),
            }
        },
        methods: {
            emptyItem() {
                return {
                    school: '',
                    degree: '',
                    graduation_date: ''
                }
            },
            showModal(index) {
                modalManipulation.methods.showModal.call(this, index);
                if (!this.isNew) {
                    this.graduation_date = this.$options.filters.stringToDate(this.modalSelectedItem.graduation_date)
                } else {
                    this.graduation_date = new Date(2016, 9, 16)
                }
            },
            confirmModal() {
                this.modalSelectedItem.graduation_date = this.$options.filters.dateToString(this.graduation_date);
                modalManipulation.methods.confirmModal.call(this)
            },
        },
    }
</script>