"""
Disease Information Database
Contains detailed info about plant diseases
"""

DISEASE_DATABASE = {
    "Late Blight": {
        "crop": "Tomato",
        "severity": "Severe",
        "scientific_name": "Phytophthora infestans",
        "description": "A devastating fungal-like disease that causes dark, water-soaked spots on leaves and fruit. Can destroy entire crops within days in favorable conditions.",
        "symptoms": [
            "Dark brown to black spots on leaves",
            "White mold growth on leaf undersides",
            "Brown lesions on stems",
            "Greasy-looking spots on fruits"
        ],
        "treatment": [
            "Remove and destroy all infected plant material immediately",
            "Apply copper-based fungicides every 7-10 days",
            "Apply chlorothalonil or mancozeb fungicides",
            "Improve air circulation by pruning",
            "Avoid overhead watering - water at soil level only"
        ],
        "prevention": [
            "Plant resistant varieties (e.g., 'Mountain Magic', 'Defiant')",
            "Space plants 2-3 feet apart for air circulation",
            "Apply mulch to prevent soil splash",
            "Remove lower leaves touching the ground",
            "Monitor weather - disease spreads in cool, wet conditions"
        ],
        "organic_treatment": [
            "Copper sulfate spray",
            "Neem oil application",
            "Baking soda solution (1 tbsp per gallon water)",
            "Milk spray (1 part milk to 9 parts water)"
        ],
        "cost_estimate": "$20-50 for treatment per acre"
    },
    
    "Early Blight": {
        "crop": "Tomato",
        "severity": "Moderate",
        "scientific_name": "Alternaria solani",
        "description": "A common fungal disease causing dark spots with concentric rings (target-like pattern) on older leaves.",
        "symptoms": [
            "Brown spots with concentric rings on older leaves",
            "Yellow halo around spots",
            "Premature leaf drop",
            "Dark spots on stems and fruit"
        ],
        "treatment": [
            "Remove affected lower leaves",
            "Apply fungicide containing chlorothalonil or copper",
            "Apply organic fungicides like Bacillus subtilis",
            "Mulch around plants to prevent soil splash",
            "Ensure proper spacing for air flow"
        ],
        "prevention": [
            "Practice 3-4 year crop rotation",
            "Remove all plant debris at end of season",
            "Water in the morning at soil level",
            "Use drip irrigation instead of sprinklers",
            "Apply preventive fungicide sprays"
        ],
        "organic_treatment": [
            "Copper fungicide",
            "Compost tea spray",
            "Garlic spray solution",
            "Bordeaux mixture"
        ],
        "cost_estimate": "$15-30 for treatment per acre"
    },
    
    "Healthy Plant": {
        "crop": "Multiple",
        "severity": "None",
        "scientific_name": "N/A",
        "description": "Your plant appears healthy with no visible signs of disease! Keep up the good work.",
        "symptoms": [
            "Green, vibrant leaves",
            "No spots or discoloration",
            "Strong stem growth",
            "Normal leaf size and shape"
        ],
        "treatment": [
            "Continue regular watering schedule",
            "Maintain fertilization routine",
            "Monitor plants regularly for any changes"
        ],
        "prevention": [
            "Water consistently - 1-2 inches per week",
            "Fertilize every 2-3 weeks during growing season",
            "Inspect plants weekly for early disease detection",
            "Remove weeds that compete for nutrients",
            "Ensure good air circulation"
        ],
        "organic_treatment": [
            "Compost application for nutrients",
            "Mulching to retain moisture"
        ],
        "cost_estimate": "$0 - Just regular maintenance"
    },
    
    "Septoria Leaf Spot": {
        "crop": "Tomato",
        "severity": "Moderate",
        "scientific_name": "Septoria lycopersici",
        "description": "Fungal disease causing small circular spots with dark borders and gray centers on leaves.",
        "symptoms": [
            "Small circular spots (1/8 inch) on leaves",
            "Gray center with dark brown border",
            "Tiny black dots (fungal structures) in spot centers",
            "Yellowing and dropping of lower leaves"
        ],
        "treatment": [
            "Remove infected leaves below the first fruit cluster",
            "Apply fungicide with chlorothalonil or copper",
            "Improve air circulation through pruning",
            "Avoid wetting foliage when watering"
        ],
        "prevention": [
            "Mulch around plants heavily",
            "Remove all crop debris at season end",
            "Rotate crops - don't plant tomatoes in same spot for 3 years",
            "Use drip irrigation",
            "Space plants properly (18-24 inches)"
        ],
        "organic_treatment": [
            "Copper-based fungicides",
            "Sulfur sprays",
            "Baking soda mixture"
        ],
        "cost_estimate": "$20-40 for treatment per acre"
    },
    
    "Bacterial Spot": {
        "crop": "Tomato/Pepper",
        "severity": "Moderate to Severe",
        "scientific_name": "Xanthomonas spp.",
        "description": "Bacterial disease causing small, dark spots on leaves, stems, and fruit.",
        "symptoms": [
            "Small dark spots on leaves (greasy appearance)",
            "Yellow halo around spots",
            "Raised brown spots on fruit",
            "Leaf drop in severe cases"
        ],
        "treatment": [
            "Apply copper-based bactericides",
            "Remove severely infected plants",
            "Avoid overhead watering",
            "Disinfect tools between plants",
            "Apply streptomycin (if available)"
        ],
        "prevention": [
            "Use disease-free seeds and transplants",
            "Rotate crops for 2-3 years",
            "Avoid working with wet plants",
            "Space plants for air circulation",
            "Use resistant varieties when possible"
        ],
        "organic_treatment": [
            "Copper sulfate sprays",
            "Plant-based bactericides",
            "Remove and destroy infected tissue"
        ],
        "cost_estimate": "$25-45 for treatment per acre"
    },
    
    "Leaf Mold": {
        "crop": "Tomato",
        "severity": "Mild to Moderate",
        "scientific_name": "Passalora fulva",
        "description": "Fungal disease common in greenhouse tomatoes, causing yellow spots on upper leaf surfaces.",
        "symptoms": [
            "Pale green to yellow spots on upper leaf surface",
            "Olive-green to brown mold on lower leaf surface",
            "Curling and drying of leaves",
            "Rarely affects fruit directly"
        ],
        "treatment": [
            "Improve ventilation in greenhouse",
            "Reduce humidity below 85%",
            "Apply fungicides containing chlorothalonil",
            "Remove infected leaves",
            "Increase spacing between plants"
        ],
        "prevention": [
            "Maintain humidity below 85%",
            "Provide adequate ventilation",
            "Use resistant varieties",
            "Avoid overhead irrigation",
            "Space plants properly"
        ],
        "organic_treatment": [
            "Sulfur-based fungicides",
            "Improve air flow naturally",
            "Copper sprays"
        ],
        "cost_estimate": "$15-30 for treatment per greenhouse"
    },
    
    "Yellow Leaf Curl Virus": {
        "crop": "Tomato",
        "severity": "Severe",
        "scientific_name": "Begomovirus",
        "description": "Viral disease transmitted by whiteflies, causing severe yield loss.",
        "symptoms": [
            "Upward curling of leaf margins",
            "Yellowing of leaf edges",
            "Stunted plant growth",
            "Reduced fruit size and yield",
            "Flowers fall off"
        ],
        "treatment": [
            "No cure - remove infected plants immediately",
            "Control whitefly populations with insecticides",
            "Use yellow sticky traps",
            "Apply neem oil to deter whiteflies",
            "Isolate affected area"
        ],
        "prevention": [
            "Plant resistant varieties (e.g., 'Tyking', 'Shanty')",
            "Use reflective mulches to repel whiteflies",
            "Install fine mesh screens in greenhouses",
            "Control weeds that host whiteflies",
            "Start with certified disease-free plants"
        ],
        "organic_treatment": [
            "Neem oil for whitefly control",
            "Insecticidal soap",
            "Remove infected plants immediately"
        ],
        "cost_estimate": "$30-60 for prevention per acre"
    },
    
    "Target Spot": {
        "crop": "Tomato",
        "severity": "Moderate",
        "scientific_name": "Corynespora cassiicola",
        "description": "Fungal disease causing circular spots with concentric rings on leaves and fruit.",
        "symptoms": [
            "Brown spots with concentric rings",
            "Spots on leaves, stems, and fruit",
            "Premature leaf drop",
            "Reduced yield"
        ],
        "treatment": [
            "Apply fungicides with azoxystrobin or chlorothalonil",
            "Remove infected plant parts",
            "Improve air circulation",
            "Reduce leaf wetness"
        ],
        "prevention": [
            "Rotate crops every 3 years",
            "Use drip irrigation",
            "Mulch to prevent soil splash",
            "Space plants adequately",
            "Remove crop debris"
        ],
        "organic_treatment": [
            "Copper-based fungicides",
            "Sulfur sprays",
            "Compost tea applications"
        ],
        "cost_estimate": "$20-35 for treatment per acre"
    },
    
    "Mosaic Virus": {
        "crop": "Tomato/Pepper",
        "severity": "Severe",
        "scientific_name": "Tobamovirus",
        "description": "Viral disease causing mottled, discolored leaves and reduced yield.",
        "symptoms": [
            "Mottled light and dark green patterns on leaves",
            "Distorted, stunted growth",
            "Narrow, twisted leaves",
            "Reduced fruit production",
            "Fruit may show yellow blotches"
        ],
        "treatment": [
            "No cure - remove and destroy infected plants",
            "Disinfect tools with 10% bleach solution",
            "Wash hands after handling infected plants",
            "Control aphids that spread the virus",
            "Destroy infected plants (don't compost)"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Plant resistant varieties",
            "Control aphid populations",
            "Avoid smoking near plants (tobacco carries virus)",
            "Wash hands before working with plants"
        ],
        "organic_treatment": [
            "Remove infected plants immediately",
            "Control aphids with neem oil",
            "Use insecticidal soap for aphids"
        ],
        "cost_estimate": "$0 for removal, $20-40 for prevention per acre"
    },
    
    "Powdery Mildew": {
        "crop": "Multiple",
        "severity": "Mild to Moderate",
        "scientific_name": "Various species",
        "description": "Fungal disease appearing as white powdery coating on leaves.",
        "symptoms": [
            "White powdery coating on leaves",
            "Leaves may yellow and drop",
            "Stunted growth",
            "Reduced yield"
        ],
        "treatment": [
            "Apply sulfur or potassium bicarbonate sprays",
            "Remove heavily infected leaves",
            "Improve air circulation",
            "Apply fungicides if severe"
        ],
        "prevention": [
            "Ensure good air circulation",
            "Avoid overhead watering",
            "Plant in full sun",
            "Use resistant varieties",
            "Apply preventive sulfur sprays"
        ],
        "organic_treatment": [
            "Milk spray (1:9 milk to water ratio)",
            "Baking soda solution",
            "Neem oil",
            "Sulfur fungicides"
        ],
        "cost_estimate": "$10-25 for treatment per acre"
    }
}

