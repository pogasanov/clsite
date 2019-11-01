<template>
    <section :class="{'profile-block--empty': !hasContent}" :id="section_id" class="profile-block">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>

            <template v-if="hasContent">
                <a @click="toggleEdit" class="btn btn--small js-edit" href="#0" v-if="!editState">Edit</a>
                <template v-else>
                    <a @click="toggleEdit" class="btn btn--small js-save" href="#0">Save</a>
                    <a @click="cancelEdit" class="btn btn--small btn--outline js-cancel" href="#0">Cancel</a>
                </template>
            </template>
            <template v-else>
                <span class="profile-block__subtitle">{{ title }} information is hidden untill you contact this user</span>
                <a class="btn btn--small" href="#0">Contact</a>
            </template>
        </header>
        <div class="profile-block__main" v-if="hasContent">
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
        },
        computed: {
            hasContent() {
                return !!this.$slots.default;
            }
        }
    }
</script>