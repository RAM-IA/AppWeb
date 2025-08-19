// Requiere Node.js instalado
const express = require('express');
const app = express();
app.use(express.json());

app.get('/api/tareas', (req, res) => {
  res.json([{ id: 1, nombre: 'Aprender Node.js' }]);
});

app.listen(3000, () => console.log('Servidor corriendo en puerto 3000'));

const Tarea = require('./models/Tarea');

// Crear una tarea (POST)
app.post('/api/tareas', async (req, res) => {
  const tarea = new Tarea({
    nombre: req.body.nombre,
    completada: false
  });
  await tarea.save();
  res.json(tarea);
});

// Consultar tareas (GET)
app.get('/api/tareas', async (req, res) => {
  const tareas = await Tarea.find();
  res.json(tareas);
});