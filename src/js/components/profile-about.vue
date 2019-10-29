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

        <viewable-list
                :edit-state="editState"
                @item-clicked="showLanguageModal"
                label="Languages"
                new-item-label="Add new language"
                v-model="languages"
        >
            <template v-slot:default="slotProps">
                {{ getLanguageName(slotProps.item.name) }},<br/>
                <span class="muted">{{ getLanguageProficiencyLevel(slotProps.item.proficiency_level) }}</span>
            </template>
        </viewable-list>

        <viewable-tags
                :edit-state="editState"
                @item-clicked="showSubjectiveTagModal"
                label="Subjective Tags"
                new-item-label="Add new subjective tag"
                v-model="subjectiveTags"
        >
        </viewable-tags>

        <language-modal
                :index="selectedLanguage"
                @reset="selectedLanguage = undefined"
                v-model="languages"
        >
        </language-modal>

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
    import languageModal from '@/components/modals/language-modal.vue'
    import subjectiveTagModal from '@/components/modals/subjective-tag-modal.vue'
    import language_choices from '../../../app/clsite/choices/language_choices'
    import viewableTextarea from '@/components/inputs/viewable-textarea.vue'
    import viewableList from '@/components/inputs/viewable-list.vue'
    import viewableTags from '@/components/inputs/viewable-tags.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            languageModal,
            subjectiveTagModal,
            viewableTextarea,
            viewableList,
            viewableTags
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

                selectedLanguage: undefined,
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

            showLanguageModal(index) {
                this.selectedLanguage = index
            },
            showSubjectiveTagModal(index) {
                this.selectedSubjectiveTag = index
            },

            getLanguageName(name) {
                return language_choices[name]
            },
            getLanguageProficiencyLevel(proficiency_level) {
                switch (proficiency_level) {
                    case 'NS':
                        return 'Native speaker';
                    case 'PF':
                        return 'Professional fluency';
                    case 'CF':
                        return 'Conversational fluency'
                }
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