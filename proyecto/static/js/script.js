function sumarUnaHora(horaStr) {
  // Separar horas y minutos
  let [horas, minutos] = horaStr.split(':').map(Number);

  // Sumar 1 hora
  horas = (horas + 1) % 24;  // Para que no pase de 23, vuelve a 0

  // Formatear con dos dígitos
  let nuevaHora = horas.toString().padStart(2, '0');
  let nuevoMinuto = minutos.toString().padStart(2, '0');

  // Devolver string en formato HH:MM
  return `${nuevaHora}:${nuevoMinuto}`;
}

// Ejemplo:
let resultado = sumarUnaHora("9:00");  // "13:00"
console.log(resultado);
