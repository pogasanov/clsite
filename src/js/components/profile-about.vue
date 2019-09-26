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
                <li @click="showLanguageModal(lang.id)" class="list__item" v-for="lang in languages">
                    {{ lang.name }},<br/>
                    <span class="muted">{{ lang.proficiency_level }}</span>
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

        <modal @close="showModal = false" v-if="showModal">
            <h3 slot="header">Edit language</h3>
            <div slot="body">
                <label for="language">Language</label>
                <select id="language" v-model="selectedLanguage">
                    <option value="ru">Ru</option>
                    <option value="en">En</option>
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
                selectedLanguage: ''
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
                        bio: this.bio
                    })
                }
                this.editState = !this.editState
            },

            showLanguageModal(id) {
                this.selectedLanguage = this.languages[0].name
                this.showModal = true
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

<style scoped>

</style>