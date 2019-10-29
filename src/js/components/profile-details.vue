<template>
    <profile-block
            @cancel="cancelHandler"
            @edit="editHandler"
            section_id="profile-details"
            title="Professional Details"
    >
        <law-type-tags-list
                :edit-state="editState"
                v-model="lawTypeTags"
        >
        </law-type-tags-list>

        <div class="profile-block__row">
            <viewable-input
                    :edit-state="editState"
                    label="Years of Practice / Experience"
                    type="number"
                    v-model="experience"
            >
            </viewable-input>

            <viewable-input
                    :edit-state="editState"
                    label="Current Job / Affiliation / Law Firm"
                    v-model="current_job"
            >
            </viewable-input>
        </div>
    </profile-block>
</template>

<script>
    import profileBlock from '@/components/profile-block.vue'
    import viewableInput from '@/components/inputs/viewable-input.vue'
    import lawTypeTagsList from '@/components/items/law-type-tags-list.vue'

    export default {
        name: "profile-details",
        components: {
            profileBlock,
            lawTypeTagsList,
            viewableInput,
        },
        props: ['about'],
        data: () => {
            return {
                editState: false,
                lawTypeTags: ['dummy', 'subjective', 'tags'],
                experience: '',
                current_job: '',
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