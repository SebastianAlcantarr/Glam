const appointmentForm = document.getElementById('appointmentForm');
const appointmentsTableBody = document.querySelector('#appointmentsTable tbody');
const API_URL = 'https://glam-s9ob.onrender.com/api/citas';

// Cargar citas al iniciar
document.addEventListener('DOMContentLoaded', cargarCitas);

// Enviar cita
appointmentForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value.trim();
    const hora_inicio = document.getElementById('timepicker').value;
    const estado = document.getElementById('estado').value;

    if (!nombre || !hora_inicio) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    function sumarUnaHora(horaStr) {
        let ampm = horaStr.match(/AM|PM/i);
        ampm = ampm ? ampm[0].toUpperCase() : null;

        let horaSinAmPm = horaStr.replace(/(AM|PM)/i, '').trim();

        let [horas, minutos] = horaSinAmPm.split(':').map(Number);

        if (isNaN(horas) || isNaN(minutos)) throw new Error("Formato inválido de hora");

        if (ampm === 'PM' && horas < 12) {
            horas += 12;
        } else if (ampm === 'AM' && horas === 12) {
            horas = 0;
        }

        horas = (horas + 1) % 24;

        let nuevaAmPm = horas >= 12 ? 'PM' : 'AM';
        let horas12 = horas % 12;
        if (horas12 === 0) horas12 = 12;

        let minutosStr = minutos.toString().padStart(2, '0');

        return `${horas12}:${minutosStr} ${nuevaAmPm}`;
    }

    let hora_final = sumarUnaHora(hora_inicio);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                nombre,
                hora_inicio,
                hora_final,
                estado
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al agregar la cita');
        }

        cargarCitas();
        appointmentForm.reset();
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Error al procesar la solicitud');
    }
});

//Funcion para cargar las citas
async function cargarCitas() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Error al cargar las citas');
        }
        const citas = await response.json();
        renderCitas(citas);
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar las citas');
    }
}

// Función para mostrar las citas en la tabla
function renderCitas(citas) {
    appointmentsTableBody.innerHTML = '';

    if (citas.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = '<td colspan="4">No hay citas programadas</td>';
        appointmentsTableBody.appendChild(tr);
        return;
    }

    citas.forEach(cita => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${cita.nombre}</td>
            <td>${cita.hora_inicio}</td>
            <td>${cita.hora_final}</td>
            <td style="color: ${cita.estado === 'disponible' ? 'green' : 'red'};">
                ${cita.estado.charAt(0).toUpperCase() + cita.estado.slice(1)}
            </td>
        `;
        appointmentsTableBody.appendChild(tr);
    });
}


flatpickr("#timepicker", {
    locale: 'es',
    minDate: "today",
    enableTime: true,
    noCalendar: false,
    dateFormat: "h:i K",
    time_24hr: false,
    minTime: "09:00",
    maxTime: "18:00",
    minuteIncrement: 30,
    disable: [
        function (date) {
            // Deshabilitar domingos
            return date.getDay() === 0;
        }
    ]
});
