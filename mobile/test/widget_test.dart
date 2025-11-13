// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cropguard_ai/screens/home_screen.dart';

void main() {
  testWidgets('CropGuard AI home screen test', (WidgetTester tester) async {
    // Build our app and trigger a frame without Supabase dependency
    await tester.pumpWidget(
      MaterialApp(
        home: const HomeScreen(),
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF4CAF50),
          ),
        ),
      ),
    );

    // Verify that our home screen loads with the correct content
    expect(find.text('Protect Your Crops'), findsOneWidget);
    expect(find.text('AI-powered disease detection in seconds'), findsOneWidget);

    // Verify main action buttons are present
    expect(find.text('Scan Your Crop'), findsOneWidget);
    expect(find.text('View History'), findsOneWidget);
    
    // Verify stats cards
    expect(find.text('90%+ Accuracy'), findsOneWidget);
    expect(find.text('<5s Detection'), findsOneWidget);
  });
}
