<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showLanguageModal"
                label="Languages"
                new-item-label="Add new language"
                v-model="value"
        >
            <template v-slot:default="slotProps">
                {{ getLanguageName(slotProps.item.name) }},<br/>
                <span class="muted">{{ getLanguageProficiencyLevel(slotProps.item.proficiency_level) }}</span>
            </template>
        </viewable-list>

        <language-modal
                :index="selectedLanguage"
                @reset="selectedLanguage = undefined"
                v-model="value"
        >
        </language-modal>
    </div>
</template>

<script>
    import language_choices from '../../../../app/clsite/choices/language_choices'
    import viewableList from '@/components/inputs/viewable-list.vue'
    import languageModal from '@/components/modals/language-modal.vue'

    export default {
        name: "language-list",
        components: {
            viewableList,
            languageModal
        },
        props: ['value', 'editState'],
        data() {
            return {
                language_choices: language_choices,
                selectedLanguage: undefined
            }
        },
        methods: {
            showLanguageModal(index) {
                this.selectedLanguage = index
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
        }
    }
</script>