def get_disease_info(disease_name):
    """Get disease information from database"""
    # Try exact match first
    if disease_name in DISEASE_DATABASE:
        return DISEASE_DATABASE[disease_name]
    
    # Try case-insensitive match
    for key in DISEASE_DATABASE:
        if key.lower() == disease_name.lower():
            return DISEASE_DATABASE[key]
    
    # Try partial match
    for key in DISEASE_DATABASE:
        if disease_name.lower() in key.lower() or key.lower() in disease_name.lower():
            return DISEASE_DATABASE[key]
    
    # Return generic info if not found
    return {
        "crop": "Unknown",
        "severity": "Unknown",
        "scientific_name": "Unknown",
        "description": f"Information about {disease_name} is not available in our database. Please consult with a local agricultural expert.",
        "symptoms": ["Information not available"],
        "treatment": ["Consult with agricultural extension officer or plant pathologist"],
        "prevention": ["Regular monitoring and good agricultural practices"],
        "organic_treatment": ["Consult with organic farming specialist"],
        "cost_estimate": "Unknown"
    }

def search_diseases(query):
    """Search for diseases by keyword"""
    results = []
    query_lower = query.lower()
    
    for disease_name, info in DISEASE_DATABASE.items():
        if (query_lower in disease_name.lower() or
            query_lower in info.get('crop', '').lower() or
            query_lower in info.get('description', '').lower()):
            results.append({
                'name': disease_name,
                **info
            })
    
    return results