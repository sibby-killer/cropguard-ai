import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../models/scan_history.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<ScanHistory> _scans = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    try {
      setState(() {
        _isLoading = true;
        _error = null;
      });

      final authService = context.read<AuthService>();
      final userId = authService.userId;

      if (userId == null) {
        throw Exception('User not authenticated');
      }

      final apiService = context.read<ApiService>();
      final scans = await apiService.getScanHistory(userId: userId);

      setState(() {
        _scans = scans;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan History'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadHistory,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadHistory,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: SpinKitThreeBounce(
          color: Color(0xFF4CAF50),
          size: 40,
        ),
      );
    }

    if (_error != null) {
      return _buildErrorState();
    }

    if (_scans.isEmpty) {
      return _buildEmptyState();
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _scans.length,
      itemBuilder: (context, index) {
        final scan = _scans[index];
        return _buildHistoryCard(scan);
      },
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 80,
              color: Colors.grey[400],
            ),
            const SizedBox(height: 16),
            Text(
              'Failed to load history',
              style: GoogleFonts.poppins(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              _error ?? 'Unknown error occurred',
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: Colors.grey[500],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _loadHistory,
              icon: const Icon(Icons.refresh),
              label: const Text('Try Again'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.history,
              size: 120,
              color: Colors.grey[300],
            ),
            const SizedBox(height: 24),
            Text(
              'No scans yet',
              style: GoogleFonts.poppins(
                fontSize: 24,
                fontWeight: FontWeight.w600,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 12),
            Text(
              'Start by scanning your first crop to detect diseases',
              style: GoogleFonts.poppins(
                fontSize: 16,
                color: Colors.grey[500],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: const Icon(Icons.camera_alt),
              label: const Text('Take Your First Scan'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHistoryCard(ScanHistory scan) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _showScanDetails(scan),
        borderRadius: BorderRadius.circular(15),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Image Thumbnail
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: SizedBox(
                  width: 80,
                  height: 80,
                  child: scan.imageUrl.isNotEmpty
                      ? CachedNetworkImage(
                          imageUrl: scan.imageUrl,
                          fit: BoxFit.cover,
                          placeholder: (context, url) => Container(
                            color: Colors.grey[200],
                            child: const Center(
                              child: SpinKitCircle(
                                color: Color(0xFF4CAF50),
                                size: 30,
                              ),
                            ),
                          ),
                          errorWidget: (context, url, error) => Container(
                            color: Colors.grey[200],
                            child: Icon(
                              Icons.image_not_supported,
                              color: Colors.grey[400],
                            ),
                          ),
                        )
                      : Container(
                          color: Colors.grey[200],
                          child: Icon(
                            Icons.image,
                            color: Colors.grey[400],
                          ),
                        ),
                ),
              ),
              
              const SizedBox(width: 16),
              
              // Content
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Disease Name
                    Text(
                      scan.diseaseDetected,
                      style: GoogleFonts.poppins(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFF2E7D32),
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    
                    const SizedBox(height: 4),
                    
                    // Crop Type
                    if (scan.cropType != null)
                      Text(
                        'Crop: ${scan.cropType}',
                        style: GoogleFonts.poppins(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                    
                    const SizedBox(height: 8),
                    
                    // Confidence Bar
                    Row(
                      children: [
                        Expanded(
                          child: LinearProgressIndicator(
                            value: scan.confidence,
                            backgroundColor: Colors.grey[300],
                            valueColor: AlwaysStoppedAnimation<Color>(
                              _getConfidenceColor(scan.confidence),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          scan.confidencePercentage,
                          style: GoogleFonts.poppins(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: _getConfidenceColor(scan.confidence),
                          ),
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 8),
                    
                    // Severity and Date
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        // Severity Badge
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          decoration: BoxDecoration(
                            color: _getSeverityColor(scan.severity),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                scan.severityIcon,
                                style: const TextStyle(fontSize: 10),
                              ),
                              const SizedBox(width: 4),
                              Text(
                                scan.severity ?? 'Unknown',
                                style: GoogleFonts.poppins(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.white,
                                ),
                              ),
                            ],
                          ),
                        ),
                        
                        // Date
                        Text(
                          scan.formattedDate,
                          style: GoogleFonts.poppins(
                            fontSize: 12,
                            color: Colors.grey[500],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              
              // Arrow
              Icon(
                Icons.chevron_right,
                color: Colors.grey[400],
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showScanDetails(ScanHistory scan) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        maxChildSize: 0.95,
        minChildSize: 0.5,
        expand: false,
        builder: (context, scrollController) {
          return Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Handle
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                
                const SizedBox(height: 20),
                
                Expanded(
                  child: SingleChildScrollView(
                    controller: scrollController,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Image
                        if (scan.imageUrl.isNotEmpty)
                          ClipRRect(
                            borderRadius: BorderRadius.circular(15),
                            child: AspectRatio(
                              aspectRatio: 16 / 9,
                              child: CachedNetworkImage(
                                imageUrl: scan.imageUrl,
                                fit: BoxFit.cover,
                                placeholder: (context, url) => Container(
                                  color: Colors.grey[200],
                                  child: const Center(
                                    child: SpinKitCircle(
                                      color: Color(0xFF4CAF50),
                                      size: 40,
                                    ),
                                  ),
                                ),
                                errorWidget: (context, url, error) => Container(
                                  color: Colors.grey[200],
                                  child: const Center(
                                    child: Icon(Icons.image_not_supported),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        
                        const SizedBox(height: 20),
                        
                        // Disease Name
                        Text(
                          scan.diseaseDetected,
                          style: GoogleFonts.poppins(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: const Color(0xFF2E7D32),
                          ),
                        ),
                        
                        const SizedBox(height: 16),
                        
                        // Details Grid
                        _buildDetailRow('Crop Type', scan.cropType ?? 'Unknown'),
                        _buildDetailRow('Confidence', scan.confidencePercentage),
                        _buildDetailRow('Severity', scan.severity ?? 'Unknown'),
                        _buildDetailRow('Scan Date', scan.formattedDate),
                        
                        if (scan.recommendations != null && scan.recommendations!.isNotEmpty) ...[
                          const SizedBox(height: 20),
                          Text(
                            'Recommendations',
                            style: GoogleFonts.poppins(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            scan.recommendations!,
                            style: GoogleFonts.poppins(
                              fontSize: 14,
                              color: Colors.grey[700],
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              '$label:',
              style: GoogleFonts.poppins(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: Colors.grey[600],
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: Colors.grey[800],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Color _getConfidenceColor(double confidence) {
    if (confidence >= 0.8) return Colors.green;
    if (confidence >= 0.6) return Colors.orange;
    return Colors.red;
  }

  Color _getSeverityColor(String? severity) {
    switch (severity?.toLowerCase()) {
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