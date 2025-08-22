import 'package:flutter/material.dart';
import 'menu_screen.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController userController = TextEditingController();
  final TextEditingController passController = TextEditingController();
  String? errorMsg;
  bool cargando = false;

  Future<void> autenticar() async {
    setState(() { errorMsg = null; cargando = true; });
    try {
      final res = await http.post(
        Uri.parse('http://localhost:5000/api/login'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nombre': userController.text,
          'contrasena': passController.text,
        }),
      );
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final usuario = data['usuario'];
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => MenuScreen(nombreUsuario: usuario['nombre']),
          ),
        );
      } else {
        setState(() { errorMsg = 'Usuario o contraseña incorrectos'; });
      }
    } catch (e) {
      setState(() { errorMsg = 'Error de conexión'; });
    }
    setState(() { cargando = false; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Iniciar Sesión')),
      body: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: userController,
              decoration: InputDecoration(labelText: 'Usuario'),
            ),
            TextField(
              controller: passController,
              decoration: InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
            ),
            SizedBox(height: 24),
            if (errorMsg != null)
              Text(errorMsg!, style: TextStyle(color: Colors.red)),
            ElevatedButton(
              child: cargando ? CircularProgressIndicator(color: Colors.white) : Text('Entrar'),
              onPressed: cargando ? null : autenticar,
            ),
          ],
        ),
      ),
    );
  }
}
