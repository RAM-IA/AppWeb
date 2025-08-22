import 'package:flutter/material.dart';
import 'usuarios_screen.dart';

class MenuScreen extends StatelessWidget {
  final String? nombreUsuario;
  MenuScreen({this.nombreUsuario});
  final List<String> opciones = [
    'Ventas', 'Compras', 'Productos', 'Clientes', 'Proveedores', 'Gastos', 'Cortes', 'Usuarios'
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Menú Principal')),
      body: Column(
        children: [
          if (nombreUsuario != null)
            Padding(
              padding: EdgeInsets.all(16),
              child: Text('Hola $nombreUsuario!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            ),
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(24),
              itemCount: opciones.length,
              itemBuilder: (context, index) {
                return Card(
                  color: Colors.white,
                  elevation: 4,
                  margin: EdgeInsets.symmetric(vertical: 8),
                  child: ListTile(
                    title: Text(
                      opciones[index],
                      style: TextStyle(
                        color: Color(0xFF1565C0),
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                      ),
                    ),
                    trailing: Icon(Icons.arrow_forward_ios, color: Color(0xFF2196F3)),
                    onTap: () {
                      if (opciones[index] == 'Usuarios') {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => UsuariosScreen()),
                        );
                      }
                      // Aquí puedes navegar a la pantalla correspondiente
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
