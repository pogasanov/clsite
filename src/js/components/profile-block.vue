<template>
    <section class="profile-block" id="profile-about">
        <header class="profile-block__header">
            <h2 class="profile-block__title">{{ title }}</h2>
        </header>
        <div class="profile-block__main">
            <template v-for="(content, header) in bodyContent">
                <h6 class="text-header">{{ header }}</h6>
                <template v-if="content.type === 'paragraphs'">
                    <p v-for="c in content.content">{{ c }}</p>
                </template>

                <ul :class="content.containerClass" v-else-if="content.type === 'list'">
                    <li :class="content.itemClass" v-for="tag in content.content">
                        {{ tag }}
                    </li>
                </ul>
            </template>
        </div>
    </section>
</template>

<script>
    export default {
        name: "profile-block",
        props: ['title'],
        data: () => {
            return {
                bodyContent: {
                    Overview: {
                        type: 'paragraphs',
                        content: [
                            'Part already down military really. Least once plant recently campaign.',
                            'Subject soldier consider road continue who. Even only put baby protect structure bank. Change shoulder number side.',
                            'Deep million system will floor form. Page change of.'
                        ]
                    },
                    Languages: {
                        type: 'list',
                        content: [
                            'English'
                        ],
                    },
                    'Subjective Tags': {
                        type: 'list',
                        containerClass: 'tag-container',
                        itemClass: 'tag',
                        content: [
                            'Fast'
                        ]
                    },
                }
            }
        }
    }
</script>

<style scoped>

</style>