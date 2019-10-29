<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-details"
            title="Professional Details"
    >
        <template v-if="editState || lawTypeTags">
            <h6 class="text-header">Practice areas</h6>
            <ul class="tag-container">
                <li @click="editState && showLawTypeTagsModal(index)" class="tag"
                    v-for="(tag, index) in lawTypeTags">
                    {{ tag }}
                </li>
                <li @click="editState && showLawTypeTagsModal(null)" class="tag tag--outline" v-if="editState">
                    Add new practice area
                </li>
            </ul>
        </template>

        <subjective-tag-modal
                :index="selectedLawTypeTag"
                @reset="selectedLawTypeTag = undefined"
                v-model="lawTypeTags"
        >
        </subjective-tag-modal>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/profile-block.vue'
    import subjectiveTagModal from '@/components/modals/subjective-tag-modal.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            subjectiveTagModal
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                lawTypeTags: ['dummy', 'subjective', 'tags'],
                showModal: false,

                selectedLawTypeTag: undefined
            }
        },
        methods: {
            updateData(data) {
                this.lawTypeTags = data.law_type_tags
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        law_type_tags: this.lawTypeTags
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about);
                this.editState = !this.editState
            },

            showLawTypeTagsModal(index) {
                this.selectedLawTypeTag = index
            },
        },
        created() {
            this.updateData(this.about)
        },
        watch: {
            about(newAbout, oldAbout) {
                this.updateData(newAbout)
            }
        }
    }
</script>