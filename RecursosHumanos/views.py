from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, ProtectedError
from django.shortcuts import redirect
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None
from django.template.loader import get_template
import datetime
from . import models
from gestionAcademica.models import Usuario as UsuarioAcademico
from django.db.models import Q
def _pdf_escape(texto):
    return str(texto).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def _generar_pdf_simple(lineas):
    contenido = ['BT', '/F1 12 Tf', '72 760 Td', '16 TL']
    for linea in lineas:
        contenido.append(f'({_pdf_escape(linea)}) Tj')
        contenido.append('T*')
    contenido.append('ET')

    stream = '\n'.join(contenido).encode('latin-1', errors='replace')
    objetos = [
        b'1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n',
        b'2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n',
        b'3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n',
        b'4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n',
        b'5 0 obj << /Length ' + str(len(stream)).encode('ascii') + b' >> stream\n' + stream + b'\nendstream endobj\n',
    ]

    pdf = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for objeto in objetos:
        offsets.append(len(pdf))
        pdf.extend(objeto)

    xref_inicio = len(pdf)
    pdf.extend(f'xref\n0 {len(objetos) + 1}\n'.encode('ascii'))
    pdf.extend(b'0000000000 65535 f \n')
    for offset in offsets[1:]:
        pdf.extend(f'{offset:010d} 00000 n \n'.encode('ascii'))
    pdf.extend(f'trailer << /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref_inicio}\n%%EOF'.encode('ascii'))
    return bytes(pdf)

def _partes_nombre(nombre_completo):
    partes = [parte for parte in str(nombre_completo).split() if parte]
    if not partes:
        return 'Profesor', '', 'Académico', ''
    if len(partes) == 1:
        return partes[0], '', 'Académico', ''
    if len(partes) == 2:
        return partes[0], '', partes[1], ''
    return partes[0], ' '.join(partes[1:-1]), partes[-1], ''


def _catalogos_profesor():
    tipo_documento, _ = models.TipoDocumento.objects.get_or_create(
        abreviatura='CC',
        defaults={'tipo_documento': 'Cedula'}
    )
    cargo, _ = models.Cargo.objects.get_or_create(cargo='Profesor')
    area, _ = models.Area.objects.get_or_create(area='Planta Profesores')
    tipo_contrato, _ = models.TipoContrato.objects.get_or_create(tipo_contrato='Termino Indefinido')
    return tipo_documento, cargo, area, tipo_contrato


def _sincronizar_profesores_academicos():
    profesores = UsuarioAcademico.objects.select_related('id_rol').filter(
        activo=True
    ).filter(
        Q(id_rol__nombre_rol__icontains='profesor') | Q(id_rol__nombre_rol__icontains='prof')
    )
    tipo_documento, cargo, area, tipo_contrato = _catalogos_profesor()
    fecha_ingreso = datetime.date.today()

    for profesor in profesores:
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido = _partes_nombre(profesor.nombre_usuario)
        correo_base = f'profesor{profesor.id_usuario}@universidad.edu.co'
        empleado, creado = models.Empleado.objects.get_or_create(
            documento=profesor.id_usuario,
            defaults={
                'primer_nombre': primer_nombre,
                'segundo_nombre': segundo_nombre,
                'primer_apellido': primer_apellido,
                'segundo_apellido': segundo_apellido,
                'correo': correo_base,
                'estado': profesor.activo,
                'tipo_documento': tipo_documento,
            }
        )

        if not creado:
            empleado.primer_nombre = primer_nombre
            empleado.segundo_nombre = segundo_nombre
            empleado.primer_apellido = primer_apellido
            empleado.segundo_apellido = segundo_apellido
            empleado.estado = profesor.activo
            empleado.tipo_documento = empleado.tipo_documento or tipo_documento
            if not empleado.correo:
                empleado.correo = correo_base
            empleado.save()

        models.Contrato.objects.get_or_create(
            empleado=empleado,
            defaults={
                'salario': 0,
                'fecha_ingreso': fecha_ingreso,
                'cargo': cargo,
                'area': area,
                'tipo_contrato': tipo_contrato,
            }
        )
