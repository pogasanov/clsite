<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-details"
            title="Professional Details"
    >

        <viewable-tags
                :edit-state="editState"
                @item-clicked="showLawTypeTagsModal"
                label="Practice areas"
                v-model="lawTypeTags"
        >
        </viewable-tags>

        <div class="profile-block__row">
            <viewable-input
                    :edit-state="editState"
                    label="Years of Practice / Experience"
                    type="number"
                    v-model="experience"
            >
            </viewable-input>

            <viewable-input
                    :edit-state="editState"
                    label="Current Job / Affiliation / Law Firm"
                    v-model="current_job"
            >
            </viewable-input>
        </div>

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
    import viewableInput from '@/components/inputs/viewable-input.vue'
    import viewableTags from '@/components/inputs/viewable-tags.vue'

    export default {
        name: "profile-details",
        components: {
            profileBlock,
            subjectiveTagModal,
            viewableInput,
            viewableTags
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                lawTypeTags: ['dummy', 'subjective', 'tags'],
                experience: '',
                current_job: '',
                showModal: false,

                selectedLawTypeTag: undefined
            }
        },
        methods: {
            updateData(data) {
                this.lawTypeTags = data.law_type_tags;
                this.experience = data.experience;
                this.current_job = data.current_job
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        law_type_tags: this.lawTypeTags,
                        experience: this.experience,
                        current_job: this.current_job,
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