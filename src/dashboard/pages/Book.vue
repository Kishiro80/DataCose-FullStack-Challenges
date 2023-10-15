<template>
    <div class="p-3">
        <h1>Book Page</h1>
        <bookComponent></bookComponent>
    </div>
</template>
<script>
import bookComponent from '@/components/bookComponent';

export default {
    layout: 'ProtectedContent',
    components: {
        bookComponent,
    },
};
</script>
