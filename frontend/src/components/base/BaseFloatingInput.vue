<script>
export default {
    name: 'FloatingInput',
    props: {
        label: {
            type: String,
            default: '',
        },
        modelValue: {
            type: [String, Number],
            default: '',
        },
        message: {
            type: String,
            default: ''
        }
    }
}
</script>

<template>
    <div class="mb-3">
        <div class="form-floating">
            <input
                :placeholder="label"
                class="form-control"
                :value="modelValue"
                v-bind="$attrs"
                @input="$emit('update:modelValue', $event.target.value)"
            />
            <label for="floatingInput">{{ label }}</label>
        </div>
        <div id="emailHelp" class="form-text" v-if="message">{{ message }}</div>
    </div>
</template>