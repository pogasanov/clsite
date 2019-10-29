<template>
    <section :id="section_id" class="profile-block">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>

            <a @click="toggleEdit" class="btn btn--small" href="#0" v-if="!editState">Edit</a>
            <template v-else>
                <a @click="toggleEdit" class="btn btn--small" href="#0">Save</a>
                <a @click="cancelEdit" class="btn btn--small btn--outline" href="#0">Cancel</a>
            </template>
        </header>
        <div class="profile-block__main">
            <slot></slot>
        </div>
    </section>
</template>

<script>
    export default {
        name: "profile-block",
        props: ['title', 'section_id'],
        data: () => {
            return {
                editState: false
            }
        },
        methods: {
            toggleEdit() {
                this.editState = !this.editState;
                this.$emit('edit')
            },
            cancelEdit() {
                this.editState = false;
                this.$emit('cancel')
            }
        }
    }
</script>