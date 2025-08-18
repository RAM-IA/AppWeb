fetch('http://127.0.0.1:5000/usuarios')
  .then(response => response.json())
  .then(data => {
    console.log('Usuarios:', data);
    const lista = document.getElementById('lista-usuarios');
    lista.innerHTML = '';
    data.forEach(usuario => {
      const item = document.createElement('li');
      item.textContent = `Nombre: ${usuario.nombre}, Email: ${usuario.email}`;
      lista.appendChild(item);
    });
  })
  .catch(error => console.error('Error al obtener usuarios:', error));
fetch('/api/tareas')
  .then(r => r.json())
  .then(tareas => {
    const lista = document.getElementById('lista-tareas');
    tareas.forEach(t => {
      const li = document.createElement('li');
      li.textContent = t.nombre;
      lista.appendChild(li);
    });
  });