# Create your views here.
def home(request):
    error = None
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        try:
            usuario_academico = UsuarioAcademico.objects.select_related('id_rol').get(
                id_usuario=usuario,
                activo=True,
            )
            es_administrador = usuario_academico.id_rol.nombre_rol.lower() == 'administrador'
            contrasena_valida = usuario_academico.nombre_usuario == contrasena

            if es_administrador and contrasena_valida:
                return redirect('/rrhh/inicio/')

            if not es_administrador:
                error = 'No tienes permisos para ingresar a Recursos Humanos.'
            else:
                error = 'Usuario o contrasena incorrectos.'
        except UsuarioAcademico.DoesNotExist:
            error = 'Usuario o contrasena incorrectos.'

    return render(request, 'Index.html', {'error': error})
    
def inicio(request):
    _sincronizar_profesores_academicos()
    data = models.Empleado.objects.all()
    areas = models.Area.objects.all()
    cargos = models.Cargo.objects.all()
    tipo_contrato = models.TipoContrato.objects.all()
    documentos = models.TipoDocumento.objects.all()
    return render(request, 'paginas/inicio.html', {'empleados': data, 'areas': areas, 'cargos': cargos, 'tipos_contrato': tipo_contrato, 'documentos': documentos})

def editar_empleado(request, empleado_id):
    empleado = models.Empleado.objects.get(id=empleado_id)
    areas = models.Area.objects.all()
    cargos = models.Cargo.objects.all()
    documentos = models.TipoDocumento.objects.all()
    tipo_contrato = models.TipoContrato.objects.all()
    return render(request, 'paginas/editar_empleado.html', {'empleado': empleado, 'areas': areas, 'cargos': cargos, 'tipos_contrato': tipo_contrato, 'documentos': documentos})

def actualizar_empleado(request, empleado_id):
    empleado = models.Empleado.objects.get(id=empleado_id)
    contrato = empleado.contratos
    if request.method == 'POST':
        empleado.primer_nombre = request.POST.get('primer_nombre')
        empleado.segundo_nombre = request.POST.get('segundo_nombre')
        empleado.primer_apellido = request.POST.get('primer_apellido')
        empleado.segundo_apellido = request.POST.get('segundo_apellido')
        empleado.correo = request.POST.get('correo')

        contrato.salario = request.POST.get('salario')
        contrato.cargo_id = request.POST.get('cargo')
        contrato.area_id = request.POST.get('area')
        contrato.tipo_contrato_id = request.POST.get('tipo_contrato')

        fecha_ingreso = request.POST.get('fecha_ingreso')
        contrato.fecha_ingreso = datetime.datetime.strptime(
            fecha_ingreso, '%Y-%m-%d'
        ).date()

        fecha_retiro = request.POST.get('fecha_retiro')
        if fecha_retiro:
            contrato.fecha_retiro = datetime.datetime.strptime(
                fecha_retiro, '%Y-%m-%d'
            ).date()
        else:
            contrato.fecha_retiro = None

        if contrato.fecha_retiro == None:
            empleado.estado = True
        else:
            empleado.estado = False
        contrato.save()
        empleado.save()
        return redirect('/rrhh/inicio/')

def crear_empleado(request):
    if request.method == 'POST':
        documento_id = request.POST['tipo_documento']
        tipo = models.TipoDocumento.objects.get(id=documento_id)        
        fecha_ingreso = datetime.datetime.strptime(request.POST['fecha_ingreso'], '%Y-%m-%d').date()
        
        models.Empleado.objects.create(
            primer_nombre=request.POST['primer_nombre'],
            segundo_nombre=request.POST['segundo_nombre'],
            primer_apellido=request.POST['primer_apellido'],
            segundo_apellido=request.POST['segundo_apellido'],
            correo=request.POST['correo'],
            documento=request.POST['documento'],
            tipo_documento=tipo,
        )
        models.Contrato.objects.create(
            empleado=models.Empleado.objects.get(documento=request.POST['documento']),
            salario=request.POST['salario'],
            fecha_ingreso=fecha_ingreso,
            cargo=models.Cargo.objects.get(id=request.POST['cargo']),
            area=models.Area.objects.get(id=request.POST['area']),
            tipo_contrato=models.TipoContrato.objects.get(id=request.POST['tipo_contrato'])
        )
        return redirect('/rrhh/inicio/')

