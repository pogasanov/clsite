<template>
    <section class="profile-block" id="profile-about">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>

            <a @click="$emit('edit')" class="btn btn--small" href="#0">Edit</a>
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
            }
        }
    }
</script>

<style scoped>

</style>