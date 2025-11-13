import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

class AuthService extends ChangeNotifier {
  final SupabaseClient _supabase = Supabase.instance.client;
  String? _userId;
  bool _isInitialized = false;

  String? get userId => _userId;
  bool get isInitialized => _isInitialized;

  AuthService() {
    _initialize();
  }

  Future<void> _initialize() async {
    try {
      // Try to get existing user ID from SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      _userId = prefs.getString('user_id');

      // If no user ID exists, create anonymous user
      if (_userId == null) {
        await _createAnonymousUser();
      }

      _isInitialized = true;
      notifyListeners();
    } catch (e) {
      debugPrint('Auth initialization error: $e');
      // Fallback to UUID if Supabase auth fails
      await _createFallbackUser();
    }
  }

  Future<void> _createAnonymousUser() async {
    try {
      // Sign in anonymously with Supabase
      final response = await _supabase.auth.signInAnonymously();
      
      if (response.user != null) {
        _userId = response.user!.id;
        
        // Save to SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('user_id', _userId!);
        
        debugPrint('Anonymous user created: $_userId');
      } else {
        throw Exception('Failed to create anonymous user');
      }
    } catch (e) {
      debugPrint('Anonymous sign-in failed: $e');
      await _createFallbackUser();
    }
  }

  Future<void> _createFallbackUser() async {
    // Generate UUID as fallback
    const uuid = Uuid();
    _userId = uuid.v4();
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_id', _userId!);
    
    _isInitialized = true;
    notifyListeners();
    
    debugPrint('Fallback user created: $_userId');
  }

  Future<void> signOut() async {
    try {
      await _supabase.auth.signOut();
      
      // Clear stored user ID
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('user_id');
      
      _userId = null;
      _isInitialized = false;
      
      // Re-initialize with new anonymous user
      await _initialize();
      
      notifyListeners();
    } catch (e) {
      debugPrint('Sign out error: $e');
    }
  }

  // Method to refresh user session
  Future<void> refreshSession() async {
    try {
      await _supabase.auth.refreshSession();
    } catch (e) {
      debugPrint('Session refresh failed: $e');
    }
  }
}