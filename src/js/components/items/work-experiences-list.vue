<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Experience"
                new-item-label="Add new experience"
                v-model="value"
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
                :deletable="selectedWorkExperience !== null"
                @cancel="hideModal"

                @delete="modalDeleteHandle"
                @ok="modalConfirmHandle"
                v-if="selectedWorkExperience !== undefined"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Company</label>
                <input id="country" type="text" v-model="selectedWorkExperience.company_name">

                <label for="state">Position</label>
                <input id="state" type="text" v-model="selectedWorkExperience.position">

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
                selectedWorkExperience: undefined,
                index: undefined,
                duration: {
                    start: new Date(2016, 9, 16),
                    end: new Date(2016, 9, 17)
                },
            }
        },
        methods: {
            showModal(index) {
                if (index === undefined) {
                    this.selectedWorkExperience = undefined
                } else if (index === null) {
                    this.selectedWorkExperience = {
                        company_name: '',
                        position: '',
                        duration: {
                            lower: new Date(2016, 9, 16),
                            upper: new Date(2016, 9, 17)
                        }
                    };
                    this.duration = {
                        start: new Date(2016, 9, 16),
                        end: new Date(2016, 9, 17)
                    }
                } else {
                    this.selectedWorkExperience = Object.assign({}, this.value[index]);
                    this.duration = {
                        start: this.$options.filters.stringToDate(this.value[index].duration.lower),
                        end: this.$options.filters.stringToDate(this.value[index].duration.upper)
                    }
                }
                this.index = index
            },
            modalConfirmHandle() {
                this.selectedWorkExperience.duration.lower = this.$options.filters.dateToString(this.duration.start);
                this.selectedWorkExperience.duration.upper = this.$options.filters.dateToString(this.duration.end);
                if (this.index === null) {
                    this.value.push(this.selectedWorkExperience)
                } else {
                    Vue.set(this.value, this.index, this.selectedWorkExperience)
                }
                this.hideModal()
            },
            modalDeleteHandle() {
                this.value.splice(this.index, 1);
                this.hideModal()
            },
            hideModal() {
                this.selectedWorkExperience = undefined
            },
        },
    }
</script>