function confirmarEliminar(event, mensaje) {
    const confirmado = confirm(mensaje || 'Esta seguro de que desea eliminar este registro?');
    if (!confirmado) {
        event.preventDefault();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    botonesEliminar.forEach(function (boton) {
        boton.addEventListener('click', function (e) {
            confirmarEliminar(e);
        });
    });
});
