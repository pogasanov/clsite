<template>
    <modal @cancel="$emit('cancel')" @ok="$emit('ok', _tag)" v-if="tag !== null">
        <h3 slot="header">Edit tag</h3>
        <div slot="body">
            <label for="subjective-tag">Subjective Tag</label>
            <input id="subjective-tag" type="text" v-model="_tag">
        </div>
    </modal>
</template>

<script>
    import modal from "./modal.vue";

    export default {
        name: "subjective-tag-modal",
        components: {
            modal
        },
        props: {
            tag: {
                required: true
            }
        },
        data() {
            return {
                _tag: ''
            }
        },
        mounted() {
            this._tag = this.tag
        }
    }
</script>