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

        <subjective-tags-list
                :edit-state="editState"
                v-model="subjectiveTags"
        >
        </subjective-tags-list>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/commons/profile-block.vue'
    import viewableTextarea from '@/components/inputs/viewable-textarea.vue'
    import languageList from '@/components/items/language-list.vue'
    import subjectiveTagsList from '@/components/items/subjective-tags-list.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            viewableTextarea,
            languageList,
            subjectiveTagsList
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