import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

import '../services/api_service.dart';
import '../services/auth_service.dart';
import 'result_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  final ImagePicker _picker = ImagePicker();
  File? _selectedImage;
  String _selectedCrop = 'Tomato';
  bool _isAnalyzing = false;
  bool _isCustomCrop = false;
  final TextEditingController _customCropController = TextEditingController();

  final List<String> _crops = [
    'Tomato',
    'Potato', 
    'Corn',
    'Pepper',
    'Apple',
    'Grape',
    'Beans',
    'Wheat',
    'Rice',
    'Cucumber',
    'Lettuce',
    'Custom Plant...',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan Your Crop'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Image Preview Area
            Container(
              height: 300,
              decoration: BoxDecoration(
                color: Colors.grey[100],
                borderRadius: BorderRadius.circular(15),
                border: Border.all(color: Colors.grey[300]!),
              ),
              child: _selectedImage != null
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(15),
                      child: Image.file(
                        _selectedImage!,
                        fit: BoxFit.cover,
                      ),
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.image,
                          size: 80,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'No image selected',
                          style: GoogleFonts.poppins(
                            fontSize: 18,
                            color: Colors.grey[600],
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Take a photo or select from gallery',
                          style: GoogleFonts.poppins(
                            fontSize: 14,
                            color: Colors.grey[500],
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
            ),
            
            const SizedBox(height: 24),
            
            // Crop Type Selector
            Text(
              'Select Crop Type',
              style: GoogleFonts.poppins(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: const Color(0xFF2E7D32),
              ),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey[300]!),
                borderRadius: BorderRadius.circular(15),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _selectedCrop,
                  isExpanded: true,
                  icon: const Icon(Icons.arrow_drop_down),
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    color: Colors.black,
                  ),
                  items: _crops.map((String crop) {
                    return DropdownMenuItem<String>(
                      value: crop,
                      child: Text(crop),
                    );
                  }).toList(),
                  onChanged: (String? newValue) {
                    if (newValue != null) {
                      setState(() {
                        _selectedCrop = newValue;
                        _isCustomCrop = newValue == 'Custom Plant...';
                        if (!_isCustomCrop) {
                          _customCropController.clear();
                        }
                      });
                    }
                  },
                ),
              ),
            ),
            
            // Custom Crop Input (show when "Custom Plant..." is selected)
            if (_isCustomCrop) ...[
              const SizedBox(height: 16),
              TextField(
                controller: _customCropController,
                decoration: InputDecoration(
                  labelText: 'Enter Plant Name',
                  hintText: 'e.g., Mango, Banana, Spinach...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                  prefixIcon: const Icon(Icons.local_florist),
                ),
                style: GoogleFonts.poppins(fontSize: 16),
                textCapitalization: TextCapitalization.words,
              ),
            ],
            
            const SizedBox(height: 24),
            
            // Camera and Gallery Buttons
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _isAnalyzing ? null : () => _pickImage(ImageSource.camera),
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('Camera'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(15),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _isAnalyzing ? null : () => _pickImage(ImageSource.gallery),
                    icon: const Icon(Icons.photo_library),
                    label: const Text('Gallery'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(15),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 24),
            
            // Analyze Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _selectedImage != null && !_isAnalyzing && _canAnalyze() ? _analyzeImage : null,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                ),
                child: _isAnalyzing
                    ? Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const SpinKitThreeBounce(
                            color: Colors.white,
                            size: 20,
                          ),
                          const SizedBox(width: 16),
                          Text(
                            'Analyzing...',
                            style: GoogleFonts.poppins(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      )
                    : Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.psychology),
                          const SizedBox(width: 8),
                          Text(
                            'Analyze Disease',
                            style: GoogleFonts.poppins(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Tips Card
            Card(
              color: Colors.blue[50],
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          Icons.lightbulb,
                          color: Colors.blue[700],
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Photo Tips',
                          style: GoogleFonts.poppins(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: Colors.blue[700],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    ...const [
                      '• Use good lighting (natural light preferred)',
                      '• Focus on the affected leaf area',
                      '• Avoid shadows and blur',
                      '• Take close-up shots of symptoms',
                      '• Include the entire leaf if possible',
                    ].map((tip) => Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text(
                        tip,
                        style: GoogleFonts.poppins(
                          fontSize: 14,
                          color: Colors.blue[700],
                        ),
                      ),
                    )),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? image = await _picker.pickImage(
        source: source,
        maxWidth: 2048,
        maxHeight: 2048,
        imageQuality: 90,
        preferredCameraDevice: CameraDevice.rear,
      );
      
      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
        });
      }
    } catch (e) {
      _showErrorSnackBar('Failed to pick image: ${e.toString()}');
    }
  }

  Future<void> _analyzeImage() async {
    if (_selectedImage == null) return;

    // Validate custom crop input
    String finalCropType = _selectedCrop;
    if (_isCustomCrop) {
      if (_customCropController.text.trim().isEmpty) {
        _showErrorSnackBar('Please enter a plant name');
        return;
      }
      finalCropType = _customCropController.text.trim();
    }

    setState(() {
      _isAnalyzing = true;
    });

    try {
      // Convert image to base64 with proper format detection
      final bytes = await _selectedImage!.readAsBytes();
      final base64Image = base64Encode(bytes);
      
      // Detect image format from file extension or header
      String imageFormat = 'jpeg';
      String fileName = _selectedImage!.path.toLowerCase();
      if (fileName.endsWith('.png')) {
        imageFormat = 'png';
      } else if (fileName.endsWith('.jpg') || fileName.endsWith('.jpeg')) {
        imageFormat = 'jpeg';
      }
      
      final dataUri = 'data:image/$imageFormat;base64,$base64Image';

      // Get user ID
      final authService = context.read<AuthService>();
      final userId = authService.userId;

      // Call API
      final apiService = context.read<ApiService>();
      final result = await apiService.detectDisease(
        imageBase64: dataUri,
        cropType: finalCropType,
        userId: userId,
      );

      // Navigate to results
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(
              result: result,
              originalImage: _selectedImage!,
            ),
          ),
        );
      }
    } catch (e) {
      _showErrorSnackBar('Analysis failed: ${e.toString()}');
    } finally {
      if (mounted) {
        setState(() {
          _isAnalyzing = false;
        });
      }
    }
  }

  bool _canAnalyze() {
    if (_isCustomCrop) {
      return _customCropController.text.trim().isNotEmpty;
    }
    return true;
  }

  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  void dispose() {
    _customCropController.dispose();
    super.dispose();
  }
}