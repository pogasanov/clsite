import Vue from 'vue'

export const modalManipulation = {
    model: {
        prop: 'value',
        event: 'change'
    },
    props: {
        value: Array,
    },
    data() {
        return {
            modalSelectedItem: undefined,
            modalIndex: undefined
        }
    },
    methods: {
        showModal(index) {
            this.modalIndex = index;
            this.modalSelectedItem = (this.isNew ? "" : this.value[index])
        },
        confirmTagModal() {
            if (this.isNew) {
                this.value.push(this.modalSelectedItem)
            } else {
                Vue.set(this.value, this.modalIndex, this.modalSelectedItem)
            }
            this.hideModal()
        },
        deleteTagModal() {
            this.value.splice(this.modalIndex, 1);
            this.hideModal()
        },
        hideModal() {
            this.modalSelectedItem = undefined
        },
    },
    computed: {
        isNew() {
            return this.modalIndex === null
        },
        isModalDisplayed() {
            return this.modalSelectedItem !== undefined
        }
    }
};
