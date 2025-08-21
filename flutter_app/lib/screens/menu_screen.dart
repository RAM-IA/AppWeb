import 'package:flutter/material.dart';

class MenuScreen extends StatelessWidget {
  final List<String> opciones = [
    'Ventas', 'Compras', 'Productos', 'Clientes', 'Proveedores', 'Gastos', 'Cortes', 'Usuarios'
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Menú Principal')),
      body: ListView.builder(
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
                // Aquí puedes navegar a la pantalla correspondiente
              },
            ),
          );
        },
      ),
    );
  }
}
