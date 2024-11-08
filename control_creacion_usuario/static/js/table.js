    //Darle diseño a al tabla mediante JS
    $(document).ready(function() {
        var tabla = $('#tabla_registro').DataTable({
            searching: false,
            pageLength: 12,
            lengthChange: false,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.12.1/i18n/es-CL.json'
            },
            order: [[0, 'desc']] // '0' indica la primera columna (Solicitudes.id), 'desc' indica orden descendente
        });
    
    
        $(".estado-select").change(function() {
            var solicitudId = $(this).data('solicitud-id');
            var nuevoEstado = $(this).val();
    
            console.log(nuevoEstado)
            // Realizar la solicitud AJAX para actualizar el estado
            $.ajax({
                url: "{% url 'actualizar_estado' %}",
                type: "POST",
                data: {
                    solicitud_id: solicitudId,
                    estado: nuevoEstado,
                    csrfmiddlewaretoken: "{{ csrf_token }}"
                },
                success: function(response) {
                    // Manejar la respuesta exitosa si es necesario
                    console.log("Estado actualizado correctamente");
                },
                error: function(xhr, status, error) {
                    // Manejar el error si es necesario
                    console.error("Error al actualizar el estado:", error);
                }
            });
        });
    
        
    
        $(".limite-select").change(function() {
        var solicitudId = $(this).data('solicitud-id'); // Obtener el ID de la solicitud
        var nuevoLimite = $(this).val(); // Obtener el nuevo límite seleccionado
        var profesionalSelect = $("select[data-solicitud-id='" + solicitudId + "']"); // Obtener el select del profesional basado en la solicitud ID
        var profesional = profesionalSelect.val(); // Obtener el valor seleccionado del <select> de profesional
    
        console.log(nuevoLimite);
    
        // Si nuevoLimite es 'P', mostrar el menú desplegable adicional para seleccionar días
        if (nuevoLimite === 'P') {
            var dias = prompt("Selecciona la cantidad de días que deseas agregar:", "1");
    
            // Verificar que el usuario haya ingresado un valor para los días
            if (dias !== null && dias !== '') {
                // Realizar la solicitud AJAX con los días seleccionados
                if (profesional !== undefined && profesional !== null && profesional !== '') {
                    $.ajax({
                        url: "{% url 'actualizar_limite' %}", // URL del endpoint
                        type: "POST",
                        data: {
                            solicitud_id: solicitudId,
                            nuevoLimite: nuevoLimite,
                            dias: dias, // Agregar los días al envío de datos
                            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val() // Obtener el CSRF token de un input oculto
                        },
                        success: function(response) {
                            // Manejar la respuesta exitosa
                            alert("Estado actualizado correctamente");
                        },
                        error: function(xhr, status, error) {
                            // Manejar el error si ocurre
                            alert("Error al actualizar el estado:", error);
                        }
                    });
                } else {
                    alert("El profesional seleccionado es 'Selecciona un profesional', no se realizará ninguna acción.");
                }
            } else {
                alert("No se ingresó una cantidad de días válida.");
            }
        } else {
            // Si nuevoLimite no es 'P', seguir con la lógica normal
            if (profesional !== undefined && profesional !== null && profesional !== '') {
                $.ajax({
                    url: "{% url 'actualizar_limite' %}", // URL del endpoint
                    type: "POST",
                    data: {
                        solicitud_id: solicitudId,
                        nuevoLimite: nuevoLimite,
                        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val() // Obtener el CSRF token de un input oculto
                    },
                    success: function(response) {
                        // Manejar la respuesta exitosa
                        alert("Estado actualizado correctamente");
                    },
                    error: function(xhr, status, error) {
                        // Manejar el error si ocurre
                        alert("Error al actualizar el estado:", error);
                    }
                });
            } else {
                alert("El profesional seleccionado es 'Selecciona un profesional', no se realizará ninguna acción.");
            }
        }
    });
    
    });
      
    $(".profesional-select").change(function() {
        console.log("Evento change disparado");
    
        // Obtener el valor de data-solicitud-id
        var solicitudId = $(this).data('solicitud-id');
        console.log("Valor de data-solicitud-id:", solicitudId);
    
        // Obtener el valor seleccionado
        var nuevoProfesional = $(this).val();
        console.log("Nuevo Profesional seleccionado:", nuevoProfesional);
    
        var csrfToken = '{{ csrf_token }}';  // Obtener el CSRF token desde la plantilla
    
        // Verificar si los valores de solicitud y profesional se están obteniendo correctamente
        if (!solicitudId || !nuevoProfesional) {
            $("#response-message").html('<div class="alert alert-warning">Error: faltan datos para la solicitud o el profesional.</div>');
            return;
        }
    
        // Realizar la solicitud AJAX para actualizar el profesional
        $.ajax({
            url: "{% url 'actualizar_profesional' %}",
            type: "POST",
            data: {
                solicitud_id: solicitudId,
                profesional: nuevoProfesional,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                // Manejar la respuesta exitosa
                if (response.success) {
                    $("#response-message").html('<div class="alert alert-success">Profesional actualizado correctamente</div>');
                } else {
                    $("#response-message").html('<div class="alert alert-danger">Error al actualizar el profesional</div>');
                }
            },
            error: function(xhr, status, error) {
                // Manejar el error si es necesario
                $("#response-message").html('<div class="alert alert-danger">Ocurrió un error al actualizar el profesional</div>');
                console.error("Error al actualizar el profesional:", error);
            }
        });
    });
    
    
        
    var previewLinks = document.querySelectorAll('.preview-link');
    previewLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evitar el comportamiento predeterminado del enlace
    
        var registroId = parseInt(this.getAttribute('data-id')); // Convertir a número
    
        // Hacer una solicitud AJAX a la vista de Django para obtener los datos del registro
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/solicitud/vista_previa/' + registroId, true);
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
    
            var previewDataElement = document.getElementById('previewData');
            previewDataElement.innerText =   'Fecha de la Solicitud: ' + data.fecha
                                           + '\n'
                                           + '\nCodigo: ' + data.codigo
                                           + '\n'
                                           + '\nDirección: ' + data.direccion
                                           + '\n'
                                           + '\nDepartamento o Unidad Responsable: ' + data.departamento
                                           + '\n'
                                           + '\nNombre del solicitante: ' + data.nombre_solicitante
                                           + '\n'
                                           + '\nNombre del proyecto: ' + data.nombre_proyecto
                                           + '\n'
                                           + '\nCorreo del solicitante: ' + data.corre_solicitante
                                           + '\n'
                                           + '\nArea De estudio: ' + data.area
                                           + '\n'
                                           + '\nObjetivos de la solicitud:' + data.objetivos
                                           + '\n'
                                           + '\nInsumo Solicitado: ' + data.insumo
                                           + '\n'
                                           + '\nProductos: ' + data.productos
                                           + '\n'
                                           + '\nCambios posible en el Insumo Entregado: ' + data.Cambios
                                           + '\n';
                                           
                                           if (data.archivos_adjuntos_urls && data.archivos_adjuntos_urls.length > 0) {
        // Agregar enlaces a los archivos adjuntos si existen
        previewDataElement.innerHTML += '<br><br><strong>Archivos Adjuntos:</strong><br>';
        data.archivos_adjuntos_urls.forEach(function(url) {
            previewDataElement.innerHTML += '<a href="' + url + '" download>' + url.split('/').pop() + '</a><br>';
        });
    } else {
        // Manejar el caso en el que no hay archivos adjuntos
        previewDataElement.innerHTML += '<br><br>No hay archivos adjuntos disponibles';
    }
    
    
      
            $('#previewModal').modal('show'); // Mostrar el modal utilizando jQuery
          }
        };
        xhr.send();
      });
    });