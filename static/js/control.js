document.addEventListener('DOMContentLoaded', function () {
    // Animación de los contadores
    const counters = document.querySelectorAll('.counter');
    counters.forEach((counter) => {
        const target = +counter.getAttribute('data-target');
        let count = 0;
        const increment = target / 200; // Ajusta la velocidad aquí

        const updateCount = () => {
            if (count < target) {
                count += increment;
                counter.innerText = Math.ceil(count);

                // Aplicar la clase 'visible' cuando el conteo alcance la mitad del objetivo
                if (count >= target / 2.5 && !counter.classList.contains('visible')) {
                    counter.classList.add('visible');
                }

                setTimeout(updateCount, 10);
            } else {
                counter.innerText = target;
                // Opcional: Mantener la clase 'visible' o eliminarla
                // counter.classList.remove('visible');
            }
        };

        updateCount();
    });

    // Asignación de colores únicos a cada funcionario
    const coloresBackground = [
        'rgba(54, 162, 235, 0.2)',    // Andres Mardones Delgado
        'rgba(255, 206, 86, 0.2)',    // Francis Cadiz Olivarez
        'rgba(75, 192, 192, 0.2)',    // Ivan Cantero Faundez
        'rgba(153, 102, 255, 0.2)',   // Emanuel Venegas Perez
        'rgba(255, 159, 64, 0.2)',     // Jaime
        'rgba(255, 0, 0, 0.2)',        // Deisy Pereira Vidal (ROJO)
        'rgba(199, 199, 199, 0.2)',    // Osvaldo Jesus Moya Vargas
        'rgba(54, 162, 235, 0.2)'      // Nicolas Rebolledo
    ];

    const coloresBorder = [
        'rgba(54, 162, 235, 1)',        // Andres Mardones Delgado
        'rgba(255, 206, 86, 1)',        // Francis Cadiz Olivarez
        'rgba(75, 192, 192, 1)',        // Ivan Cantero Faundez
        'rgba(153, 102, 255, 1)',       // Emanuel Venegas Perez
        'rgba(255, 159, 64, 1)',        // Jaime
        'rgba(255, 0, 0, 1)',           // Deisy Pereira Vidal (ROJO)
        'rgba(199, 199, 199, 1)',       // Osvaldo Jesus Moya Vargas
        'rgba(54, 162, 235, 1)'         // Nicolas Rebolledo
    ];

    // Configuración del Gráfico de Barras con animación gradual de izquierda a derecha
    if (typeof labels !== 'undefined' && typeof data !== 'undefined') {
        const ctx = document.getElementById('solicitudesPorProfesionalChart').getContext('2d');

        // Verificar que la cantidad de colores coincida con la cantidad de labels
        if (labels.length !== coloresBackground.length) {
            console.warn('La cantidad de colores no coincide con la cantidad de labels.');
        }

        const solicitudesPorProfesionalChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Cantidad de Solicitudes',
                    data: data,
                    backgroundColor: coloresBackground,
                    borderColor: coloresBorder,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true
                    }
                },
                animation: {
                    duration: 1000, // Duración total de la animación (en ms)
                    easing: 'easeOutBounce',
                    delay: function (context) {
                        let delay = 0;
                        if (context.type === 'data' && context.mode === 'default') {
                            delay = context.dataIndex * 600; // 300ms de retraso por barra
                        }
                        return delay;
                    }
                }
            }
        });
    }
});
