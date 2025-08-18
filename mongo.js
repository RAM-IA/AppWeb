const mongoose = require('mongoose');

const uri = "mongodb+srv://ramongo:LeoyDem01@cluster0.aemc3mn.mongodb.net/sample_mflix?retryWrites=true&w=majority&connectTimeoutMS=10000&socketTimeoutMS=10000";
//mongodb+srv://ramongo:LeoyDem01!_@cluster0.zbeo28o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
//const mongoose = require('mongoose');


mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Conectado a MongoDB Atlas'))
  .catch(err => console.error('Error al conectar a MongoDB:', err));

// ...puedes agregar aquí tus modelos y lógica adicional...
// ...puedes agregar aquí tus modelos y lógica adicional...

// Definir un esquema y modelo de ejemplo
const usuarioSchema = new mongoose.Schema({
  nombre: String,
  email: String
});

const Usuario = mongoose.model('Usuario', usuarioSchema);

// Crear y guardar un usuario de prueba
const usuarioPrueba = new Usuario({ nombre: 'Juan', email: 'juan@email.com' });

usuarioPrueba.save()
  .then(() => {
    console.log('Usuario guardado correctamente');
    // Consultar todos los usuarios guardados
    return Usuario.find();
  })
  .then(usuarios => {
    console.log('Usuarios en la colección:', usuarios);
  })
  .catch(err => console.error('Error al guardar o consultar usuarios:', err));