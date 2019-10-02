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

        <modal @cancel="showModal = false" @ok="hideLanguageModal" v-if="showModal">
            <h3 slot="header">Edit language</h3>
            <div slot="body">
                <label for="language">Language</label>
                <select id="language" v-model="selectedLanguage">
                    <option value="ru">Ru</option>
                    <option value="en">En</option>
                </select>
                <label for="proficiency_level">Proficiency Level</label>
                <select id="proficiency_level" v-model="selectedProficiencyLevel">
                    <option value="NS">Native speaker</option>
                    <option value="PF">Professional fluency</option>
                    <option value="CF">Conversational fluency</option>
                </select>
            </div>
        </modal>
    </profile-block>
</template>

<script>
    import profileBlock from './profile-block.vue'
    import modal from "./modal.vue"

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            modal
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
                selectedIndex: 0,
                selectedLanguage: '',
                selectedProficiencyLevel: ''
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
                    this.selectedIndex = null
                    this.selectedLanguage = 'en'
                    this.selectedProficiencyLevel = 'NS'
                } else {
                    this.selectedIndex = index
                    this.selectedLanguage = this.languages[index].name
                    this.selectedProficiencyLevel = this.languages[index].proficiency_level
                }
                this.showModal = true
            },
            hideLanguageModal() {
                if (this.selectedIndex === null) {
                    this.languages.push({
                        name: this.selectedLanguage,
                        proficiency_level: this.selectedProficiencyLevel
                    })
                } else {
                    const index = this.selectedIndex
                    this.languages[index].name = this.selectedLanguage
                    this.languages[index].proficiency_level = this.selectedProficiencyLevel
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