def eliminar_empleado(request, empleado_id):
    empleado = models.Empleado.objects.get(id=empleado_id)

    UsuarioAcademico.objects.filter(
        id_usuario=empleado.documento,
        id_rol__nombre_rol__icontains='prof'
    ).update(activo=False)

    try:
        try:
            empleado.contratos.delete()
        except models.Contrato.DoesNotExist:
            pass
        empleado.delete()
    except ProtectedError:
        empleado.estado = False
        empleado.save()
        try:
            contrato = empleado.contratos
            contrato.fecha_retiro = datetime.date.today()
            contrato.save()
        except models.Contrato.DoesNotExist:
            pass

    return redirect('/rrhh/inicio/')
def areas(request):
    data = models.Empleado.objects.all()
    documento = models.TipoDocumento.objects.all()
    cargos = models.Cargo.objects.all()
    tipo_contrato = models.TipoContrato.objects.all()
    areas = models.Area.objects.annotate(total_empleados=Count('areas__empleado'))
    return render(request, 'paginas/areas_trabajo.html', {'areas': areas , 'empleados': data, 'documentos': documento, 'cargos': cargos, 'tipos_contrato': tipo_contrato})

def editar_area(request, area_id):
    area = models.Area.objects.get(id=area_id)
    if request.method == 'POST':
        area.area = request.POST.get('area')
        area.save()
        return redirect('areas')

def agregar_area(request):
    if request.method == 'POST':
        models.Area.objects.create(area=request.POST['area'])
        return redirect('areas')
def eliminar_area(request, area_id):
    area = models.Area.objects.get(id=area_id)
    area.delete()
    return redirect('areas')

#novedades
def novedades(request, empleado_id):
    empleado = models.Empleado.objects.get(id=empleado_id)
    novedades_empleado = empleado.novedades_empleado.all()
    documento = models.TipoDocumento.objects.all()
    cargos = models.Cargo.objects.all()
    tipo_contrato = models.TipoContrato.objects.all()
    areas = models.Area.objects.all()
    novedades = models.Novedades.objects.all()
    return render(request, 'paginas/novedades.html', {'novedades_empleado': novedades_empleado, 
                                                      'empleado': empleado, 
                                                      'novedades': novedades,
                                                      'documentos': documento,
                                                      'cargos': cargos,
                                                      'tipos_contrato': tipo_contrato,
                                                      'areas': areas})

def agregar_novedad(request):
    if request.method == 'POST':
        fecha_inicial = datetime.datetime.strptime(request.POST['fecha_inicial'], '%Y-%m-%d').date()
        duracion = int(request.POST['dias_duracion'])
        duracion = datetime.timedelta(days=duracion)
        fecha_final = fecha_inicial + duracion
        models.NovedadesEmpleado.objects.create(
            empleado=models.Empleado.objects.get(id=request.POST['empleado']),
            novedades=models.Novedades.objects.get(id=request.POST['novedad']),
            fecha_inicial=fecha_inicial,
            fecha_final=fecha_final
        )
        return redirect('novedades', empleado_id=request.POST['empleado'])
    
def certificado_laboral(request, empleado_id):
    empleado = models.Empleado.objects.get(id=empleado_id)
    contrato = empleado.contratos
    hoy = datetime.date.today()

    nombre_completo = f'{empleado.primer_nombre} {empleado.primer_apellido}'
    lineas = [
        'CERTIFICADO LABORAL',
        '',
        'La empresa UNIVERSIDAD UNINPAHU certifica que',
        f'{nombre_completo}, identificado con tipo {empleado.tipo_documento.abreviatura}',
        f'documento numero {empleado.documento}, labora en nuestra institucion',
        f'desde el dia {contrato.fecha_ingreso.strftime("%d/%m/%Y")},',
        f'desempenando el cargo de {contrato.cargo.cargo}.',
        '',
        'El presente certificado se expide a solicitud del interesado,',
        f'el dia {hoy.strftime("%d/%m/%Y")}.',
        '',
        '______________________________',
        'Departamento de Recursos Humanos',
        'Juan Felipe Delgadillo V.',
        'Director de Recursos Humanos',
    ]

    respuesta = HttpResponse(_generar_pdf_simple(lineas), content_type='application/pdf')
    respuesta['Content-Disposition'] = 'attachment; filename="certificado_laboral.pdf"'
    return respuesta








