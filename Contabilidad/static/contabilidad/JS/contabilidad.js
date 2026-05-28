function confirmarEliminar(event, mensaje) {
    const confirmado = confirm(mensaje || '¿Está seguro de que desea eliminar este registro?');
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

function limpiarDatosEmpleado() {
    ['empleado_nombre', 'cargo', 'area'].forEach(function (id) {
        const campo = document.getElementById(id);
        if (campo) {
            campo.value = '';
        }
    });
}

function escribirMensajeEmpleado(texto, esError) {
    const mensaje = document.getElementById('empleado_mensaje');
    if (!mensaje) {
        return;
    }
    mensaje.textContent = texto;
    mensaje.style.color = esError ? '#c0392b' : '#138a4b';
}

function cargarEmpleadoPorCedula() {
    const formulario = document.getElementById('nomina-form');
    const cedula = document.getElementById('empleado_cedula')?.value.trim();
    if (!formulario || !cedula) {
        limpiarDatosEmpleado();
        escribirMensajeEmpleado('Busca la cédula registrada en Recursos Humanos.', false);
        return;
    }

    const url = formulario.dataset.buscarEmpleadoUrl + '?cedula=' + encodeURIComponent(cedula);
    escribirMensajeEmpleado('Buscando empleado...', false);

    fetch(url)
        .then(function (respuesta) {
            if (!respuesta.ok) {
                throw new Error('Empleado no encontrado');
            }
            return respuesta.json();
        })
        .then(function (data) {
            const empleado = data.empleado;
            document.getElementById('empleado_nombre').value = empleado.nombre || '';
            document.getElementById('cargo').value = empleado.cargo || '';
            document.getElementById('area').value = empleado.area || '';

            const salario = document.getElementById('salario_base');
            if (salario && empleado.salario !== '') {
                salario.value = empleado.salario;
            }

            escribirMensajeEmpleado('Empleado cargado desde Recursos Humanos.', false);
            calcularTotalNomina();
        })
        .catch(function () {
            limpiarDatosEmpleado();
            escribirMensajeEmpleado('No se encontró un empleado activo con esa cédula.', true);
        });
}

document.addEventListener('DOMContentLoaded', function () {

    const camposNomina = ['salario_base', 'horas_extras', 'comisiones', 'deducciones'];
    camposNomina.forEach(function (id) {
        const campo = document.getElementById(id);
        if (campo) {
            campo.addEventListener('input', calcularTotalNomina);
        }
    });

    const botonBuscarEmpleado = document.getElementById('buscar_empleado');
    if (botonBuscarEmpleado) {
        botonBuscarEmpleado.addEventListener('click', cargarEmpleadoPorCedula);
    }

    const campoCedula = document.getElementById('empleado_cedula');
    if (campoCedula) {
        campoCedula.addEventListener('change', cargarEmpleadoPorCedula);
    }

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
