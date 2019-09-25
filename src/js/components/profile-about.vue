<template>
    <profile-block @edit="editHandler" title="About">
        <template v-if="summary">
            <h6 class="text-header">Summary</h6>
            <template v-if="editState">
                <textarea cols="30" v-model="summary"></textarea>
            </template>
            <template v-else>
                {{ summary }}
            </template>
        </template>

        <template v-if="bio">
            <h6 class="text-header">Bio</h6>
            <template v-if="editState">
                <textarea cols="30" v-model="bio"></textarea>
            </template>
            <template v-else>
                {{ bio }}
            </template>
        </template>

        <template v-if="languages">
            <h6 class="text-header">Languages</h6>
            <ul>
                <li v-for="lang in languages">
                    {{ lang }},<br/>
                    <span class="muted">test</span>
                </li>
            </ul>
        </template>

        <template v-if="subjectiveTags">
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
        data: () => {
            return {
                editState: false,
                summary: 'dummy summary',
                bio: 'dummy bio',
                languages: ['dummy', 'languages'],
                subjectiveTags: ['dummy', 'subjective', 'tags']
            }
        },
        methods: {
            editHandler() {
                this.editState = !this.editState
            }
        }
    }
</script>

<style scoped>

</style>