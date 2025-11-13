import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:google_fonts/google_fonts.dart';

class LoadingDialog extends StatelessWidget {
  final String message;

  const LoadingDialog({
    super.key,
    this.message = 'Loading...',
  });

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SpinKitThreeBounce(
              color: Color(0xFF4CAF50),
              size: 40,
            ),
            const SizedBox(height: 24),
            Text(
              message,
              style: GoogleFonts.poppins(
                fontSize: 16,
                fontWeight: FontWeight.w500,
                color: Colors.grey[800],
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  static void show(BuildContext context, {String message = 'Loading...'}) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => LoadingDialog(message: message),
    );
  }

  static void hide(BuildContext context) {
    Navigator.of(context, rootNavigator: true).pop();
  }
}