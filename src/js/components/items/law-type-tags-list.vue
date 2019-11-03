<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showModal"
                label="Practice areas"
                new-item-label="Add new practice area"
                v-model="value"
        >
        </viewable-tags>

        <modal
                :deletable="!isNew"
                @cancel="hideModal"

                @delete="deleteModal"
                @ok="confirmModal"
                v-if="isModalDisplayed"
        >
            <h3 slot="header">Edit tag</h3>
            <div slot="body">
                <label for="subjective-tag">Subjective Tag</label>
                <select id="subjective-tag" v-model="modalSelectedItem">
                    <option :value="tag" v-for="tag in lawTypeTags">{{tag}}</option>
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
            lawTypeTags() {
                let result = [];
                law_type_tags_choices.forEach(el => {
                    el.subareas.forEach(el => {
                        if (!this.isNew || this.value.indexOf(el.name) === -1) {
                            result.push(el.name)
                        }
                    })
                });
                return result.sort()
            }
        }
    }
</script>