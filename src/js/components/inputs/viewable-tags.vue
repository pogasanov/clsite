<template>
    <div v-if="editState || value">
        <h6 class="text-header">{{ label }}</h6>
        <ul class="tag-container">
            <li @click="onItemClicked(index)" class="tag"
                v-for="(item, index) in value">
                {{ item }}
            </li>
            <li @click="onItemClicked(null)" class="tag tag--outline" v-if="editState">
                {{ newItemLabel }}
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "viewable-tags",
        props: {
            editState: Boolean,
            value: Array,
            label: String,
            newItemLabel: {
                type: String,
                default: 'Add new tag'
            }
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