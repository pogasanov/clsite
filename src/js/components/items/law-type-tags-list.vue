<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showLawTypeTagsModal"
                label="Practice areas"
                new-item-label="Add new practice area"
                v-model="value"
        >
        </viewable-tags>

        <subjective-tag-modal
                :index="selectedLawTypeTag"
                @reset="selectedLawTypeTag = undefined"
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
                selectedLawTypeTag: undefined
            }
        },
        methods: {
            showLawTypeTagsModal(index) {
                this.selectedLawTypeTag = index
            },
        }
    }
</script>