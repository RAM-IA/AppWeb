// ...existing code...
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:uuid/uuid.dart';

class UsuariosScreen extends StatefulWidget {
  @override
  _UsuariosScreenState createState() => _UsuariosScreenState();
}

class _UsuariosScreenState extends State<UsuariosScreen> {
  List usuarios = [];
  final nombreController = TextEditingController();
  final contrasenaController = TextEditingController();
  final rolController = TextEditingController();
  bool cargando = false;
  String mensaje = '';

  Future<void> modificarUsuario(Map usuario) async {
    final datos = await showDialog<String>(
      context: context,
      builder: (context) {
        final nombreController = TextEditingController(text: usuario['nombre']);
        final contrasenaController = TextEditingController(text: usuario['contrasena'] ?? '');
        final rolController = TextEditingController(text: usuario['rol'] ?? 'usuario');
        return AlertDialog(
          title: Text('Modificar Usuario'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nombreController,
                decoration: InputDecoration(labelText: 'Nombre'),
              ),
              TextField(
                controller: contrasenaController,
                decoration: InputDecoration(labelText: 'Contraseña'),
                obscureText: true,
              ),
              TextField(
                controller: rolController,
                decoration: InputDecoration(labelText: 'Rol'),
              ),
            ],
          ),
          actions: [
            TextButton(
              child: Text('Cancelar'),
              onPressed: () => Navigator.pop(context),
            ),
            TextButton(
              child: Text('Guardar'),
              onPressed: () => Navigator.pop(context, json.encode({
                'nombre': nombreController.text,
                'contrasena': contrasenaController.text,
                'rol': rolController.text
              })),
            ),
          ],
        );
      },
    );
    if (datos != null) {
      setState(() { cargando = true; mensaje = ''; });
      try {
        final data = json.decode(datos);
        final res = await http.post(
          Uri.parse('http://localhost:5000/modificar_usuario'),
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: {
            'id': usuario['id'] ?? usuario['_id'] ?? '',
            'nombre': data['nombre'],
            'contrasena': data['contrasena'],
            'rol': data['rol'],
          },
        );
        if (res.statusCode == 200 || res.statusCode == 302) {
          setState(() { mensaje = 'Usuario modificado correctamente'; });
          await fetchUsuarios();
        } else {
          setState(() { mensaje = 'Error al modificar usuario'; });
        }
      } catch (e) {
        setState(() { mensaje = 'Error de conexión'; });
      }
      setState(() { cargando = false; });
    }
  }

  Future<void> eliminarUsuario(Map usuario) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Eliminar Usuario'),
        content: Text('¿Seguro que deseas eliminar este usuario?'),
        actions: [
          TextButton(
            child: Text('Cancelar'),
            onPressed: () => Navigator.pop(context, false),
          ),
          TextButton(
            child: Text('Eliminar'),
            onPressed: () => Navigator.pop(context, true),
          ),
        ],
      ),
    );
    if (confirmar == true) {
      setState(() { cargando = true; mensaje = ''; });
      try {
        final res = await http.post(
          Uri.parse('http://localhost:5000/eliminar_usuario'),
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: {
            'id': usuario['id'] ?? usuario['_id'] ?? '',
          },
        );
        if (res.statusCode == 200 || res.statusCode == 302) {
          setState(() { mensaje = 'Usuario eliminado correctamente'; });
          await fetchUsuarios();
        } else {
          setState(() { mensaje = 'Error al eliminar usuario'; });
        }
      } catch (e) {
        setState(() { mensaje = 'Error de conexión'; });
      }
      setState(() { cargando = false; });
    }
  }

  Future<void> fetchUsuarios() async {
    setState(() { cargando = true; });
    try {
      final res = await http.get(Uri.parse('http://localhost:5000/api/usuarios'));
      if (res.statusCode == 200) {
        setState(() {
          usuarios = json.decode(res.body);
          mensaje = '';
        });
      } else {
        setState(() { mensaje = 'Error al obtener usuarios'; });
      }
    } catch (e) {
      setState(() { mensaje = 'Error de conexión'; });
    }
    setState(() { cargando = false; });
  }

  Future<void> agregarUsuario() async {
    setState(() { cargando = true; mensaje = ''; });
    try {
      var uuid = Uuid();
      final res = await http.post(
        Uri.parse('http://localhost:5000/api/usuarios'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'id': uuid.v4(),
          'nombre': nombreController.text,
          'contrasena': contrasenaController.text,
          'rol': rolController.text.isNotEmpty ? rolController.text : 'usuario',
        }),
      );
      if (res.statusCode == 200) {
        nombreController.clear();
        contrasenaController.clear();
        rolController.clear();
        setState(() { mensaje = 'Usuario agregado correctamente'; });
        await fetchUsuarios();
      } else {
        setState(() { mensaje = 'Error al agregar usuario'; });
      }
    } catch (e) {
      setState(() { mensaje = 'Error de conexión'; });
    }
    setState(() { cargando = false; });
  }

  @override
  void initState() {
    super.initState();
    fetchUsuarios();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Gestión de Usuarios')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: nombreController,
              decoration: InputDecoration(labelText: 'Nombre'),
            ),
            TextField(
              controller: contrasenaController,
              decoration: InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
            ),
            TextField(
              controller: rolController,
              decoration: InputDecoration(labelText: 'Rol (opcional, ejemplo: admin, usuario)'),
            ),
            SizedBox(height: 12),
            ElevatedButton(
              child: Text('Agregar Usuario'),
              onPressed: cargando ? null : agregarUsuario,
            ),
            if (mensaje.isNotEmpty)
              Padding(
                padding: EdgeInsets.symmetric(vertical: 8),
                child: Text(mensaje, style: TextStyle(color: mensaje.contains('correctamente') ? Colors.green : Colors.red)),
              ),
            Divider(),
            cargando
                ? Center(child: CircularProgressIndicator())
                : Expanded(
                    child: ListView.builder(
                      itemCount: usuarios.length,
                      itemBuilder: (context, index) {
                        final u = usuarios[index];
                        return ListTile(
                          title: Text(u['nombre'] ?? ''),
                          subtitle: Text(u['direccion'] ?? ''),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              IconButton(
                                icon: Icon(Icons.edit),
                                onPressed: () => modificarUsuario(u),
                              ),
                              IconButton(
                                icon: Icon(Icons.delete),
                                onPressed: () => eliminarUsuario(u),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}
