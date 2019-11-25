<template>
    <div v-if="editState || value">
        <h6 class="text-header">{{ label }}</h6>
        <template v-if="editState">
            <select
                    :value="value"
                    @input="$emit('input', $event.target.value)"
            >
                <option :value="option" v-for="option in options">{{option}}</option>
            </select>
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
            options: Array
        }
    }
</script>