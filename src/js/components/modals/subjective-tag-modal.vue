<template>
    <modal
            :deletable="index !== null"
            @cancel="$emit('reset')"

            @delete="deleteTagModal"
            @ok="confirmTagModal"
            v-if="index !== undefined"
    >
        <h3 slot="header">Edit tag</h3>
        <div slot="body">
            <label for="subjective-tag">Subjective Tag</label>
            <input id="subjective-tag" type="text" v-model="selectedTag">
        </div>
    </modal>
</template>

<script>
    import modal from "@/components/modals/modal.vue";

    export default {
        name: "subjective-tag-modal",
        components: {
            modal
        },
        model: {
            prop: 'tags',
            event: 'change'
        },
        props: {
            tags: {
                required: true
            },
            index: {
                required: true
            }
        },
        data() {
            return {
                selectedTag: undefined
            }
        },
        methods: {
            confirmTagModal() {
                if (this.index === null) {
                    this.tags.push(this.selectedTag)
                } else {
                    this.tags[this.index] = this.selectedTag
                }
                this.$emit('reset')
            },
            deleteTagModal() {
                this.tags.splice(this.index, 1);
                this.$emit('reset')
            },
        },
        watch: {
            index() {
                if (this.index === undefined) {
                    this.selectedTag = undefined
                }
                if (this.index === null) {
                    this.selectedTag = ""
                } else {
                    this.selectedTag = this.tags[this.index]
                }
            }
        }
    }
</script>