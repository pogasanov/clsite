<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Languages"
                new-item-label="Add new language"
                v-model="value"
        >
            <template v-slot:default="slotProps">
                {{ getLanguageName(slotProps.item.name) }},<br/>
                <span class="muted">{{ getLanguageProficiencyLevel(slotProps.item.proficiency_level) }}</span>
            </template>
        </viewable-list>

        <modal
                :deletable="!isNew"
                @cancel="hideModal"

                @delete="deleteModal"
                @ok="confirmModal"
                v-if="isModalDisplayed"
        >
            <h3 slot="header">Edit language</h3>
            <div slot="body">
                <label for="language">Language</label>
                <select id="language" v-model="modalSelectedItem.name">
                    <option :value="value" v-for="(label, value) in language_choices">{{label}}</option>
                </select>

                <label for="proficiency_level">Proficiency Level</label>
                <select id="proficiency_level" v-model="modalSelectedItem.proficiency_level">
                    <option value="NS">Native speaker</option>
                    <option value="PF">Professional fluency</option>
                    <option value="CF">Conversational fluency</option>
                </select>
            </div>
        </modal>
    </div>
</template>

<script>
    import language_choices from '../../../../app/clsite/choices/languages'
    import viewableList from '@/components/inputs/viewable-list.vue'
    import modal from "@/components/commons/modal.vue";
    import {modalManipulation} from "@/mixins";

    export default {
        name: "language-list",
        mixins: [modalManipulation],
        components: {
            viewableList,
            modal
        },
        props: {
            editState: Boolean
        },
        data() {
            return {
                language_choices: language_choices,
            }
        },
        methods: {
            emptyItem() {
                return {
                    name: 'en',
                    proficiency_level: 'NS'
                }
            },
            existingItem() {
                return Object.assign({}, this.value[this.modalIndex])
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
    }
</script>