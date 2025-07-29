import requests
import json
import os
import time
from typing import Dict, List, Optional
from prompts import TripPrompts

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

class TripPlanner:
    def __init__(self):
        # Get Hugging Face API token from environment
        self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGING_FACE_TOKEN environment variable is required. Please set it in your environment or .env file.")
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Alternative free models to try
        self.models = [
            "facebook/blenderbot-400M-distill",
            "microsoft/DialoGPT-medium",
            "gpt2",
            "EleutherAI/gpt-neo-125M"
        ]
        
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        self.prompts = TripPrompts()
    

    
    def query_huggingface_api(self, prompt: str, model: Optional[str] = None) -> str:
        """Query Hugging Face API with fallback models"""
        models_to_try = [model] if model is not None else self.models
        
        for model_name in models_to_try:
            if not model_name:
                continue
                
            api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "do_sample": True,
                    "top_p": 0.9
                }
            }
            
            try:
                response = requests.post(
                    api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            return result[0]["generated_text"]
                        elif "text" in result[0]:
                            return result[0]["text"]
                    elif isinstance(result, dict):
                        if "generated_text" in result:
                            return result["generated_text"]
                        elif "text" in result:
                            return result["text"]
                    
                    return str(result)
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    time.sleep(2)
                    continue
                
            except requests.exceptions.RequestException as e:
                print(f"Error with model {model_name}: {e}")
                continue
        
        # If all models fail, return a fallback response
        return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a basic response when API is unavailable"""
        if "adventurous" in prompt.lower():
            return """I'd recommend an adventurous trip to Ladakh! Here's why:

            Ladakh offers incredible adventure activities like motorcycle tours, river rafting, and high-altitude trekking through stunning Himalayan landscapes. The region has diverse terrains from barren mountains to pristine lakes, perfect for thrill-seekers.

            Activities could include:
            - Leh-Ladakh bike expedition
            - Pangong Tso and Tso Moriri lake visits
            - River rafting in Zanskar River
            - Trekking in Markha Valley
            - Magnetic Hill and Khardung La Pass

            This destination perfectly matches your adventurous spirit with its world-class high-altitude activities and breathtaking Himalayan beauty."""
        
        elif "peaceful" in prompt.lower():
            return """For a peaceful retreat, I suggest Manali and Shimla. Here's my reasoning:

            These hill stations offer serene mountain environments, cool weather, and breathtaking views perfect for relaxation and rejuvenation. The peaceful atmosphere of the Himalayas provides an ideal escape from city life.

            Peaceful activities include:
            - Morning walks in apple orchards and pine forests
            - Scenic viewpoints with mountain panoramas
            - Quiet cafes with mountain views
            - Nature photography and bird watching
            - Peaceful temple visits (Hidimba Devi, Jakhu Temple)
            - Leisurely strolls through hill station markets

            These destinations will refresh your mind with their tranquil mountain atmosphere and natural beauty."""
        
        else:  # fun
            return """For a fun-filled trip, I recommend Goa! Here's why:

            Goa offers an incredible mix of vibrant nightlife, beautiful beaches, delicious food, and relaxed culture. It's perfect for those seeking entertainment and social experiences.

            Fun activities include:
            - Beach parties and water sports in North Goa
            - Exploring spice plantations and local markets
            - Portuguese heritage tours in Old Goa
            - Sunset cruises and casino experiences
            - Local Goan cuisine and feni tasting
            - Flea markets and beach shacks

            Goa guarantees non-stop fun with its lively atmosphere and endless entertainment options."""
    
    def parse_ai_response(self, response: str, mood: str, budget: str, duration: int, user_city: str, destination_city: str, transport_mode: str) -> Dict:
        """Parse AI response into structured itinerary format"""
        
        # Clean the response - remove the original prompt if it's included
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("Plan a") and not line.startswith("Create"):
                cleaned_lines.append(line)
        
        cleaned_response = '\n'.join(cleaned_lines)
        
        # Extract destination (look for country/city names)
        destination = "Recommended Destination"
        destination_description = ""
        
        # Look for common destination patterns
        import re
        dest_patterns = [
            r"(?:visit|go to|travel to|explore|recommend)\s+([A-Z][a-zA-Z\s,]+?)(?:\.|!|\n|$)",
            r"([A-Z][a-zA-Z\s]+(?:land|sia|stan|ina|ary|rope|rica|tralia))",
            r"([A-Z][a-zA-Z\s]+(?:Island|City|Beach|Mountain)s?)"
        ]
        
        for pattern in dest_patterns:
            match = re.search(pattern, cleaned_response, re.IGNORECASE)
            if match:
                destination = match.group(1).strip()
                break
        
        # Calculate transport costs
        transport_costs = self._calculate_transport_cost(user_city, destination_city, transport_mode)
        
        # Generate daily plan with location-specific activities
        daily_plan = []
        location_activities = self._get_location_specific_activities(destination_city, mood, duration)
        
        for i in range(duration):
            day_num = i + 1
            if i < len(location_activities):
                day_activity = location_activities[i]
            else:
                # Fallback for longer trips
                day_activity = location_activities[i % len(location_activities)]
            
            daily_plan.append({
                "day": f"Day {day_num}",
                "theme": day_activity["theme"],
                "activities": day_activity["activities"],
                "estimated_cost": self._estimate_daily_cost(budget)
            })
        
        # Generate enhanced reasoning with creative variations
        reasoning = self._enhance_reasoning_text(cleaned_response, destination_city, mood, budget)
        
        # Create budget breakdown with transport costs
        budget_breakdown = self._create_budget_breakdown(budget, duration, transport_costs)
        
        # Generate tips
        tips = self._generate_tips(mood, budget, destination)
        
        return {
            "destination": destination_city,
            "user_city": user_city,
            "transport_mode": transport_mode,
            "destination_description": reasoning,
            "reasoning": f"Based on your {mood} mood and {budget} budget, traveling from {user_city} to {destination_city} via {transport_mode} offers the perfect combination of experiences that match your preferences and financial considerations.",
            "daily_plan": daily_plan,
            "budget_breakdown": budget_breakdown,
            "transport_info": transport_costs,
            "tips": tips
        }
    
    def _estimate_daily_cost(self, budget: str) -> str:
        """Estimate daily costs based on budget level"""
        if budget == "budget":
            return "₹1,500-2,500 per day"
        elif budget == "mid-range":
            return "₹4,000-8,000 per day"
        else:  # luxury
            return "₹12,000-20,000 per day"
    
    def _create_budget_breakdown(self, budget: str, duration: int, transport_costs: Dict[str, int]) -> Dict[str, str]:
        """Create a budget breakdown"""
        if budget == "budget":
            accommodation_cost = 800 * duration
            food_cost = 600 * duration
            activities_cost = 400 * duration
            local_transport_cost = 200 * duration
            transport_cost = transport_costs["round_trip_cost"]
            
            total_min = accommodation_cost + food_cost + activities_cost + local_transport_cost + transport_cost
            total_max = int(accommodation_cost * 1.5 + food_cost * 1.5 + activities_cost * 1.5 + local_transport_cost * 1.5 + transport_cost)
            
            return {
                "accommodation": f"₹{accommodation_cost}-{int(accommodation_cost * 1.5)} ({duration} nights)",
                "food": f"₹{food_cost}-{int(food_cost * 1.5)} (meals)",
                "activities": f"₹{activities_cost}-{int(activities_cost * 1.5)} (attractions)",
                "transportation": f"₹{transport_cost} (round trip via {transport_costs.get('mode', 'selected mode')})",
                "local_transport": f"₹{local_transport_cost}-{int(local_transport_cost * 1.5)} (local travel)",
                "total_estimated": f"₹{total_min}-{total_max}"
            }
        elif budget == "mid-range":
            accommodation_cost = 2500 * duration
            food_cost = 1200 * duration
            activities_cost = 1000 * duration
            local_transport_cost = 500 * duration
            transport_cost = transport_costs["round_trip_cost"]
            
            total_min = accommodation_cost + food_cost + activities_cost + local_transport_cost + transport_cost
            total_max = int(accommodation_cost * 1.6 + food_cost * 1.6 + activities_cost * 1.8 + local_transport_cost * 1.5 + transport_cost)
            
            return {
                "accommodation": f"₹{accommodation_cost}-{int(accommodation_cost * 1.6)} ({duration} nights)",
                "food": f"₹{food_cost}-{int(food_cost * 1.6)} (meals)",
                "activities": f"₹{activities_cost}-{int(activities_cost * 1.8)} (attractions)",
                "transportation": f"₹{transport_cost} (round trip via {transport_costs.get('mode', 'selected mode')})",
                "local_transport": f"₹{local_transport_cost}-{int(local_transport_cost * 1.5)} (local travel)",
                "total_estimated": f"₹{total_min}-{total_max}"
            }
        else:  # luxury
            accommodation_cost = 6000 * duration
            food_cost = 2500 * duration
            activities_cost = 2000 * duration
            local_transport_cost = 1000 * duration
            transport_cost = transport_costs["round_trip_cost"]
            
            total_min = accommodation_cost + food_cost + activities_cost + local_transport_cost + transport_cost
            total_max = int(accommodation_cost * 2 + food_cost * 1.6 + activities_cost * 2 + local_transport_cost * 1.5 + transport_cost)
            
            return {
                "accommodation": f"₹{accommodation_cost}-{int(accommodation_cost * 2)} ({duration} nights)",
                "food": f"₹{food_cost}-{int(food_cost * 1.6)} (fine dining)",
                "activities": f"₹{activities_cost}-{int(activities_cost * 2)} (premium experiences)",
                "transportation": f"₹{transport_cost} (round trip via {transport_costs.get('mode', 'selected mode')})",
                "local_transport": f"₹{local_transport_cost}-{int(local_transport_cost * 1.5)} (luxury local travel)",
                "total_estimated": f"₹{total_min}-{total_max}"
            }
    
    def _generate_tips(self, mood: str, budget: str, destination: str) -> List[str]:
        """Generate travel tips based on preferences"""
        base_tips = [
            "Book flights and accommodation in advance for better prices",
            "Research local customs and dress codes",
            "Keep digital and physical copies of important documents",
            "Consider travel insurance for peace of mind"
        ]
        
        mood_tips = {
            "adventurous": [
                "Pack appropriate gear for outdoor activities",
                "Check weather conditions and seasonal considerations",
                "Book adventure activities in advance as they fill up quickly"
            ],
            "spiritual": [
                "Research local spiritual practices and etiquette",
                "Pack modest clothing for temple visits",
                "Consider bringing a travel journal for reflection"
            ],
            "fun": [
                "Research local nightlife and entertainment options",
                "Learn basic phrases in the local language",
                "Download translation and navigation apps"
            ]
        }
        
        budget_tips = {
            "budget": ["Look for free walking tours and activities", "Eat at local markets for authentic and affordable food"],
            "mid-range": ["Balance splurge experiences with budget-friendly options", "Consider package deals for activities"],
            "luxury": ["Research high-end experiences unique to the destination", "Book premium restaurants well in advance"]
        }
        
        return base_tips + mood_tips.get(mood, []) + budget_tips.get(budget, [])
    
    def _get_location_specific_activities(self, destination: str, mood: str, duration: int) -> List[Dict[str, str]]:
        """Generate location-specific daily activities based on destination and mood"""
        
        # Define comprehensive destination-specific activity mappings with real tourist spots
        destination_activities = {
            # Adventure destinations
            "ladakh": {
                "adventurous": [
                    {"theme": "High Altitude Acclimatization", "activities": ["Morning: Arrive in Leh, rest and acclimatize", "Afternoon: Visit Leh Palace and Shanti Stupa", "Evening: Explore Leh Market and local cuisine"]},
                    {"theme": "Monastery and Culture Trail", "activities": ["Morning: Visit Hemis Monastery", "Afternoon: Explore Thiksey Monastery", "Evening: Traditional Ladakhi dinner with local family"]},
                    {"theme": "Pangong Lake Adventure", "activities": ["Morning: Early drive to Pangong Tso via Chang La Pass", "Afternoon: Lake activities and photography", "Evening: Overnight camping by the lake"]},
                    {"theme": "Nubra Valley Expedition", "activities": ["Morning: Drive to Nubra Valley via Khardung La", "Afternoon: Camel safari in Hunder sand dunes", "Evening: Stay in traditional camps"]},
                    {"theme": "River Rafting and Trekking", "activities": ["Morning: White water rafting in Zanskar River", "Afternoon: Short trek to Alchi Monastery", "Evening: Sunset at Magnetic Hill"]},
                    {"theme": "Extreme Sports Day", "activities": ["Morning: Mountain biking expedition", "Afternoon: Rock climbing and rappelling", "Evening: Stargazing in clear mountain skies"]},
                    {"theme": "Cultural Immersion", "activities": ["Morning: Visit traditional Ladakhi village", "Afternoon: Learn traditional crafts and farming", "Evening: Folk dance and music performance"]}
                ],
                "spiritual": [
                    {"theme": "Monastery Meditation", "activities": ["Morning: Meditation session at Hemis Monastery", "Afternoon: Prayer wheel spinning and chanting", "Evening: Sunset meditation at Shanti Stupa"]},
                    {"theme": "Sacred Lakes Pilgrimage", "activities": ["Morning: Journey to Pangong Tso for spiritual reflection", "Afternoon: Silent contemplation by the sacred lake", "Evening: Group meditation under stars"]},
                    {"theme": "Buddhist Learning", "activities": ["Morning: Buddhist philosophy sessions with monks", "Afternoon: Mandala making workshop", "Evening: Evening prayers at Thiksey Monastery"]},
                    {"theme": "Inner Peace Retreat", "activities": ["Morning: Sunrise yoga in mountains", "Afternoon: Walking meditation in valleys", "Evening: Spiritual discourse and tea ceremony"]},
                    {"theme": "Sacred Art and Culture", "activities": ["Morning: Study ancient Buddhist murals", "Afternoon: Learn traditional prayer flag making", "Evening: Chanting and spiritual music session"]}
                ],
                "fun": [
                    {"theme": "Cultural Festival Fun", "activities": ["Morning: Local market exploration and shopping", "Afternoon: Traditional Ladakhi games and sports", "Evening: Folk dance and music celebration"]},
                    {"theme": "Adventure Photography", "activities": ["Morning: Scenic photography expedition", "Afternoon: Group adventure activities", "Evening: Photo sharing and local food tasting"]},
                    {"theme": "Local Life Experience", "activities": ["Morning: Village homestay activities", "Afternoon: Traditional cooking classes", "Evening: Bonfire and storytelling session"]},
                    {"theme": "Nature and Wildlife", "activities": ["Morning: Wildlife spotting expedition", "Afternoon: Nature walks and bird watching", "Evening: Local cultural performances"]}
                ]
            },
            
            # Peaceful destinations
            "rishikesh": {
                "peaceful": [
                    {"theme": "Ganga Aarti and Sacred Rituals", "activities": ["Morning: Sunrise yoga by the Ganges", "Afternoon: Visit Neelkanth Mahadev Temple", "Evening: Participate in Ganga Aarti at Triveni Ghat"]},
                    {"theme": "Yoga and Meditation Retreat", "activities": ["Morning: Intensive yoga session at ashram", "Afternoon: Meditation and pranayama practice", "Evening: Spiritual discourse and satsang"]},
                    {"theme": "Ashram Life Experience", "activities": ["Morning: Join ashram morning prayers", "Afternoon: Seva (service) activities", "Evening: Group meditation and chanting"]},
                    {"theme": "Sacred Temples Tour", "activities": ["Morning: Visit Mansa Devi Temple via cable car", "Afternoon: Explore Chandi Devi Temple", "Evening: Evening prayers at local temples"]},
                    {"theme": "Spiritual Learning", "activities": ["Morning: Vedanta and philosophy classes", "Afternoon: Sanskrit learning session", "Evening: Kirtan and devotional singing"]},
                    {"theme": "Inner Cleansing", "activities": ["Morning: Ayurvedic consultation and treatment", "Afternoon: Detox and cleansing rituals", "Evening: Silent meditation by Ganges"]},
                    {"theme": "Sacred Geography", "activities": ["Morning: Trek to Kunjapuri Temple for sunrise", "Afternoon: Visit ancient caves and meditation spots", "Evening: Reflection and journal writing"]}
                ],
                "adventurous": [
                    {"theme": "River Adventure", "activities": ["Morning: White water rafting on Ganges", "Afternoon: Cliff jumping and swimming", "Evening: Riverside camping and bonfire"]},
                    {"theme": "Himalayan Trekking", "activities": ["Morning: Trek to Neer Garh Waterfall", "Afternoon: Continue to higher altitude trails", "Evening: Mountain camping under stars"]},
                    {"theme": "Extreme Sports", "activities": ["Morning: Bungee jumping from 83m height", "Afternoon: Flying fox and giant swing", "Evening: Rock climbing and rappelling"]},
                    {"theme": "Adventure Yoga", "activities": ["Morning: Yoga on suspension bridge", "Afternoon: Adventure sports in mountains", "Evening: Meditation in caves"]}
                ],
                "fun": [
                    {"theme": "Café Culture and Music", "activities": ["Morning: Explore Beatles Ashram", "Afternoon: Café hopping in Laxman Jhula area", "Evening: Live music and cultural performances"]},
                    {"theme": "Market and Shopping", "activities": ["Morning: Shopping for spiritual items and books", "Afternoon: Local market exploration", "Evening: Street food tour and local delicacies"]},
                    {"theme": "Photography and Sightseeing", "activities": ["Morning: Instagram-worthy spots photography", "Afternoon: Scenic bridge walks and river views", "Evening: Sunset photography from Ram Jhula"]}
                ]
            },
            
            # Fun destinations  
            "goa": {
                "fun": [
                    {"theme": "Beach Hopping Extravaganza", "activities": ["Morning: Sunrise at Anjuna Beach with breakfast shacks", "Afternoon: Water sports at Baga Beach (parasailing, jet skiing)", "Evening: Sunset party at Arambol Beach"]},
                    {"theme": "North Goa Nightlife", "activities": ["Morning: Beach volleyball and relaxation at Calangute", "Afternoon: Shopping at Mapusa Market", "Evening: Club hopping - Tito's, Mambo's, and beach parties"]},
                    {"theme": "Portuguese Heritage and Food", "activities": ["Morning: Old Goa churches tour (Basilica of Bom Jesus)", "Afternoon: Portuguese architecture walk in Fontainhas", "Evening: Traditional Goan dinner with feni tasting"]},
                    {"theme": "Adventure Water Sports", "activities": ["Morning: Scuba diving at Grande Island", "Afternoon: Dolphin watching cruise", "Evening: Beach shack dinner with live music"]},
                    {"theme": "Spice Plantation and Culture", "activities": ["Morning: Spice plantation tour with traditional lunch", "Afternoon: Village tour and local crafts", "Evening: Casino experience and entertainment"]},
                    {"theme": "South Goa Serenity", "activities": ["Morning: Peaceful beaches of Palolem and Agonda", "Afternoon: Cabo de Rama Fort exploration", "Evening: Beachside massage and wellness"]},
                    {"theme": "Market and Local Life", "activities": ["Morning: Saturday Night Market at Arpora", "Afternoon: Local fishing village visit", "Evening: Beach party with DJs and dancing"]}
                ],
                "peaceful": [
                    {"theme": "Beach Meditation and Wellness", "activities": ["Morning: Meditation at peaceful beaches", "Afternoon: Visit quiet churches and heritage sites", "Evening: Silent reflection by the sea"]},
                    {"theme": "Wellness and Relaxation", "activities": ["Morning: Beach yoga and meditation", "Afternoon: Ayurvedic spa treatments", "Evening: Peaceful music and relaxation"]}
                ],
                "adventurous": [
                    {"theme": "Extreme Water Sports", "activities": ["Morning: Deep sea fishing expedition", "Afternoon: Windsurfing and kite surfing", "Evening: Night scuba diving experience"]},
                    {"theme": "Jungle and Wildlife", "activities": ["Morning: Trekking in Western Ghats", "Afternoon: Wildlife spotting at Bhagwan Mahavir Sanctuary", "Evening: Night safari and camping"]}
                ]
            },
            
            # Manali
            "manali": {
                "peaceful": [
                    {"theme": "Rohtang Pass Serenity", "activities": ["Morning: Drive to Rohtang Pass for snow activities", "Afternoon: Peaceful walks in Solang Valley", "Evening: Quiet time at Old Manali cafes"]},
                    {"theme": "Temple and Spirituality", "activities": ["Morning: Visit Hidimba Devi Temple", "Afternoon: Manu Temple and meditation", "Evening: Vashisht hot springs relaxation"]},
                    {"theme": "Nature Retreat", "activities": ["Morning: Jogini Falls trek", "Afternoon: Apple orchards walk", "Evening: Beas River side contemplation"]},
                    {"theme": "Local Culture", "activities": ["Morning: Old Manali village exploration", "Afternoon: Tibetan monasteries visit", "Evening: Local Himachali cuisine experience"]},
                    {"theme": "Mountain Meditation", "activities": ["Morning: Sunrise at Gulaba", "Afternoon: Forest meditation walks", "Evening: Yoga at mountain resorts"]}
                ],
                "adventurous": [
                    {"theme": "High Altitude Adventure", "activities": ["Morning: Rohtang Pass adventure activities", "Afternoon: Paragliding in Solang Valley", "Evening: Mountain camping at Gulaba"]},
                    {"theme": "River and Rock Adventures", "activities": ["Morning: River rafting in Beas", "Afternoon: Rock climbing at local crags", "Evening: Adventure photography at sunset points"]},
                    {"theme": "Trekking Expeditions", "activities": ["Morning: Bhrigu Lake trek start", "Afternoon: Continue to high altitude meadows", "Evening: Camping under starlit sky"]},
                    {"theme": "Winter Sports", "activities": ["Morning: Skiing at Solang Valley", "Afternoon: Snowboarding and snow activities", "Evening: Mountain adventure stories by bonfire"]}
                ],
                "fun": [
                    {"theme": "Mall Road Entertainment", "activities": ["Morning: Shopping at Mall Road", "Afternoon: Local market exploration", "Evening: Live music at cafes"]},
                    {"theme": "Adventure Activities", "activities": ["Morning: Zorbing and ropeway rides", "Afternoon: ATV rides in mountains", "Evening: Cultural performances and local food"]},
                    {"theme": "Social Mountain Experience", "activities": ["Morning: Group trekking activities", "Afternoon: Adventure sports with friends", "Evening: Bonfire parties and music"]}
                ]
            },

            # Shimla
            "shimla": {
                "peaceful": [
                    {"theme": "Colonial Heritage", "activities": ["Morning: Viceregal Lodge and gardens", "Afternoon: Christ Church and peaceful walks", "Evening: Quiet time at Scandal Point"]},
                    {"theme": "Toy Train Journey", "activities": ["Morning: Kalka-Shimla toy train experience", "Afternoon: Pine forest walks at Mashobra", "Evening: Sunset at Jakhoo Temple"]},
                    {"theme": "Nature and Serenity", "activities": ["Morning: Chadwick Falls trek", "Afternoon: Summer Hill peaceful walks", "Evening: Ridge relaxation and mountain views"]},
                    {"theme": "Hill Station Culture", "activities": ["Morning: State Museum visit", "Afternoon: Local craft shopping at Lakkar Bazaar", "Evening: Traditional Himachali dinner"]},
                    {"theme": "Mountain Retreat", "activities": ["Morning: Kufri nature walks", "Afternoon: Green Valley meditation", "Evening: Peaceful evening at hotel gardens"]}
                ],
                "adventurous": [
                    {"theme": "Adventure Sports", "activities": ["Morning: River rafting near Shimla", "Afternoon: Trekking to Shali Peak", "Evening: Rock climbing activities"]},
                    {"theme": "Mountain Exploration", "activities": ["Morning: Bike rides to Narkanda", "Afternoon: Adventure activities at Kufri", "Evening: Night camping in forests"]},
                    {"theme": "High Altitude Trekking", "activities": ["Morning: Churdhar Peak trek", "Afternoon: Continue through dense forests", "Evening: Mountain camping under stars"]}
                ],
                "fun": [
                    {"theme": "Mall Road Shopping", "activities": ["Morning: Shopping at Mall Road", "Afternoon: Local market exploration", "Evening: Cultural shows and entertainment"]},
                    {"theme": "Food and Entertainment", "activities": ["Morning: Local food tours", "Afternoon: Adventure parks visit", "Evening: Live music and dancing at hotels"]},
                    {"theme": "Social Activities", "activities": ["Morning: Group activities at Ridge", "Afternoon: Fun rides and games", "Evening: Local cultural performances"]}
                ]
            },

            # Jaipur
            "jaipur": {
                "fun": [
                    {"theme": "Royal Palaces Tour", "activities": ["Morning: Amber Fort and elephant rides", "Afternoon: City Palace and museum", "Evening: Hawa Mahal and pink city walk"]},
                    {"theme": "Cultural Immersion", "activities": ["Morning: Jantar Mantar astronomical observatory", "Afternoon: Local bazaar shopping (Johari Bazaar)", "Evening: Traditional Rajasthani dinner with folk dance"]},
                    {"theme": "Adventure and Fun", "activities": ["Morning: Hot air balloon over Jaipur", "Afternoon: Nahargarh Fort sunset point", "Evening: Chokhi Dhani cultural village experience"]},
                    {"theme": "Art and Craft", "activities": ["Morning: Block printing workshop", "Afternoon: Gem and jewelry market exploration", "Evening: Puppet show and cultural entertainment"]},
                    {"theme": "Royal Experience", "activities": ["Morning: Jal Mahal photo session", "Afternoon: Royal vintage car museum", "Evening: Heritage hotel experience with traditional music"]}
                ],
                "peaceful": [
                    {"theme": "Garden Serenity", "activities": ["Morning: Sisodia Rani Garden peaceful walks", "Afternoon: Ram Niwas Garden and Albert Hall", "Evening: Quiet time at Birla Temple"]},
                    {"theme": "Spiritual Sites", "activities": ["Morning: Govind Dev Ji Temple", "Afternoon: Galtaji Temple (Monkey Temple)", "Evening: Evening aarti and meditation"]}
                ],
                "adventurous": [
                    {"theme": "Desert Adventures", "activities": ["Morning: Camel safari in outskirts", "Afternoon: Quad biking in desert areas", "Evening: Desert camping with traditional music"]},
                    {"theme": "Fort Exploration", "activities": ["Morning: Jaigarh Fort trek", "Afternoon: Underground passages exploration", "Evening: Adventure photography at historic sites"]}
                ]
            },

            # Udaipur
            "udaipur": {
                "peaceful": [
                    {"theme": "Lake City Serenity", "activities": ["Morning: Sunrise boat ride on Lake Pichola", "Afternoon: Saheliyon ki Bari garden walks", "Evening: Sunset at Fateh Sagar Lake"]},
                    {"theme": "Palace and Heritage", "activities": ["Morning: City Palace peaceful exploration", "Afternoon: Jagdish Temple spiritual time", "Evening: Lake palace views and meditation"]},
                    {"theme": "Cultural Immersion", "activities": ["Morning: Local art galleries visit", "Afternoon: Traditional craft workshops", "Evening: Cultural performances at Bagore ki Haveli"]},
                    {"theme": "Garden Retreat", "activities": ["Morning: Gulab Bagh and Zoo peaceful walks", "Afternoon: Shilpgram rural arts complex", "Evening: Quiet lake side dining"]}
                ],
                "fun": [
                    {"theme": "Royal Experience", "activities": ["Morning: City Palace grand tour", "Afternoon: Vintage car museum", "Evening: Royal dining experience with folk dance"]},
                    {"theme": "Lake Activities", "activities": ["Morning: Boat rides and water activities", "Afternoon: Lake side markets and shopping", "Evening: Sunset cruise with dinner"]},
                    {"theme": "Cultural Entertainment", "activities": ["Morning: Puppet show workshops", "Afternoon: Local market exploration", "Evening: Cultural performances and traditional music"]}
                ],
                "adventurous": [
                    {"theme": "Aravalli Adventures", "activities": ["Morning: Trekking in Aravalli hills", "Afternoon: Rock climbing and rappelling", "Evening: Adventure camping in wilderness"]},
                    {"theme": "Wildlife and Nature", "activities": ["Morning: Sajjangarh Wildlife Sanctuary", "Afternoon: Adventure activities at Jaisamand Lake", "Evening: Night wildlife spotting"]}
                ]
            },

            # Agra
            "agra": {
                "peaceful": [
                    {"theme": "Taj Mahal Meditation", "activities": ["Morning: Sunrise at Taj Mahal", "Afternoon: Peaceful gardens exploration", "Evening: Sunset views from Mehtab Bagh"]},
                    {"theme": "Spiritual Heritage", "activities": ["Morning: Tomb of Itimad-ud-Daulah", "Afternoon: Jama Masjid peaceful visit", "Evening: Quiet reflection at historical sites"]},
                    {"theme": "Gardens and Nature", "activities": ["Morning: Ram Bagh peaceful walks", "Afternoon: Soami Bagh meditation", "Evening: Chambal river side tranquility"]}
                ],
                "fun": [
                    {"theme": "Mughal Heritage Tour", "activities": ["Morning: Taj Mahal comprehensive tour", "Afternoon: Agra Fort exploration", "Evening: Local market shopping and food tour"]},
                    {"theme": "Cultural Experience", "activities": ["Morning: Fatehpur Sikri day trip", "Afternoon: Mughal cuisine cooking class", "Evening: Cultural show with traditional music"]},
                    {"theme": "Art and Craft", "activities": ["Morning: Marble inlay workshop", "Afternoon: Local artisan visits", "Evening: Traditional performances and shopping"]}
                ],
                "adventurous": [
                    {"theme": "Chambal Safari", "activities": ["Morning: Chambal river wildlife safari", "Afternoon: Boat rides and wildlife spotting", "Evening: Adventure camping by river"]},
                    {"theme": "Historical Exploration", "activities": ["Morning: Fatehpur Sikri adventure exploration", "Afternoon: Underground passages and hidden chambers", "Evening: Night photography at monuments"]}
                ]
            },

            # Varanasi
            "varanasi": {
                "peaceful": [
                    {"theme": "Spiritual Awakening", "activities": ["Morning: Sunrise boat ride on Ganges", "Afternoon: Kashi Vishwanath Temple", "Evening: Ganga Aarti at Dashashwamedh Ghat"]},
                    {"theme": "Ancient Wisdom", "activities": ["Morning: Sarnath Buddha temple visit", "Afternoon: Ancient university ruins exploration", "Evening: Meditation by the holy river"]},
                    {"theme": "Sacred Rituals", "activities": ["Morning: Holy bath in Ganges", "Afternoon: Ancient temples tour", "Evening: Evening prayers and spiritual discourse"]},
                    {"theme": "Cultural Spirituality", "activities": ["Morning: Classical music learning session", "Afternoon: Spiritual book reading at ghats", "Evening: Devotional singing and aarti"]}
                ],
                "fun": [
                    {"theme": "Cultural Heritage", "activities": ["Morning: Banaras Hindu University tour", "Afternoon: Silk weaving workshops", "Evening: Classical music and dance performances"]},
                    {"theme": "Street Culture", "activities": ["Morning: Ghat walks and photography", "Afternoon: Local street food tour", "Evening: Boat rides and cultural interactions"]},
                    {"theme": "Art and Music", "activities": ["Morning: Traditional music lessons", "Afternoon: Local art galleries", "Evening: Cultural performances at ghats"]}
                ],
                "adventurous": [
                    {"theme": "River Adventures", "activities": ["Morning: Ganges river rafting", "Afternoon: Cycling tour of rural areas", "Evening: Adventure camping near river"]},
                    {"theme": "Cultural Exploration", "activities": ["Morning: Village exploration outside city", "Afternoon: Rural adventure activities", "Evening: Traditional village life experience"]}
                ]
            },

            # Kochi
            "kochi": {
                "peaceful": [
                    {"theme": "Backwater Serenity", "activities": ["Morning: Peaceful houseboat cruise", "Afternoon: Kumrakom bird sanctuary", "Evening: Sunset at Vembanad Lake"]},
                    {"theme": "Heritage and Culture", "activities": ["Morning: Mattancherry Palace visit", "Afternoon: Jewish Synagogue peaceful exploration", "Evening: Chinese fishing nets meditation"]},
                    {"theme": "Spice Routes", "activities": ["Morning: Spice market aromatic walks", "Afternoon: Traditional spice garden tours", "Evening: Ayurvedic treatments and wellness"]}
                ],
                "fun": [
                    {"theme": "Backwater Adventures", "activities": ["Morning: Houseboat party cruise", "Afternoon: Water sports in backwaters", "Evening: Traditional Kathakali performance"]},
                    {"theme": "Cultural Entertainment", "activities": ["Morning: Fort Kochi street art tour", "Afternoon: Local market shopping", "Evening: Traditional music and dance shows"]},
                    {"theme": "Food and Festivities", "activities": ["Morning: Cooking class for Kerala cuisine", "Afternoon: Spice market tours", "Evening: Beach festivals and local celebrations"]}
                ],
                "adventurous": [
                    {"theme": "Backwater Trekking", "activities": ["Morning: Munnar hills day trip", "Afternoon: Tea plantation trekking", "Evening: Wildlife spotting in Periyar"]},
                    {"theme": "Water Adventures", "activities": ["Morning: Kayaking in backwaters", "Afternoon: Bamboo rafting", "Evening: Night fishing experiences"]}
                ]
            },

            # Amritsar
            "amritsar": {
                "peaceful": [
                    {"theme": "Golden Temple Spirituality", "activities": ["Morning: Golden Temple early morning prayers", "Afternoon: Langar service and meditation", "Evening: Evening prayers and kirtan"]},
                    {"theme": "Sikh Heritage", "activities": ["Morning: Akal Takht and spiritual discourse", "Afternoon: Guru Ram Das Sarai peaceful stay", "Evening: Harmandir Sahib night illumination"]},
                    {"theme": "Historical Reflection", "activities": ["Morning: Jallianwala Bagh memorial", "Afternoon: Partition Museum visit", "Evening: Peaceful contemplation at Durgiana Temple"]}
                ],
                "fun": [
                    {"theme": "Cultural Immersion", "activities": ["Morning: Golden Temple comprehensive tour", "Afternoon: Punjabi folk dance learning", "Evening: Traditional Punjabi dinner with music"]},
                    {"theme": "Border Experience", "activities": ["Morning: Wagah Border ceremony", "Afternoon: Local market shopping", "Evening: Cultural shows and entertainment"]},
                    {"theme": "Food and Festivities", "activities": ["Morning: Kulcha and lassi food tour", "Afternoon: Traditional cooking class", "Evening: Punjabi music and dance performances"]}
                ],
                "adventurous": [
                    {"theme": "Rural Punjab", "activities": ["Morning: Village tourism and farming", "Afternoon: Tractor rides and rural activities", "Evening: Traditional village camping"]},
                    {"theme": "Cultural Adventure", "activities": ["Morning: Bhangra and Gidda dance workshops", "Afternoon: Adventure sports near city", "Evening: Cultural immersion with local families"]}
                ]
            }
        }
        
        # Extract location key from destination string
        location_key = None
        destination_lower = destination.lower()
        
        if "ladakh" in destination_lower:
            location_key = "ladakh"
        elif "rishikesh" in destination_lower:
            location_key = "rishikesh"
        elif "goa" in destination_lower:
            location_key = "goa"
        elif "manali" in destination_lower:
            location_key = "manali"
        elif "shimla" in destination_lower:
            location_key = "shimla"
        elif "ooty" in destination_lower:
            location_key = "ooty"
        elif "munnar" in destination_lower:
            location_key = "munnar"
        elif "darjeeling" in destination_lower:
            location_key = "darjeeling"
        elif "gangtok" in destination_lower:
            location_key = "gangtok"
        elif "jaipur" in destination_lower:
            location_key = "jaipur"
        elif "udaipur" in destination_lower:
            location_key = "udaipur"
        elif "agra" in destination_lower:
            location_key = "agra"
        elif "varanasi" in destination_lower:
            location_key = "varanasi"
        elif "kochi" in destination_lower:
            location_key = "kochi"
        elif "amritsar" in destination_lower:
            location_key = "amritsar"
        
        # Get activities for the location and mood
        if location_key and location_key in destination_activities:
            location_data = destination_activities[location_key]
            if mood in location_data:
                activities = location_data[mood]
                # Ensure we have enough activities for the duration
                if len(activities) >= duration:
                    return activities[:duration]
                else:
                    # Add creative variations for longer trips
                    enhanced_activities = self._add_creative_variations(activities, duration, destination)
                    return enhanced_activities
        
        # If specific location not found, use general fallback with location name
        print(f"Location-specific activities not found for {destination}, using generic activities")
        return self._get_generic_activities(mood, duration)
    
    def _get_generic_activities(self, mood: str, duration: int) -> List[Dict[str, str]]:
        """Dynamic fallback activities with creative variations"""
        import random
        
        creative_themes = {
            "adventurous": [
                "Adrenaline Rush Expedition", "Extreme Adventure Challenge", "Thrill-Seeker's Paradise", 
                "Wild Frontier Exploration", "High-Octane Adventure Quest", "Daredevil's Dream Journey"
            ],
            "peaceful": [
                "Zen Harmony Experience", "Tranquil Soul Journey", "Serenity Sanctuary Discovery", 
                "Mindful Retreat Adventure", "Inner Peace Pilgrimage", "Calm Oasis Exploration"
            ],
            "fun": [
                "Cultural Celebration Fiesta", "Entertainment Extravaganza", "Social Butterfly Adventure", 
                "Joyful Discovery Journey", "Interactive Fun Festival", "Vibrant Experience Carnival"
            ]
        }
        
        activity_templates = {
            "adventurous": [
                ["Dawn conquest of challenging terrains", "Peak performance extreme activities", "Starlit adventure camp experiences"],
                ["Sunrise aquatic adventures", "Midday water sport mastery", "Evening lakeside victory celebrations"],
                ["Early thrill-seeking expeditions", "Afternoon courage-building challenges", "Twilight adventure storytelling sessions"]
            ],
            "peaceful": [
                ["Gentle morning nature meditation", "Serene afternoon wellness practices", "Peaceful evening reflection moments"],
                ["Sunrise tranquility rituals", "Midday harmony experiences", "Sunset gratitude ceremonies"],
                ["Dawn mindfulness sessions", "Calm afternoon healing practices", "Restful evening spiritual connections"]
            ],
            "fun": [
                ["Vibrant morning cultural immersion", "Energetic afternoon social activities", "Lively evening entertainment shows"],
                ["Joyful start with local festivities", "Interactive midday experiences", "Celebratory evening performances"],
                ["Fun-filled morning adventures", "Engaging afternoon discoveries", "Memorable evening celebrations"]
            ]
        }
        
        selected_activities = []
        available_themes = creative_themes[mood].copy()
        available_templates = activity_templates[mood].copy()
        
        for i in range(duration):
            # Refresh lists if empty
            if not available_themes:
                available_themes = creative_themes[mood].copy()
            if not available_templates:
                available_templates = activity_templates[mood].copy()
            
            # Select unique theme and template
            theme = random.choice(available_themes)
            template = random.choice(available_templates)
            
            available_themes.remove(theme)
            available_templates.remove(template)
            
            selected_activities.append({
                "theme": f"{theme} - Day {i+1}",
                "activities": template
            })
        
        return selected_activities
    
    def _add_creative_variations(self, base_activities: List[Dict], duration: int, destination: str) -> List[Dict]:
        """Add creative variations to prevent repetitive content"""
        import random
        
        creative_prefixes = {
            "morning": ["Dawn adventure at", "Sunrise discovery of", "Early morning exploration of", "Fresh start with", "Morning magic at", "Daybreak journey to"],
            "afternoon": ["Midday immersion in", "Afternoon adventure at", "Peak hours exploring", "Sunny afternoon at", "Prime time visit to", "Daytime discovery of"],
            "evening": ["Sunset experience at", "Evening enchantment with", "Twilight adventure at", "Golden hour at", "Dusk exploration of", "Evening serenity at"]
        }
        
        activity_enhancers = [
            "with local guide insights", "featuring authentic experiences", "including photo opportunities", "with cultural storytelling", 
            "enhanced by local traditions", "complete with regional flavors", "accompanied by expert commentary", 
            "featuring interactive experiences", "with immersive activities", "including hands-on learning"
        ]
        
        enhanced_activities = []
        for i in range(duration):
            base_activity = base_activities[i % len(base_activities)]
            enhanced_activity = {
                "theme": f"{base_activity['theme']} - Day {i+1} Special",
                "activities": []
            }
            
            for activity_text in base_activity['activities']:
                # Add creative variations to each activity
                parts = activity_text.split(': ', 1)
                if len(parts) == 2:
                    time_part = parts[0].lower()
                    activity_part = parts[1]
                    
                    # Select random creative prefix
                    if 'morning' in time_part:
                        prefix = random.choice(creative_prefixes['morning'])
                    elif 'afternoon' in time_part:
                        prefix = random.choice(creative_prefixes['afternoon'])
                    else:
                        prefix = random.choice(creative_prefixes['evening'])
                    
                    # Add enhancement
                    enhancer = random.choice(activity_enhancers)
                    enhanced_text = f"{prefix} {activity_part} {enhancer}"
                    enhanced_activity['activities'].append(enhanced_text)
                else:
                    enhanced_activity['activities'].append(activity_text)
            
            enhanced_activities.append(enhanced_activity)
        
        return enhanced_activities
    
    def _enhance_reasoning_text(self, ai_response: str, destination: str, mood: str, budget: str) -> str:
        """Enhance AI response with creative and engaging language"""
        import random
        
        # Creative introductions based on mood
        mood_intros = {
            "adventurous": [
                f"Get ready for an epic adventure in {destination}! ",
                f"{destination} is calling your adventurous spirit! ",
                f"Prepare for thrilling escapades in {destination}! ",
                f"Your adrenaline-pumping journey to {destination} awaits! "
            ],
            "peaceful": [
                f"Discover tranquil bliss in the serene landscapes of {destination}. ",
                f"Find your inner peace amidst {destination}'s calming embrace. ",
                f"Let {destination}'s peaceful aura rejuvenate your soul. ",
                f"Embrace serenity in {destination}'s tranquil haven. "
            ],
            "fun": [
                f"Get ready to create unforgettable memories in vibrant {destination}! ",
                f"{destination} promises endless entertainment and joy! ",
                f"Dive into the colorful culture and festivities of {destination}! ",
                f"Experience the lively spirit of {destination}'s celebrations! "
            ]
        }
        
        # Budget-appropriate descriptors
        budget_descriptors = {
            "budget": ["wallet-friendly", "affordable", "budget-conscious", "economical"],
            "mid-range": ["comfortable", "well-balanced", "thoughtfully curated", "perfectly planned"],
            "luxury": ["premium", "lavish", "exclusive", "world-class"]
        }
        
        # Select random intro and descriptor
        intro = random.choice(mood_intros.get(mood, mood_intros["fun"]))
        descriptor = random.choice(budget_descriptors.get(budget, budget_descriptors["mid-range"]))
        
        # Clean and enhance the AI response
        if ai_response and len(ai_response.strip()) > 50:
            # Take first meaningful part of AI response
            cleaned = ai_response.strip()[:250]
            if len(ai_response) > 250:
                cleaned += "..."
            
            # Combine with creative intro
            enhanced = f"{intro}This {descriptor} journey combines {cleaned}"
        else:
            # Fallback creative description
            enhanced = f"{intro}This {descriptor} adventure is perfectly crafted for your {mood} mood, offering unique experiences that blend local culture with unforgettable moments."
        
        return enhanced
    
    def _calculate_transport_cost(self, user_city: str, destination_city: str, transport_mode: str) -> Dict[str, int]:
        """Calculate transport costs based on route and mode"""
        
        # Distance matrix for major Indian city pairs (approximate distances in km)
        distance_matrix = {
            # From Delhi
            ("Delhi", "Goa"): 1500, ("Delhi", "Manali"): 550, ("Delhi", "Shimla"): 350,
            ("Delhi", "Rishikesh"): 240, ("Delhi", "Udaipur"): 650, ("Delhi", "Jaipur"): 280,
            ("Delhi", "Agra"): 230, ("Delhi", "Varanasi"): 800, ("Delhi", "Kochi"): 2200,
            ("Delhi", "Munnar"): 2300, ("Delhi", "Ooty"): 2000, ("Delhi", "Darjeeling"): 1500,
            ("Delhi", "Gangtok"): 1600, ("Delhi", "Leh-Ladakh"): 1000, ("Delhi", "Amritsar"): 450,
            
            # From Mumbai
            ("Mumbai", "Goa"): 600, ("Mumbai", "Manali"): 900, ("Mumbai", "Shimla"): 800,
            ("Mumbai", "Rishikesh"): 750, ("Mumbai", "Udaipur"): 650, ("Mumbai", "Jaipur"): 750,
            ("Mumbai", "Agra"): 850, ("Mumbai", "Varanasi"): 1200, ("Mumbai", "Kochi"): 1150,
            ("Mumbai", "Munnar"): 1200, ("Mumbai", "Ooty"): 1000, ("Mumbai", "Darjeeling"): 1900,
            
            # From Bangalore
            ("Bangalore", "Goa"): 560, ("Bangalore", "Manali"): 1400, ("Bangalore", "Shimla"): 1300,
            ("Bangalore", "Rishikesh"): 1200, ("Bangalore", "Udaipur"): 1100, ("Bangalore", "Jaipur"): 1200,
            ("Bangalore", "Agra"): 1300, ("Bangalore", "Varanasi"): 1400, ("Bangalore", "Kochi"): 460,
            ("Bangalore", "Munnar"): 480, ("Bangalore", "Ooty"): 280, ("Bangalore", "Darjeeling"): 1600,
            
            # From Chennai
            ("Chennai", "Goa"): 750, ("Chennai", "Manali"): 1500, ("Chennai", "Shimla"): 1400,
            ("Chennai", "Rishikesh"): 1300, ("Chennai", "Udaipur"): 1250, ("Chennai", "Jaipur"): 1350,
            ("Chennai", "Agra"): 1400, ("Chennai", "Varanasi"): 1200, ("Chennai", "Kochi"): 700,
            ("Chennai", "Munnar"): 520, ("Chennai", "Ooty"): 350, ("Chennai", "Darjeeling"): 1400,
            
            # From Kolkata
            ("Kolkata", "Goa"): 1400, ("Kolkata", "Manali"): 1200, ("Kolkata", "Shimla"): 1100,
            ("Kolkata", "Rishikesh"): 900, ("Kolkata", "Udaipur"): 1200, ("Kolkata", "Jaipur"): 950,
            ("Kolkata", "Agra"): 850, ("Kolkata", "Varanasi"): 450, ("Kolkata", "Kochi"): 1600,
            ("Kolkata", "Munnar"): 1700, ("Kolkata", "Ooty"): 1500, ("Kolkata", "Darjeeling"): 250,
        }
        
        # Get distance (with fallback for unlisted routes)
        route = (user_city, destination_city)
        reverse_route = (destination_city, user_city)
        
        if route in distance_matrix:
            distance = distance_matrix[route]
        elif reverse_route in distance_matrix:
            distance = distance_matrix[reverse_route]
        else:
            # Fallback distance calculation for unlisted routes
            distance = 800  # Average distance
        
        # Cost calculation based on transport mode
        costs = {}
        
        if transport_mode == "Flight":
            # Flight costs: ₹3-8 per km depending on route
            base_cost = max(3000, distance * 4)
            costs["one_way"] = base_cost
            costs["round_trip"] = base_cost * 2
            
        elif "Train" in transport_mode:
            if "AC 1st Class" in transport_mode:
                costs["one_way"] = distance * 2.5
                costs["round_trip"] = costs["one_way"] * 2
            elif "AC 2nd Class" in transport_mode:
                costs["one_way"] = distance * 1.8
                costs["round_trip"] = costs["one_way"] * 2
            elif "AC 3rd Class" in transport_mode:
                costs["one_way"] = distance * 1.2
                costs["round_trip"] = costs["one_way"] * 2
                
        elif "Bus" in transport_mode:
            if "Volvo AC" in transport_mode:
                costs["one_way"] = distance * 1.5
                costs["round_trip"] = costs["one_way"] * 2
            else:  # Non-AC
                costs["one_way"] = distance * 0.8
                costs["round_trip"] = costs["one_way"] * 2
                
        elif "Car" in transport_mode:
            if "Rental" in transport_mode:
                costs["one_way"] = distance * 12  # Including driver, fuel, tolls
                costs["round_trip"] = costs["one_way"] * 2
            else:  # Own car
                costs["one_way"] = distance * 6  # Fuel and tolls only
                costs["round_trip"] = costs["one_way"] * 2
                
        elif "Bike" in transport_mode:
            if "Rental" in transport_mode:
                costs["one_way"] = distance * 4
                costs["round_trip"] = costs["one_way"] * 2
            else:  # Own bike
                costs["one_way"] = distance * 2
                costs["round_trip"] = costs["one_way"] * 2
        
        return {
            "distance": distance,
            "one_way_cost": int(costs["one_way"]),
            "round_trip_cost": int(costs["round_trip"])
        }
    
    def generate_itinerary(self, mood: str, budget: str, duration: int, user_city: str, destination_city: str, transport_mode: str) -> Dict:
        """Generate a complete trip itinerary using AI"""
        
        # Create the prompt
        prompt = self.prompts.create_trip_prompt(mood, budget, duration, user_city, destination_city, transport_mode)
        
        # Query the AI
        try:
            ai_response = self.query_huggingface_api(prompt)
            
            # Parse the response into structured format
            itinerary = self.parse_ai_response(ai_response, mood, budget, duration, user_city, destination_city, transport_mode)
            
            return itinerary
            
        except Exception as e:
            # Return a structured error response
            return {
                "error": True,
                "message": f"Failed to generate itinerary: {str(e)}",
                "destination": "Unable to generate",
                "reasoning": "There was an error connecting to the AI service. Please try again later.",
                "daily_plan": [],
                "budget_breakdown": {},
                "tips": ["Please check your internet connection and try again"]
            }
