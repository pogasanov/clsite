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
            <ul>
                <li v-for="lang in languages">
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
    </profile-block>
</template>

<script>
    import profileBlock from './profile-block.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock
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
                subjectiveTags: ['dummy', 'subjective', 'tags']
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