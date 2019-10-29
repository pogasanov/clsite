<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-details"
            title="Professional Details"
    >
        <template v-if="editState || lawTypeTags">
            <h6 class="text-header">Practice areas</h6>
            <ul class="tag-container">
                <li @click="editState && showLawTypeTagsModal(index)" class="tag"
                    v-for="(tag, index) in lawTypeTags">
                    {{ tag }}
                </li>
                <li @click="editState && showLawTypeTagsModal(null)" class="tag tag--outline" v-if="editState">
                    Add new practice area
                </li>
            </ul>
        </template>

        <div class="profile-block__row">
            <div v-if="editState || experience">
                <h6 class="text-header">Years of Practice / Experience</h6>
                <template v-if="editState">
                    <input type="number" v-model="experience">
                </template>
                <template v-else>
                    {{ experience }}
                </template>
            </div>

            <div v-if="editState || current_job">
                <h6 class="text-header">Current Job / Affiliation / Law Firm</h6>
                <template v-if="editState">
                    <input type="text" v-model="current_job">
                </template>
                <template v-else>
                    {{ current_job }}
                </template>
            </div>
        </div>

        <subjective-tag-modal
                :index="selectedLawTypeTag"
                @reset="selectedLawTypeTag = undefined"
                v-model="lawTypeTags"
        >
        </subjective-tag-modal>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/profile-block.vue'
    import subjectiveTagModal from '@/components/modals/subjective-tag-modal.vue'

    export default {
        name: "profile-about",
        components: {
            profileBlock,
            subjectiveTagModal
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                lawTypeTags: ['dummy', 'subjective', 'tags'],
                experience: '',
                current_job: '',
                showModal: false,

                selectedLawTypeTag: undefined
            }
        },
        methods: {
            updateData(data) {
                this.lawTypeTags = data.law_type_tags;
                this.experience = data.experience;
                this.current_job = data.current_job
            },
            editHandler() {
                if (this.editState) {
                    this.$emit('update', {
                        law_type_tags: this.lawTypeTags,
                        experience: this.experience,
                        current_job: this.current_job,
                    })
                }
                this.editState = !this.editState
            },
            cancelHandler() {
                this.updateData(this.about);
                this.editState = !this.editState
            },

            showLawTypeTagsModal(index) {
                this.selectedLawTypeTag = index
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