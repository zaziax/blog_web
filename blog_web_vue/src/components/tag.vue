<template>
    <span class="tag" :class="`tag-${type}`">{{ label }}</span>
  </template>
  
  <script>
  export default {
    name: 'Tag',
    props: {
      label: {
        type: String,
        required: true,
      },
      type: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'primary', 'success', 'warning', 'danger'].includes(value),
      },
    },
  };
  </script>
  
  <style scoped>
  .tag {
    display: inline-block;
    padding: 0.25em 0.5em;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
  }
  
  .tag-default {
    color: #333;
    background-color: #f5f5f5;
  }
  
  .tag-primary {
    color: #fff;
    background-color: #ff5e00;
  }
  
  .tag-success {
    color: #fff;
    background-color: #3de1ad;
  }
  
  .tag-warning {
    color: #fff;
    background-color: #ffc107;
  }
  
  .tag-danger {
    color: #fff;
    background-color: #dc3545;
  }
  </style>