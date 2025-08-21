import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  final Color azulPrincipal = Color(0xFF2196F3);
  final Color azulOscuro = Color(0xFF1565C0);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Constructora',
      theme: ThemeData(
        primaryColor: azulPrincipal,
        scaffoldBackgroundColor: Colors.white,
        appBarTheme: AppBarTheme(backgroundColor: azulOscuro),
      ),
      home: LoginScreen(),
    );
  }
}
