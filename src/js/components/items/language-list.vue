<template>
    <div>
        <viewable-list
                :edit-state="editState"
                @item-clicked="showModal"
                label="Languages"
                new-item-label="Add new language"
                v-model="modalItems"
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
                    <option :value="value" v-for="(label, value) in choosable_languages">{{label}}</option>
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
            editState: Boolean,
        },
        data() {
            return {
                all_languages: language_choices
            }
        },
        methods: {
            emptyItem() {
                return {
                    name: 'en',
                    proficiency_level: 'NS'
                }
            },

            getLanguageName(name) {
                return this.all_languages[name]
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
        computed: {
            choosable_languages() {
                const names = this.modalItems.map(i => i.name);
                return Object.fromEntries(Object.entries(this.all_languages).filter(el => {
                    return (this.isNew || this.modalSelectedItem.name !== el[0]) ? names.indexOf(el[0]) === -1 : true
                }))
            }
        }
    }
</script>