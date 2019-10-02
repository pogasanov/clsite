<template>
    <profile-block @edit="editHandler" title="About">
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
                <li class="tag" v-for="tag in subjectiveTags">
                    {{ tag }}
                </li>
            </ul>
        </template>

        <language-modal :language="selectedLanguage" :show="showModal" @ok="hideLanguageModal">
        </language-modal>
    </profile-block>
</template>

<script>
    import profileBlock from './profile-block.vue'
    import languageModal from './modals/language-modal.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            languageModal
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
                selectedLanguage: {},
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
                        languages: this.languages
                    })
                }
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
                this.showModal = true
            },
            hideLanguageModal() {
                if (this.languages.indexOf(this.selectedLanguage) === -1) {
                    this.languages.push(this.selectedLanguage)
                }
                this.showModal = false
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