<template>
    <div v-if="editState || value">
        <h6 class="text-header">{{ label }}</h6>
        <template v-if="editState">
            <textarea
                    :value="value"
                    @input="$emit('input', $event.target.value)"
            ></textarea>
        </template>
        <template v-else>
            {{ value }}
        </template>
    </div>
</template>

<script>
    export default {
        name: "viewable-textarea",
        props: {
            editState: Boolean,
            value: [String, Number],
            label: String,
            type: {
                type: String,
                default: 'text'
            }
        }
    }
</script>