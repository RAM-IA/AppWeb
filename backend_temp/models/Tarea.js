const mongoose = require('mongoose');

const tareaSchema = new mongoose.Schema({
  nombre: String,
  completada: Boolean,
});

module.exports = mongoose.model('Tarea', tareaSchema);