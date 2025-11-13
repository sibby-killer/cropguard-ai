class DiseaseResult {
  final String scanId;
  final String disease;
  final double confidence;
  final String severity;
  final String description;
  final List<String> symptoms;
  final List<String> treatment;
  final List<String> prevention;
  final List<String> organicTreatment;
  final String costEstimate;
  final String scientificName;
  final String imageUrl;
  final DateTime timestamp;
  final String? cropType;

  DiseaseResult({
    required this.scanId,
    required this.disease,
    required this.confidence,
    required this.severity,
    required this.description,
    required this.symptoms,
    required this.treatment,
    required this.prevention,
    required this.organicTreatment,
    required this.costEstimate,
    required this.scientificName,
    required this.imageUrl,
    required this.timestamp,
    this.cropType,
  });

  factory DiseaseResult.fromJson(Map<String, dynamic> json) {
    return DiseaseResult(
      scanId: json['scan_id'] ?? '',
      disease: json['disease'] ?? 'Unknown',
      confidence: (json['confidence'] ?? 0).toDouble(),
      severity: json['severity'] ?? 'Unknown',
      description: json['description'] ?? '',
      symptoms: List<String>.from(json['symptoms'] ?? []),
      treatment: List<String>.from(json['treatment'] ?? []),
      prevention: List<String>.from(json['prevention'] ?? []),
      organicTreatment: List<String>.from(json['organic_treatment'] ?? []),
      costEstimate: json['cost_estimate'] ?? '',
      scientificName: json['scientific_name'] ?? '',
      imageUrl: json['image_url'] ?? '',
      timestamp: json['timestamp'] != null 
          ? DateTime.parse(json['timestamp'])
          : DateTime.now(),
      cropType: json['crop_type'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'scan_id': scanId,
      'disease': disease,
      'confidence': confidence,
      'severity': severity,
      'description': description,
      'symptoms': symptoms,
      'treatment': treatment,
      'prevention': prevention,
      'organic_treatment': organicTreatment,
      'cost_estimate': costEstimate,
      'scientific_name': scientificName,
      'image_url': imageUrl,
      'timestamp': timestamp.toIso8601String(),
      'crop_type': cropType,
    };
  }

  // Helper method to get confidence as percentage
  String get confidencePercentage => '${(confidence * 100).toStringAsFixed(1)}%';

  // Helper method to get severity color
  String get severityColor {
    switch (severity.toLowerCase()) {
      case 'severe':
        return '#F44336'; // Red
      case 'moderate':
        return '#FF9800'; // Orange
      case 'mild':
        return '#FFC107'; // Yellow
      case 'healthy':
      case 'none':
        return '#4CAF50'; // Green
      default:
        return '#9E9E9E'; // Grey
    }
  }

  // Helper method to check if plant is healthy
  bool get isHealthy => disease.toLowerCase().contains('healthy') || 
                       disease.toLowerCase().contains('no disease') ||
                       severity.toLowerCase() == 'none';

  // Helper method to get severity icon
  String get severityIcon {
    switch (severity.toLowerCase()) {
      case 'severe':
        return '🔴';
      case 'moderate':
        return '🟠';
      case 'mild':
        return '🟡';
      case 'healthy':
      case 'none':
        return '🟢';
      default:
        return '⚪';
    }
  }
}