<template>
    <div>
        <viewable-tags
                :edit-state="editState"
                @item-clicked="showModal"
                label="Subjective Tags"
                new-item-label="Add new subjective tag"
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
                    <option :value="tag" v-for="tag in subjectiveTags">{{tag}}</option>
                </select>
            </div>
        </modal>
    </div>
</template>

<script>
    import subjective_tags_choices from '../../../../app/clsite/choices/subjective-tags'
    import viewableTags from '@/components/inputs/viewable-tags.vue'
    import modal from "@/components/commons/modal.vue"
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
            subjectiveTags() {
                if (this.isNew) {
                    return subjective_tags_choices.filter(el => {
                        return this.value.indexOf(el) === -1
                    })
                } else {
                    return subjective_tags_choices
                }
            }
        }
    }
</script>