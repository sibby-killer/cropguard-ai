import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:google_fonts/google_fonts.dart';

import 'screens/home_screen.dart';
import 'services/api_service.dart';
import 'services/auth_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Supabase
  await Supabase.initialize(
    url: 'https://ibquhztgscfqtnnvlyxc.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlicXVoenRnc2NmcXRubnZseXhjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2NTk0NjQsImV4cCI6MjA3ODIzNTQ2NH0.4FWZ84RdAy4PHdcLo32z2iSuonuXFsOoRqvIO1BrfW4',
  );
  
  runApp(const CropGuardApp());
}

class CropGuardApp extends StatelessWidget {
  const CropGuardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthService()),
        Provider(create: (_) => ApiService()),
      ],
      child: MaterialApp(
        title: 'CropGuard AI',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF4CAF50),
            brightness: Brightness.light,
          ),
          textTheme: GoogleFonts.poppinsTextTheme(),
          appBarTheme: AppBarTheme(
            elevation: 0,
            centerTitle: true,
            backgroundColor: const Color(0xFF4CAF50),
            foregroundColor: Colors.white,
            titleTextStyle: GoogleFonts.poppins(
              fontSize: 20,
              fontWeight: FontWeight.w600,
              color: Colors.white,
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF4CAF50),
              foregroundColor: Colors.white,
              textStyle: GoogleFonts.poppins(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
            ),
          ),
          outlinedButtonTheme: OutlinedButtonThemeData(
            style: OutlinedButton.styleFrom(
              foregroundColor: const Color(0xFF4CAF50),
              side: const BorderSide(color: Color(0xFF4CAF50)),
              textStyle: GoogleFonts.poppins(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
            ),
          ),
          cardTheme: CardThemeData(
            elevation: 4,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
          ),
        ),
        home: const HomeScreen(),
      ),
    );
  }
}