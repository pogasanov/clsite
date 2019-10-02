<template>
    <section class="profile-block" id="profile-about">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>

            <a @click="toggleEdit" class="btn btn--small" href="#0" v-if="!editState">Edit</a>
            <a @click="toggleEdit" class="btn btn--small" href="#0" v-else>Save</a>
        </header>
        <div class="profile-block__main">
            <slot></slot>
        </div>
    </section>
</template>

<script>
    export default {
        name: "profile-block",
        props: ['title'],
        data: () => {
            return {
                editState: false
            }
        },
        methods: {
            toggleEdit() {
                this.editState = !this.editState
                this.$emit('edit')
            }
        }
    }
</script>