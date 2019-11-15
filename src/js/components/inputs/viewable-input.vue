<template>
    <div v-if="editState || value">
        <h6 class="text-header">{{ label }}</h6>
        <template v-if="editState">
            <input
                    :type="type"
                    :value="value"
                    @input="$emit('input', $event.target.value)"
            >
        </template>
        <template v-else>
            {{ value }}
        </template>
    </div>
</template>

<script>
    export default {
        name: "viewable-input",
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