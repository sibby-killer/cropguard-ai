class ScanHistory {
  final String id;
  final String userId;
  final String imageUrl;
  final String? cropType;
  final String diseaseDetected;
  final double confidence;
  final String? severity;
  final String? recommendations;
  final DateTime createdAt;

  ScanHistory({
    required this.id,
    required this.userId,
    required this.imageUrl,
    this.cropType,
    required this.diseaseDetected,
    required this.confidence,
    this.severity,
    this.recommendations,
    required this.createdAt,
  });

  factory ScanHistory.fromJson(Map<String, dynamic> json) {
    return ScanHistory(
      id: json['id'] ?? '',
      userId: json['user_id'] ?? '',
      imageUrl: json['image_url'] ?? '',
      cropType: json['crop_type'],
      diseaseDetected: json['disease_detected'] ?? '',
      confidence: (json['confidence'] ?? 0).toDouble(),
      severity: json['severity'],
      recommendations: json['recommendations'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'image_url': imageUrl,
      'crop_type': cropType,
      'disease_detected': diseaseDetected,
      'confidence': confidence,
      'severity': severity,
      'recommendations': recommendations,
      'created_at': createdAt.toIso8601String(),
    };
  }

  // Helper methods
  String get confidencePercentage => '${(confidence * 100).toStringAsFixed(1)}%';

  String get formattedDate {
    final now = DateTime.now();
    final difference = now.difference(createdAt);

    if (difference.inDays > 0) {
      return '${difference.inDays} day${difference.inDays > 1 ? 's' : ''} ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hour${difference.inHours > 1 ? 's' : ''} ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minute${difference.inMinutes > 1 ? 's' : ''} ago';
    } else {
      return 'Just now';
    }
  }

  String get severityColor {
    switch (severity?.toLowerCase()) {
      case 'severe':
        return '#F44336';
      case 'moderate':
        return '#FF9800';
      case 'mild':
        return '#FFC107';
      case 'healthy':
      case 'none':
        return '#4CAF50';
      default:
        return '#9E9E9E';
    }
  }

  String get severityIcon {
    switch (severity?.toLowerCase()) {
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

  bool get isHealthy => diseaseDetected.toLowerCase().contains('healthy') ||
                       diseaseDetected.toLowerCase().contains('no disease') ||
                       severity?.toLowerCase() == 'none';
}