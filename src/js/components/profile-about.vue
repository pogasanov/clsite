<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-about"
            title="About"
    >
        <viewable-textarea
                :edit-state="editState"
                label="Summary"
                v-model="summary"
        >
        </viewable-textarea>

        <viewable-textarea
                :edit-state="editState"
                label="Bio"
                v-model="bio"
        >
        </viewable-textarea>

        <language-list
                :edit-state="editState"
                v-model="languages"
        >

        </language-list>

        <viewable-tags
                :edit-state="editState"
                @item-clicked="showSubjectiveTagModal"
                label="Subjective Tags"
                new-item-label="Add new subjective tag"
                v-model="subjectiveTags"
        >
        </viewable-tags>

        <subjective-tag-modal
                :index="selectedSubjectiveTag"
                @reset="selectedSubjectiveTag = undefined"
                v-model="subjectiveTags"
        >
        </subjective-tag-modal>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/profile-block.vue'
    import subjectiveTagModal from '@/components/modals/subjective-tag-modal.vue'
    import viewableTextarea from '@/components/inputs/viewable-textarea.vue'
    import viewableTags from '@/components/inputs/viewable-tags.vue'
    import languageList from '@/components/items/language-list.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            subjectiveTagModal,
            viewableTextarea,
            viewableTags,
            languageList,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                summary: 'dummy summary',
                bio: 'dummy bio',
                languages: [
                    {
                        name: 'dummy',
                        proficiency_level: 'dunno'
                    }, {
                        name: 'language',
                        proficiency_level: 'dunno'
                    }
                ],
                subjectiveTags: ['dummy', 'subjective', 'tags'],
                showModal: false,

                selectedSubjectiveTag: undefined
            }
        },
        methods: {
            updateData(data) {
                this.summary = data.summary;
                this.bio = data.bio;
                this.languages = data.languages;
                this.subjectiveTags = data.subjective_tags
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        summary: this.summary,
                        bio: this.bio,
                        languages: this.languages,
                        subjective_tags: this.subjectiveTags
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about);
                this.editState = !this.editState
            },
            showSubjectiveTagModal(index) {
                this.selectedSubjectiveTag = index
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