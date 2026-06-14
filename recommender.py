# Smart Design Recommendation Engine
import requests

def get_weather_data(city):
    """Fetch real-time weather data for a city"""
    try:
        # Using OpenWeatherMap API (free tier)
        api_key = "YOUR_API_KEY"  # Replace with actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['description']
            }
    except:
        pass
    
    # Return default values if API fails
    return {'temperature': 28, 'humidity': 65, 'condition': 'clear'}

def get_climate_zone(city):
    """Determine climate zone based on city"""
    north_cities = ['delhi', 'chandigarh', 'jaipur', 'lucknow', 'amritsar', 'dehradun']
    coastal_cities = ['mumbai', 'chennai', 'kolkata', 'goa', 'cochin', 'vizag']
    hot_cities = ['ahmedabad', 'nagpur', 'jodhpur', 'bikaner', 'surat']
    
    city_lower = city.lower()
    
    if any(nc in city_lower for nc in north_cities):
        return "Extreme"
    elif any(cc in city_lower for cc in coastal_cities):
        return "Humid"
    elif any(hc in city_lower for hc in hot_cities):
        return "Hot & Dry"
    else:
        return "Moderate"

def recommend_design(city, floors, plot_size, family_size):
    """Generate design recommendations"""
    
    weather = get_weather_data(city)
    climate = get_climate_zone(city)
    
    recommendations = {
        'climate_zone': climate,
        'current_temp': weather['temperature'],
        'humidity': weather['humidity'],
        'roof_type': '',
        'wall_material': '',
        'window_placement': '',
        'house_type': '',
        'special_features': []
    }
    
    # Determine house type
    if floors == 1:
        if "Small" in plot_size:
            recommendations['house_type'] = "Compact Bungalow"
        elif "Medium" in plot_size:
            recommendations['house_type'] = "Standard Bungalow"
        else:
            recommendations['house_type'] = "Luxury Villa"
    elif floors == 2:
        recommendations['house_type'] = "Duplex House"
    else:
        recommendations['house_type'] = "Triplex Villa"
    
    # Climate-specific recommendations
    if climate == "Extreme":
        recommendations['roof_type'] = "Insulated RCC with cavity wall + Thermal insulation"
        recommendations['wall_material'] = "9-inch hollow brick with insulation + Double-glazed windows"
        recommendations['window_placement'] = "Minimize west windows; maximize south for winter sun"
        recommendations['special_features'].extend([
            "Add sunshades on south/west windows",
            "Use air cavity walls for thermal break",
            "Consider radiant barrier in roof"
        ])
        
    elif climate == "Humid":
        recommendations['roof_type'] = "Sloped roof with ventilation + Overhangs"
        recommendations['wall_material'] = "AAC blocks with weather-resistant coating"
        recommendations['window_placement'] = "Cross ventilation design; louvered windows"
        recommendations['special_features'].extend([
            "High ceiling for air circulation",
            "Rainwater harvesting system",
            "Mosquito nets on all openings"
        ])
        
    elif climate == "Hot & Dry":
        recommendations['roof_type'] = "Cool roof with reflective coating + Terrace garden"
        recommendations['wall_material'] = "Double-wall construction with air cavity + Light color finish"
        recommendations['window_placement'] = "Small windows on east/west; Deep overhangs"
        recommendations['special_features'].extend([
            "Courtyard design for natural cooling",
            "Bamboo screens or jaalis",
            "Underground water tank for cooling"
        ])
        
    else:  # Moderate
        recommendations['roof_type'] = "Flat RCC with terrace + Green roof option"
        recommendations['wall_material'] = "9-inch brick masonry + Moderate insulation"
        recommendations['window_placement'] = "Balanced distribution on all sides"
        recommendations['special_features'].extend([
            "Open terrace for outdoor living",
            "Solar panel ready structure",
            "Rainwater harvesting"
        ])
    
    # Family size adjustments
    if family_size == "7+ persons":
        recommendations['special_features'].append("Minimum 4 bedrooms with attached bathrooms")
    elif family_size == "5-6 persons":
        recommendations['special_features'].append("3-4 bedrooms with common areas spacious")
    
    return recommendations

def calculate_efficiency_score(params):
    """Calculate energy efficiency score based on building parameters"""
    score = 70  # Base score
    
    # Compactness impact
    if params.get('compactness', 0.75) > 0.80:
        score += 10
    elif params.get('compactness', 0.75) < 0.70:
        score -= 10
    
    # Glazing impact
    glazing = params.get('glazing', 0.20)
    if glazing < 0.20:
        score += 5
    elif glazing > 0.30:
        score -= 15
    
    # Orientation impact
    orientation = params.get('orientation', 'North')
    if orientation in ['North', 'East']:
        score += 5
    else:
        score -= 10
    
    return max(0, min(100, score))