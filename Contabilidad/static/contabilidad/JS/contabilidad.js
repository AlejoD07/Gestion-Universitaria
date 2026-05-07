function confirmarEliminar(event, mensaje) {
    const confirmado = confirm(mensaje || '¿Esta seguro de que desea eliminar este registro?');
    if (!confirmado) {
        event.preventDefault();
    }
}

function calcularTotalNomina() {
    const salario = parseFloat(document.getElementById('salario_base')?.value) || 0;
    const extras = parseFloat(document.getElementById('horas_extras')?.value) || 0;
    const comisiones = parseFloat(document.getElementById('comisiones')?.value) || 0;
    const deducciones = parseFloat(document.getElementById('deducciones')?.value) || 0;

    const total = salario + extras + comisiones - deducciones;

    const campoTotal = document.getElementById('total_calculado');
    if (campoTotal) {
        campoTotal.textContent = '$ ' + total.toLocaleString('es-CO');
    }
}

function calcularSaldo() {
    const asignado = parseFloat(document.getElementById('monto_asignado')?.value) || 0;
    const gastado = parseFloat(document.getElementById('monto_gastado')?.value) || 0;

    const saldo = asignado - gastado;

    const campoSaldo = document.getElementById('saldo_calculado');
    if (campoSaldo) {
        campoSaldo.textContent = '$ ' + saldo.toLocaleString('es-CO');
        campoSaldo.style.color = saldo >= 0 ? '#27ae60' : '#e74c3c';
    }
}

document.addEventListener('DOMContentLoaded', function () {

    const camposNomina = ['salario_base', 'horas_extras', 'comisiones', 'deducciones'];
    camposNomina.forEach(function (id) {
        const campo = document.getElementById(id);
        if (campo) {
            campo.addEventListener('input', calcularTotalNomina);
        }
    });

    const camposPresupuesto = ['monto_asignado', 'monto_gastado'];
    camposPresupuesto.forEach(function (id) {
        const campo = document.getElementById(id);
        if (campo) {
            campo.addEventListener('input', calcularSaldo);
        }
    });

    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    botonesEliminar.forEach(function (boton) {
        boton.addEventListener('click', function (e) {
            confirmarEliminar(e);
        });
    });
});
