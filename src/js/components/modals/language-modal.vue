<template>
    <modal @cancel="$emit('cancel')" @ok="$emit('ok')" v-if="language !== null">
        <h3 slot="header">Edit language</h3>
        <div slot="body">
            <label for="language">Language</label>
            <select id="language" v-model="language.name">
                <option value="ru">Ru</option>
                <option value="en">En</option>
            </select>
            <label for="proficiency_level">Proficiency Level</label>
            <select id="proficiency_level" v-model="language.proficiency_level">
                <option value="NS">Native speaker</option>
                <option value="PF">Professional fluency</option>
                <option value="CF">Conversational fluency</option>
            </select>
        </div>
    </modal>
</template>

<script>
    import modal from "./modal.vue";

    export default {
        name: "language-modal",
        components: {
            modal
        },
        props: {
            language: {
                required: true
            }
        }
    }
</script>