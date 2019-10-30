<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Associations"
                new-item-label="Add new associations"
                v-model="value"
        >
            <template v-slot:default="slotProps">
                <ul class="list list--condensed">
                    <li class="list__item"><span class="muted">Name:</span> {{ slotProps.item.name }}</li>
                    <li class="list__item"><span class="muted">Position:</span> {{ slotProps.item.position }}</li>
                    <li class="list__item"><span class="muted">Duration:</span> {{ slotProps.item.duration.lower }} - {{
                        slotProps.item.duration.upper }}
                    </li>
                </ul>
            </template>
        </viewable-list>

        <modal
                :deletable="selectedAssociation !== null"
                @cancel="hideModal"

                @delete="modalDeleteHandle"
                @ok="modalConfirmHandle"
                v-if="selectedAssociation !== undefined"
        >
            <h3 slot="header">Edit address</h3>
            <div slot="body">
                <label for="country">Company</label>
                <input id="country" type="text" v-model="selectedAssociation.name">

                <label for="state">Position</label>
                <input id="state" type="text" v-model="selectedAssociation.position">

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
        name: "associations-list",
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
                selectedAssociation: undefined,
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
                    this.selectedAssociation = undefined
                } else if (index === null) {
                    this.selectedAssociation = {
                        name: '',
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
                    this.selectedAssociation = Object.assign({}, this.value[index]);
                    this.duration = {
                        start: this.$options.filters.stringToDate(this.value[index].duration.lower),
                        end: this.$options.filters.stringToDate(this.value[index].duration.upper)
                    }
                }
                this.index = index
            },
            modalConfirmHandle() {
                this.selectedAssociation.duration.lower = this.$options.filters.dateToString(this.duration.start);
                this.selectedAssociation.duration.upper = this.$options.filters.dateToString(this.duration.end);
                if (this.index === null) {
                    this.value.push(this.selectedAssociation)
                } else {
                    Vue.set(this.value, this.index, this.selectedAssociation)
                }
                this.hideModal()
            },
            modalDeleteHandle() {
                this.value.splice(this.index, 1);
                this.hideModal()
            },
            hideModal() {
                this.selectedAssociation = undefined
            },
        },
    }
</script>