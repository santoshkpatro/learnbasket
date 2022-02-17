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
        <label for="exampleInputEmail1" class="form-label">{{ label }}</label>
        <input
            :placeholder="label"
            class="form-control"
            :value="modelValue"
            v-bind="$attrs"
            @input="$emit('update:modelValue', $event.target.value)"
        />
        <div id="emailHelp" class="form-text">{{ message }}</div>
    </div>
</template>