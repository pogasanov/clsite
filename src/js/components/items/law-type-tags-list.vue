<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showModal"
                label="Practice areas"
                new-item-label="Add new practice area"
                v-model="modalItems"
        >
        </viewable-tags>

        <modal
                :deletable="!isNew"
                @cancel="hideModal"

                @delete="deleteModal"
                @ok="confirmModal"
                v-if="isModalDisplayed"
        >
            <h3 slot="header">Edit practice area</h3>
            <div slot="body">
                <label for="subjective-tag">Practice area</label>
                <select id="subjective-tag" v-model="modalSelectedItem">
                    <option :value="tag" v-for="tag in choosableLawTypeTags">{{tag}}</option>
                </select>
            </div>
        </modal>
    </div>
</template>

<script>
    import law_type_tags_choices from '../../../../app/clsite/choices/law-type-tags-ontology'
    import viewableTags from '@/components/inputs/viewable-tags.vue'
    import modal from "@/components/commons/modal.vue";
    import {modalManipulation} from '@/mixins'


    export default {
        name: "subjective-tags-list",
        mixins: [modalManipulation],
        components: {
            viewableTags,
            modal
        },
        props: {
            editState: Boolean
        },
        computed: {
            allLawTypeTags() {
                let result = [];
                law_type_tags_choices.forEach(el => {
                    el.subareas.forEach(el => {
                        result.push(el.name)
                    })
                });
                return result.sort()
            },
            choosableLawTypeTags() {
                return this.allLawTypeTags.filter(el => {
                    return (this.isNew || this.modalSelectedItem !== el) ? this.modalItems.indexOf(el) === -1 : true
                })
            }
        }
    }
</script>