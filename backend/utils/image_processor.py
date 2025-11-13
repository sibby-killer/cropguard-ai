"""
Image Processing Utilities
Handles image preprocessing for disease detection
"""

from PIL import Image
import io
import base64
import cv2
import numpy as np

def decode_base64_image(base64_string):
    """
    Decode base64 image string to PIL Image
    Supports JPEG, PNG, and other common formats
    
    Args:
        base64_string: Base64 encoded image string
        
    Returns:
        PIL Image object
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Ensure we can handle all common formats
        # Convert to RGB if needed (handles JPEG, PNG, etc.)
        if image.mode in ['RGBA', 'LA', 'P']:
            # Create a white background for transparent images
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ['RGBA', 'LA'] else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    
    except Exception as e:
        raise ValueError(f"Failed to decode image: {str(e)}")

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess image for ML model
    
    Args:
        image: PIL Image object
        target_size: Target size tuple (width, height)
        
    Returns:
        Preprocessed PIL Image
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size, Image.LANCZOS)
        
        # Optional: Enhance image quality
        # You can add contrast, brightness adjustments here
        
        return image
    
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {str(e)}")

def enhance_image(image):
    """
    Enhance image quality using OpenCV
    
    Args:
        image: PIL Image object
        
    Returns:
        Enhanced PIL Image
    """
    try:
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Denoise
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        # Convert back to PIL
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        enhanced_image = Image.fromarray(enhanced_rgb)
        
        return enhanced_image
    
    except Exception as e:
        print(f"Enhancement failed, returning original: {str(e)}")
        return image

def validate_image(image):
    """
    Validate if image is suitable for processing
    
    Args:
        image: PIL Image object
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check if image exists
        if image is None:
            return False, "Image is None"
        
        # Check image size
        width, height = image.size
        if width < 100 or height < 100:
            return False, "Image too small (minimum 100x100 pixels)"
        
        if width > 5000 or height > 5000:
            return False, "Image too large (maximum 5000x5000 pixels)"
        
        # Check image mode
        if image.mode not in ['RGB', 'RGBA', 'L']:
            return False, f"Unsupported image mode: {image.mode}"
        
        return True, "Image is valid"
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def image_to_base64(image, format='JPEG'):
    """
    Convert PIL Image to base64 string
    
    Args:
        image: PIL Image object
        format: Image format (JPEG, PNG, etc.)
        
    Returns:
        Base64 encoded string
    """
    try:
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/{format.lower()};base64,{img_str}"
    
    except Exception as e:
        raise ValueError(f"Failed to encode image: {str(e)}")