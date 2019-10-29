<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showSubjectiveTagModal"
                label="Subjective Tags"
                new-item-label="Add new subjective tag"
                v-model="value"
        >
        </viewable-tags>

        <subjective-tag-modal
                :index="selectedSubjectiveTag"
                @reset="selectedSubjectiveTag = undefined"
                v-model="value"
        >
        </subjective-tag-modal>
    </div>
</template>

<script>
    import viewableTags from '@/components/inputs/viewable-tags.vue'
    import subjectiveTagModal from '@/components/modals/subjective-tag-modal.vue'

    export default {
        name: "subjective-tags-list",
        components: {
            viewableTags,
            subjectiveTagModal
        },
        props: ['value', 'editState'],
        data() {
            return {
                selectedSubjectiveTag: undefined
            }
        },
        methods: {
            showSubjectiveTagModal(index) {
                this.selectedSubjectiveTag = index
            },
        }
    }
</script>