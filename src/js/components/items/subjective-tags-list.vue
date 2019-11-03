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
                selectedTag: undefined,
                index: undefined
            }
        },
        methods: {
            showModal(index) {
                this.index = index;
                this.selectedTag = (this.isNew ? "" : this.value[index])
            },
            confirmTagModal() {
                if (this.isNew) {
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
        },
        computed: {
            isNew() {
                return this.index === null
            },
            subjectiveTags() {
                if (this.isNew) {
                    return subjective_tags_choices.filter(el => {
                        return this.value.indexOf(el) === -1
                    })
                } else {
                    return subjective_tags_choices
                }
            }
        }
    }
</script>