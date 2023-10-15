<template>
    <div>
        <b-button @click="$bvModal.show('modal-scoped')">Ope5n Modal</b-button>

        <b-modal id="modal-scoped">
            <template #modal-header="{ close }">
                <!-- Emulate built in modal header close button action -->
                <b-button size="sm" variant="outline-danger" @click="close()"> Close Modal </b-button>
                <h5>Modal Header</h5>
                ``
            </template>

            <template #default="{ hide }">
                <p>Modal Body with button</p>
                <b-button @click="hide()">Hide Modal</b-button>
            </template>

            <template #modal-footer="{ ok, cancel, hide }">
                <b>Custom Footer</b>
                <!-- Emulate built in modal footer ok and cancel button actions -->
                <b-button size="sm" variant="success" @click="ok()"> OK </b-button>
                <b-button size="sm" variant="danger" @click="cancel()"> Cancel </b-button>
                <!-- Button with custom close trigger value -->
                <b-button size="sm" variant="outline-secondary" @click="hide('forget')"> Forget it </b-button>
            </template>
        </b-modal>
    </div>
</template>
<script>
export default {};
</script>
