import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/disease_result.dart';
import '../models/scan_history.dart';

class ApiService {
  static const String baseUrl = 'https://cropguard-oji3662ur-sibby-killers-projects.vercel.app/api';
  static const Duration timeoutDuration = Duration(seconds: 30);

  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/health'),
            headers: {'Content-Type': 'application/json'},
          )
          .timeout(timeoutDuration);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Health check failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: ${e.toString()}');
    }
  }

  Future<DiseaseResult> detectDisease({
    required String imageBase64,
    required String cropType,
    String? userId,
  }) async {
    try {
      final requestBody = {
        'image': imageBase64,
        'crop_type': cropType.toLowerCase(),
        if (userId != null) 'user_id': userId,
      };

      final response = await http
          .post(
            Uri.parse('$baseUrl/detect'),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            body: json.encode(requestBody),
          )
          .timeout(timeoutDuration);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['success'] == true) {
          return DiseaseResult.fromJson(data);
        } else {
          throw Exception(data['error'] ?? 'Detection failed');
        }
      } else {
        final errorData = json.decode(response.body);
        throw Exception(errorData['error'] ?? 'Server error: ${response.statusCode}');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection failed. Please try again.');
    } catch (e) {
      if (e.toString().contains('TimeoutException')) {
        throw Exception('Request timed out. Please try again.');
      }
      rethrow;
    }
  }

  Future<List<ScanHistory>> getScanHistory({
    required String userId,
    int limit = 50,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/history').replace(queryParameters: {
        'user_id': userId,
        'limit': limit.toString(),
      });

      final response = await http
          .get(
            uri,
            headers: {'Content-Type': 'application/json'},
          )
          .timeout(timeoutDuration);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['success'] == true) {
          final scans = (data['scans'] as List)
              .map((scan) => ScanHistory.fromJson(scan))
              .toList();
          return scans;
        } else {
          throw Exception(data['error'] ?? 'Failed to fetch history');
        }
      } else {
        throw Exception('Server error: ${response.statusCode}');
      }
    } on SocketException {
      throw Exception('No internet connection');
    } catch (e) {
      rethrow;
    }
  }

  Future<Map<String, dynamic>> getDiseaseInfo(String diseaseName) async {
    try {
      final uri = Uri.parse('$baseUrl/diseases').replace(queryParameters: {
        'name': diseaseName,
      });

      final response = await http
          .get(
            uri,
            headers: {'Content-Type': 'application/json'},
          )
          .timeout(timeoutDuration);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to get disease info');
      }
    } catch (e) {
      throw Exception('Error fetching disease info: ${e.toString()}');
    }
  }

  Future<List<Map<String, dynamic>>> searchDiseases(String query) async {
    try {
      final uri = Uri.parse('$baseUrl/diseases').replace(queryParameters: {
        'search': query,
      });

      final response = await http
          .get(
            uri,
            headers: {'Content-Type': 'application/json'},
          )
          .timeout(timeoutDuration);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<Map<String, dynamic>>.from(data['diseases'] ?? []);
      } else {
        throw Exception('Search failed');
      }
    } catch (e) {
      throw Exception('Search error: ${e.toString()}');
    }
  }
}