<template>
    <profile-block @cancel="cancelHandler" @edit="editHandler" title="About">
        <template v-if="editState || summary">
            <h6 class="text-header">Summary</h6>
            <template v-if="editState">
                <textarea cols="30" v-model="summary"></textarea>
            </template>
            <template v-else>
                {{ summary }}
            </template>
        </template>

        <template v-if="editState || bio">
            <h6 class="text-header">Bio</h6>
            <template v-if="editState">
                <textarea cols="30" v-model="bio"></textarea>
            </template>
            <template v-else>
                {{ bio }}
            </template>
        </template>

        <template v-if="editState || languages">
            <h6 class="text-header">Languages</h6>
            <ul :class="editState ? 'list--selectable' : ''" class="list">
                <li @click="editState && showLanguageModal(index)" class="list__item"
                    v-for="(lang, index) in languages">
                    {{ lang.name }},<br/>
                    <span class="muted">{{ lang.proficiency_level }}</span>
                </li>
                <li @click="editState && showLanguageModal(null)" class="list__item" v-if="editState">
                    Add new language
                </li>
            </ul>
        </template>

        <template v-if="editState || subjectiveTags">
            <h6 class="text-header">Subjective Tags</h6>
            <ul class="tag-container">
                <li @click="editState && showSubjectiveTagModal(index)" class="tag"
                    v-for="(tag, index) in subjectiveTags">
                    {{ tag }}
                </li>
                <li @click="editState && showSubjectiveTagModal(null)" class="tag tag--outline" v-if="editState">
                    Add new subjective tag
                </li>
            </ul>
        </template>

        <language-modal :language="selectedLanguage"
                        @cancel="selectedLanguage = null"
                        @ok="hideLanguageModal">
        </language-modal>

        <subjective-tag-modal :tag="selectedSubjectiveTag"
                              @cancel="selectedSubjectiveTag = null"
                              @ok="hideSubjectiveTagModal"
        >

        </subjective-tag-modal>
    </profile-block>
</template>

<script>
    import profileBlock from './profile-block.vue'
    import languageModal from './modals/language-modal.vue'
    import subjectiveTagModal from './modals/subjective-tag-modal.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            languageModal,
            subjectiveTagModal
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

                selectedLanguage: null,
                selectedSubjectiveTag: null
            }
        },
        methods: {
            updateData(data) {
                this.summary = data.summary
                this.bio = data.bio
                this.languages = data.languages
                this.subjectiveTags = data.law_type_tags
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        summary: this.summary,
                        bio: this.bio,
                        languages: this.languages,
                        law_type_tags: this.subjectiveTags
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about)
                this.editState = !this.editState
            },

            showLanguageModal(index) {
                if (index === null) {
                    this.selectedLanguage = {
                        name: 'en',
                        proficiency_level: 'NS'
                    }
                } else {
                    this.selectedLanguage = this.languages[index]
                }
            },
            hideLanguageModal() {
                if (this.languages.indexOf(this.selectedLanguage) === -1) {
                    this.languages.push(this.selectedLanguage)
                }
                this.selectedLanguage = null
            },

            showSubjectiveTagModal(index) {
                if (index === null) {
                    this.selectedSubjectiveTag = ''
                } else {
                    this.selectedSubjectiveTag = this.subjectiveTags[index]
                }
            },
            hideSubjectiveTagModal(value) {
                const tagIndex = this.subjectiveTags.findIndex(e => {
                    return e === this.selectedSubjectiveTag
                })
                if (tagIndex === -1) {
                    this.subjectiveTags.push(value)
                } else {
                    this.subjectiveTags[tagIndex] = value
                }
                this.selectedSubjectiveTag = null
            }
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