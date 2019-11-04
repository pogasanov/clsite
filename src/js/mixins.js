import Vue from 'vue'

export const modalManipulation = {
    model: {
        prop: 'modalItems',
        event: 'change'
    },
    props: {
        modalItems: Array,
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
            this.modalSelectedItem = (this.isNew ? this.emptyItem() : this.existingItem())
        },
        confirmModal() {
            if (this.isNew) {
                this.modalItems.push(this.modalSelectedItem)
            } else {
                Vue.set(this.modalItems, this.modalIndex, this.modalSelectedItem)
            }
            this.hideModal()
        },
        deleteModal() {
            this.modalItems.splice(this.modalIndex, 1);
            this.hideModal()
        },
        hideModal() {
            this.modalSelectedItem = undefined
        },

        existingItem() {
            if (typeof this.modalItems[this.modalIndex] === 'object') {
                return Object.assign({}, this.modalItems[this.modalIndex])
            }
            return this.modalItems[this.modalIndex]
        },
        emptyItem() {
            return ""
        },
    },
    computed: {
        isNew() {
            return this.modalIndex === null
        },
        isModalDisplayed() {
            return this.modalSelectedItem !== undefined
        },
    }
};
