<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">
                    <div class="modal-header">
                        <slot name="header">
                            default header
                        </slot>
                    </div>

                    <div class="modal-body">
                        <slot name="body">
                            default body
                        </slot>
                    </div>

                    <div class="modal-footer">
                        <slot name="footer">
                            <button @click="$emit('ok')" class="modal-default-button">
                                OK
                            </button>
                            <button @click="$emit('delete')" class="modal-default-button" v-if="deletable">
                                Delete
                            </button>
                            <button @click="$emit('cancel')" class="modal-default-button">
                                Cancel
                            </button>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "modal",
        props: ['deletable']
    }
</script>