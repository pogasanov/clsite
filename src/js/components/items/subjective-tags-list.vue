<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showModal"
                label="Subjective Tags"
                new-item-label="Add new subjective tag"
                v-model="value"
        >
        </viewable-tags>

        <modal
                :deletable="index !== null"
                @cancel="hideModal"

                @delete="deleteTagModal"
                @ok="confirmTagModal"
                v-if="selectedTag !== undefined"
        >
            <h3 slot="header">Edit tag</h3>
            <div slot="body">
                <label for="subjective-tag">Subjective Tag</label>
                <select id="subjective-tag" v-model="selectedTag">
                    <option :value="tag" v-for="tag in subjectiveTags">{{tag}}</option>
                </select>
            </div>
        </modal>
    </div>
</template>

<script>
    import subjective_tags_choices from '../../../../app/clsite/choices/subjective-tags'
    import viewableTags from '@/components/inputs/viewable-tags.vue'
    import modal from "@/components/commons/modal.vue";
    import Vue from 'vue'

    export default {
        name: "subjective-tags-list",
        components: {
            viewableTags,
            modal
        },
        model: {
            prop: 'value',
            event: 'change'
        },
        props: {
            value: Array,
            editState: Boolean
        },
        data() {
            return {
                subjectiveTags: subjective_tags_choices,
                selectedTag: undefined,
                index: undefined
            }
        },
        methods: {
            showModal(index) {
                if (index === undefined) {
                    this.selectedTag = undefined
                }
                if (index === null) {
                    this.selectedTag = ""
                } else {
                    this.selectedTag = this.value[index]
                }
                this.index = index
            },
            confirmTagModal() {
                if (this.index === null) {
                    this.value.push(this.selectedTag)
                } else {
                    Vue.set(this.value, this.index, this.selectedTag)
                }
                this.hideModal()
            },
            deleteTagModal() {
                this.value.splice(this.index, 1);
                this.hideModal()
            },
            hideModal() {
                this.selectedTag = undefined
            },
        }
    }
</script>