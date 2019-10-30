<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Educations"
                new-item-label="Add new education"
                v-model="value"
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
                :deletable="selectedEducation !== null"
                @cancel="hideModal"

                @delete="modalDeleteHandle"
                @ok="modalConfirmHandle"
                v-if="selectedEducation !== undefined"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Name</label>
                <input id="country" type="text" v-model="selectedEducation.school">

                <label for="state">Degree</label>
                <input id="state" type="text" v-model="selectedEducation.degree">

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
    import Vue from 'vue'

    Vue.component('date-picker', DatePicker);

    export default {
        name: "educations-list",
        components: {
            DatePicker,
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
                graduation_date: new Date(2016, 9, 16),
            }
        },
        methods: {
            showModal(index) {
                if (index === undefined) {
                    this.selectedEducation = undefined
                } else if (index === null) {
                    this.selectedEducation = {
                        school: '',
                        degree: '',
                        graduation_date: '',
                    };
                    this.graduation_date = new Date(2016, 9, 16)
                } else {
                    this.selectedEducation = Object.assign({}, this.value[index]);
                    this.graduation_date = this.$options.filters.stringToDate(this.value[index].graduation_date)
                }
                this.index = index
            },
            modalConfirmHandle() {
                this.selectedEducation.graduation_date = this.$options.filters.dateToString(this.graduation_date);
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