import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

import '../models/disease_result.dart';
import 'home_screen.dart';
import 'camera_screen.dart';

class ResultScreen extends StatefulWidget {
  final DiseaseResult result;
  final File originalImage;

  const ResultScreen({
    super.key,
    required this.result,
    required this.originalImage,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          // App Bar with Image
          SliverAppBar(
            expandedHeight: 250,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  Image.file(
                    widget.originalImage,
                    fit: BoxFit.cover,
                  ),
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [
                          Colors.transparent,
                          Colors.black.withOpacity(0.7),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            ),
          ),
          
          // Content
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Disease Name and Confidence
                  _buildResultCard(),
                  
                  const SizedBox(height: 24),
                  
                  // Description Section
                  if (widget.result.description.isNotEmpty)
                    _buildExpandableSection(
                      'Description',
                      Icons.info,
                      [widget.result.description],
                      isExpanded: true,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Symptoms Section
                  if (widget.result.symptoms.isNotEmpty)
                    _buildExpandableSection(
                      'Symptoms',
                      Icons.visibility,
                      widget.result.symptoms,
                      showCheckmarks: true,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Treatment Section
                  if (widget.result.treatment.isNotEmpty)
                    _buildExpandableSection(
                      'Treatment Steps',
                      Icons.medical_services,
                      widget.result.treatment,
                      numbered: true,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Prevention Section
                  if (widget.result.prevention.isNotEmpty)
                    _buildExpandableSection(
                      'Prevention Tips',
                      Icons.lightbulb,
                      widget.result.prevention,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Organic Treatment Section
                  if (widget.result.organicTreatment.isNotEmpty)
                    _buildExpandableSection(
                      'Organic Alternatives',
                      Icons.eco,
                      widget.result.organicTreatment,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Cost Estimate
                  if (widget.result.costEstimate.isNotEmpty)
                    _buildInfoCard(
                      'Cost Estimate',
                      Icons.attach_money,
                      widget.result.costEstimate,
                      Colors.green,
                    ),
                  
                  const SizedBox(height: 16),
                  
                  // Scientific Name
                  if (widget.result.scientificName.isNotEmpty)
                    _buildInfoCard(
                      'Scientific Name',
                      Icons.science,
                      widget.result.scientificName,
                      Colors.blue,
                    ),
                  
                  const SizedBox(height: 24),
                  
                  // Alternative Diagnoses (if confidence < 90%)
                  if (widget.result.confidence < 0.9)
                    _buildAlternativesCard(),
                  
                  const SizedBox(height: 32),
                  
                  // Action Buttons
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () {
                            Navigator.pushAndRemoveUntil(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const HomeScreen(),
                              ),
                              (route) => false,
                            );
                          },
                          icon: const Icon(Icons.home),
                          label: const Text('Home'),
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () {
                            Navigator.pushReplacement(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const CameraScreen(),
                              ),
                            );
                          },
                          icon: const Icon(Icons.camera_alt),
                          label: const Text('Scan Again'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                    ],
                  ),
                  
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Disease Name
            Text(
              widget.result.disease,
              style: GoogleFonts.poppins(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: const Color(0xFF2E7D32),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Confidence Bar
            Row(
              children: [
                Text(
                  'Confidence: ',
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  widget.result.confidencePercentage,
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: _getConfidenceColor(widget.result.confidence),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 8),
            
            LinearProgressIndicator(
              value: widget.result.confidence,
              backgroundColor: Colors.grey[300],
              valueColor: AlwaysStoppedAnimation<Color>(
                _getConfidenceColor(widget.result.confidence),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Severity Badge
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: _getSeverityColor(widget.result.severity),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        widget.result.severityIcon,
                        style: const TextStyle(fontSize: 14),
                      ),
                      const SizedBox(width: 6),
                      Text(
                        widget.result.severity,
                        style: GoogleFonts.poppins(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
                const Spacer(),
                Text(
                  DateFormat('MMM d, yyyy').format(widget.result.timestamp),
                  style: GoogleFonts.poppins(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExpandableSection(
    String title,
    IconData icon,
    List<String> items, {
    bool isExpanded = false,
    bool showCheckmarks = false,
    bool numbered = false,
  }) {
    return Card(
      child: ExpansionTile(
        leading: Icon(icon, color: const Color(0xFF4CAF50)),
        title: Text(
          title,
          style: GoogleFonts.poppins(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        initiallyExpanded: isExpanded,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: Column(
              children: items.asMap().entries.map((entry) {
                int index = entry.key;
                String item = entry.value;
                
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (showCheckmarks)
                        const Icon(
                          Icons.check_circle,
                          color: Color(0xFF4CAF50),
                          size: 20,
                        )
                      else if (numbered)
                        Container(
                          width: 24,
                          height: 24,
                          decoration: const BoxDecoration(
                            color: Color(0xFF4CAF50),
                            shape: BoxShape.circle,
                          ),
                          child: Center(
                            child: Text(
                              '${index + 1}',
                              style: GoogleFonts.poppins(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        )
                      else
                        const Icon(
                          Icons.lightbulb,
                          color: Color(0xFFFFC107),
                          size: 20,
                        ),
                      
                      const SizedBox(width: 12),
                      
                      Expanded(
                        child: Text(
                          item,
                          style: GoogleFonts.poppins(
                            fontSize: 14,
                            color: Colors.grey[800],
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoCard(String title, IconData icon, String content, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(icon, color: color),
            const SizedBox(width: 12),
            Text(
              '$title: ',
              style: GoogleFonts.poppins(
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
            ),
            Expanded(
              child: Text(
                content,
                style: GoogleFonts.poppins(
                  fontSize: 14,
                  color: Colors.grey[800],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAlternativesCard() {
    return Card(
      color: Colors.orange[50],
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.warning, color: Colors.orange[700]),
                const SizedBox(width: 8),
                Text(
                  'Low Confidence Detection',
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.orange[700],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              'The confidence level is below 90%. Consider:',
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: Colors.orange[700],
              ),
            ),
            const SizedBox(height: 8),
            ...const [
              '• Taking another photo with better lighting',
              '• Consulting with a local agricultural expert',
              '• Monitoring the plant for additional symptoms',
              '• Getting a second opinion',
            ].map((tip) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                tip,
                style: GoogleFonts.poppins(
                  fontSize: 14,
                  color: Colors.orange[700],
                ),
              ),
            )),
          ],
        ),
      ),
    );
  }

  Color _getConfidenceColor(double confidence) {
    if (confidence >= 0.8) return Colors.green;
    if (confidence >= 0.6) return Colors.orange;
    return Colors.red;
  }

  Color _getSeverityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'severe':
        return const Color(0xFFF44336);
      case 'moderate':
        return const Color(0xFFFF9800);
      case 'mild':
        return const Color(0xFFFFC107);
      case 'healthy':
      case 'none':
        return const Color(0xFF4CAF50);
      default:
        return const Color(0xFF9E9E9E);
    }
  }
}