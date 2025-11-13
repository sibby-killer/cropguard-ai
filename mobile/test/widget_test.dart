// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('CropGuard AI basic widget test', (WidgetTester tester) async {
    // Create a simple test widget
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          appBar: AppBar(
            title: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('🌱'),
                SizedBox(width: 8),
                Text('CropGuard AI'),
              ],
            ),
          ),
          body: const Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Protect Your Crops'),
                SizedBox(height: 16),
                Text('AI-powered disease detection in seconds'),
              ],
            ),
          ),
        ),
      ),
    );

    // Verify basic UI elements
    expect(find.text('CropGuard AI'), findsOneWidget);
    expect(find.text('Protect Your Crops'), findsOneWidget);
    expect(find.text('AI-powered disease detection in seconds'), findsOneWidget);
    expect(find.text('🌱'), findsOneWidget);
  });
}
