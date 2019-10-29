<template>
    <div v-if="editState || value">
        <h6 class="text-header">{{ label }}</h6>
        <ul :class="editState ? 'list--selectable' : ''" class="list">
            <li @click="onItemClicked(index)" class="list__item"
                v-for="(item, index) in value">
                <slot :item="item"></slot>
            </li>
            <li @click="onItemClicked(null)" class="list__item" v-if="editState">
                Add new language
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "viewable-list",
        props: {
            editState: Boolean,
            value: Array,
            label: String,
        },
        methods: {
            onItemClicked(index) {
                if (!this.editState) {
                    return
                }
                this.$emit('item-clicked', index)
            }
        }
    }
</script>