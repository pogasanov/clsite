<template>
    <modal
            @ok="confirmLanguageModal"
            :deletable="index !== null"

            @cancel="$emit('reset')"
            @delete="deleteLanguageModal"
            v-if="index !== undefined"
    >
        <h3 slot="header">Edit language</h3>
        <div slot="body">
            <label for="language">Language</label>
            <select id="language" v-model="selectedLanguage.name">
                <option :value="value" v-for="(label, value) in language_choices">{{label}}</option>
            </select>

            <label for="proficiency_level">Proficiency Level</label>
            <select id="proficiency_level" v-model="selectedLanguage.proficiency_level">
                <option value="NS">Native speaker</option>
                <option value="PF">Professional fluency</option>
                <option value="CF">Conversational fluency</option>
            </select>
        </div>
    </modal>
</template>

<script>
    import modal from "@/components/modals/modal.vue";
    import language_choices from '../../../../app/clsite/choices/language_choices'

    export default {
        name: "language-modal",
        components: {
            modal
        },
        model: {
            prop: 'languages',
            event: 'change'
        },
        props: {
            languages: {
                required: true
            },
            index: {
                required: true
            }
        },
        data() {
            return {
                language_choices: language_choices,
                selectedLanguage: undefined
            }
        },
        methods: {
            confirmLanguageModal() {
                if (this.index === null) {
                    this.languages.push(this.selectedLanguage)
                } else {
                    Vue.set(this.languages, this.index, this.selectedLanguage)
                }
                this.$emit('reset')
            },
            deleteLanguageModal() {
                this.languages.splice(this.index, 1);
                this.$emit('reset')
            },
        },
        watch: {
            index() {
                if (this.index === undefined) {
                    this.selectedLanguage = undefined
                }
                if (this.index === null) {
                    this.selectedLanguage = {
                        name: 'en',
                        proficiency_level: 'NS'
                    }
                } else {
                    this.selectedLanguage = Object.assign({}, this.languages[this.index])
                }
            }
        }
    }
</script>