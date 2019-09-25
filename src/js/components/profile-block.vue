<template>
    <section class="profile-block" id="profile-about">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>
        </header>
        <div class="profile-block__main">
            <slot></slot>
        </div>
    </section>
</template>

<script>
    export default {
        name: "profile-block",
        props: ['title']
    }
</script>

<style scoped>

</style>