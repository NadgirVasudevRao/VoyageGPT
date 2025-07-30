# === Prompts (inlined from prompts.py) ===
class TripPrompts:
    """Class to handle AI prompts for trip planning"""
    
    def __init__(self):
        self.base_context = """You are a professional travel advisor with expertise in creating personalized itineraries. 
        You understand different travel moods, budget constraints, and can provide detailed reasoning for your recommendations."""
    
    def create_trip_prompt(self, mood: str, budget: str, duration: int, user_city: str, destination_city: str, transport_mode: str) -> str:
        """Create a comprehensive prompt for trip generation"""
        
        mood_descriptions = {
            "adventurous": "seeking thrilling experiences, outdoor activities, extreme sports, and off-the-beaten-path destinations",
            "fun": "looking for entertainment, social activities, vibrant nightlife, festivals, and lively experiences", 
            "peaceful": "wanting tranquil hill station experiences, serene mountain views, nature walks, and relaxing environments away from city chaos"
        }
        
        budget_descriptions = {
            "budget": "budget-conscious (under ₹50,000 total), looking for affordable options while maximizing value",
            "mid-range": "comfortable spending (₹50,000-₹1,50,000), wanting good quality experiences with reasonable costs",
            "luxury": "premium budget (₹1,50,000+), seeking high-end experiences and luxury accommodations"
        }
        
        prompt = f"""As a professional Indian travel advisor, create a personalized {duration}-day trip recommendation for a traveler going from {user_city} to {destination_city} via {transport_mode}. The traveler is {mood_descriptions.get(mood, mood)} and is {budget_descriptions.get(budget, budget)}.

Please provide:
1. Why {destination_city} is perfect for someone with a {mood} mood and {budget} budget
2. Key activities and experiences in {destination_city} that align with their {mood} preferences
3. Travel considerations for the {user_city} to {destination_city} route via {transport_mode}
4. Budget considerations in Indian Rupees including transport costs

Focus on creating an authentic, detailed recommendation for {destination_city} that considers both the emotional experience they're seeking and their financial constraints.

Trip Requirements:
- Origin: {user_city}
- Destination: {destination_city}
- Duration: {duration} days
- Mood: {mood} 
- Budget level: {budget}
- Transport: {transport_mode}
- Focus: Realistic Indian travel planning

Provide a comprehensive response with specific activities in {destination_city}, realistic cost estimates in Indian Rupees, and practical travel advice for this route."""
        
        return prompt
    
    def create_activity_prompt(self, destination: str, mood: str, day_number: int) -> str:
        """Create a prompt for specific day activities"""
        return f"""Suggest specific activities for day {day_number} in {destination} for someone with a {mood} travel mood. 
        Include morning, afternoon, and evening activities with brief descriptions and why they fit the {mood} theme."""
    
    def create_budget_prompt(self, destination: str, budget_level: str, duration: int) -> str:
        """Create a prompt for budget breakdown"""
        return f"""Provide a detailed budget breakdown for a {duration}-day trip to {destination} with a {budget_level} budget level. 
        Include accommodation, food, activities, transportation, and miscellaneous expenses with realistic price ranges."""
    
    def create_reasoning_prompt(self, destination: str, mood: str, budget: str) -> str:
        """Create a prompt for AI reasoning explanation"""
        return f"""Explain why {destination} is the perfect choice for someone with a {mood} travel mood and {budget} budget. 
        Provide detailed reasoning covering the destination's appeal, cost-effectiveness, and mood alignment."""


import os
import time
import requests
from typing import Dict, List, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

# Import translation libraries
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    try:
        from googletrans import Translator as GoogleTranslator
        TRANSLATION_AVAILABLE = True
    except ImportError:
        TRANSLATION_AVAILABLE = False
        print("Translation not available: neither deep-translator nor googletrans installed")

class TripPlanner:
    def __init__(self):
        # Get Hugging Face API token from environment
        self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGING_FACE_TOKEN environment variable is required. Please set it in your environment or .env file.")
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Alternative free small models to try (optimized for size)
        self.models = [
            "EleutherAI/gpt-neo-125M",  # Small and fast
            "gpt2",  # Reliable small model
            "facebook/blenderbot-400M-distill",  # Compact conversational model
            "microsoft/DialoGPT-small"  # Smaller DialoGPT variant
        ]
        
        # Translation setup with language mappings
        self.translation_available = TRANSLATION_AVAILABLE
        self.language_codes = {
            "hi": "hi",  # Hindi
            "bn": "bn",  # Bengali
            "ta": "ta",  # Tamil
            "te": "te",  # Telugu
            "gu": "gu",  # Gujarati
            "kn": "kn",  # Kannada
            "mr": "mr",  # Marathi
            "pa": "pa",  # Punjabi
            "ml": "ml"   # Malayalam
        }
        
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        self.prompts = TripPrompts()
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language using available translation services"""
        if not self.translation_available or target_language == "en":
            return text
        
        if target_language not in self.language_codes:
            return text
            
        try:
            # Try using deep-translator first
            try:
                translator = GoogleTranslator(source='en', target=target_language)
                if hasattr(translator, 'translate'):
                    return translator.translate(text)
            except:
                # Fallback to googletrans if deep-translator fails
                try:
                    from googletrans import Translator
                    translator = Translator()
                    result = translator.translate(text, dest=target_language, src='en')
                    return result.text
                except:
                    pass
                    
        except Exception as e:
            print(f"Translation error: {e}")
            
        return text  # Return original text if translation fails

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
    
    def generate_trip_plan(self, mood: str, budget: str, duration: int, user_city: str, destination_city: str, transport_mode: str) -> Dict:
        """Main method to generate a complete trip plan"""
        
        # Generate AI prompt
        prompt = self.prompts.create_trip_prompt(
            mood=mood,
            budget=budget,
            duration=duration,
            user_city=user_city,
            destination_city=destination_city,
            transport_mode=transport_mode
        )
        
        # Get AI response
        ai_response = self.query_huggingface_api(prompt)
        
        # Parse response into structured format
        trip_data = self.parse_ai_response(
            response=ai_response,
            mood=mood,
            budget=budget,
            duration=duration,
            user_city=user_city,
            destination_city=destination_city,
            transport_mode=transport_mode
        )
        
        return trip_data
    
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
                "day": day_num,
                "theme": f"Day {day_num} - {mood.title()} Experience",
                "activities": day_activity if isinstance(day_activity, list) else [day_activity],
                "estimated_cost": self._estimate_daily_cost(budget, mood, day_num == 1)
            })
        
        # Calculate total costs
        accommodation_cost = self._calculate_accommodation_cost(budget, duration)
        food_cost = self._calculate_food_cost(budget, duration)
        activity_cost = self._calculate_activity_cost(mood, budget, duration)
        misc_cost = self._calculate_misc_cost(budget, duration)
        
        total_cost = transport_costs + accommodation_cost + food_cost + activity_cost + misc_cost
        
        return {
            "destination": destination_city,
            "duration": duration,
            "mood": mood,
            "budget": budget,
            "reasoning": cleaned_response[:500] + "..." if len(cleaned_response) > 500 else cleaned_response,
            "daily_plan": daily_plan,
            "total_cost": total_cost,
            "cost_breakdown": {
                "transport": transport_costs,
                "accommodation": accommodation_cost,
                "food": food_cost,
                "activities": activity_cost,
                "miscellaneous": misc_cost
            },
            "transport_details": {
                "mode": transport_mode,
                "cost": transport_costs,
                "route": f"{user_city} to {destination_city}"
            }
        }
    
    def _get_location_specific_activities(self, destination: str, mood: str, duration: int) -> List[List[str]]:
        """Get location and mood specific activities"""
        
        # Define activities based on destination and mood
        activity_database = {
            "Goa": {
                "adventurous": [
                    ["Water sports at Baga Beach", "Scuba diving", "Jet skiing"],
                    ["Dudhsagar Falls trek", "Spice plantation tour", "Kayaking"],
                    ["Parasailing", "Dolphin spotting cruise", "Beach volleyball"]
                ],
                "fun": [
                    ["Beach hopping", "Flea market shopping", "Beach parties"],
                    ["Casino cruise", "Nightlife in Tito's", "Live music venues"],
                    ["Food tours", "Local bars", "Cultural shows"]
                ],
                "peaceful": [
                    ["Sunrise meditation on beach", "Ayurvedic spa", "Quiet beach walks"],
                    ["Old Goa churches", "Peaceful backwaters", "Yoga sessions"],
                    ["Sunset watching", "Reading by the beach", "Nature photography"]
                ]
            },
            "Manali": {
                "adventurous": [
                    ["Rohtang Pass adventure", "River rafting", "Paragliding"],
                    ["Solang Valley skiing", "Mountain biking", "Rock climbing"],
                    ["Trekking to Bhrigu Lake", "Adventure sports", "Camping"]
                ],
                "fun": [
                    ["Mall Road shopping", "Local cafes", "Cultural programs"],
                    ["Apple orchard visits", "Local festivals", "Mountain railways"],
                    ["Photography tours", "Local markets", "Folk performances"]
                ],
                "peaceful": [
                    ["Hidimba Temple visit", "Nature walks", "Mountain meditation"],
                    ["Hot springs relaxation", "Quiet mountain views", "Bird watching"],
                    ["Peaceful forest walks", "Sunset points", "Reading in nature"]
                ]
            },
            "Rajasthan": {
                "adventurous": [
                    ["Desert safari", "Camel riding", "Dune bashing"],
                    ["Fort exploration", "Heritage walks", "Desert camping"],
                    ["Hot air ballooning", "Wildlife safari", "Adventure tours"]
                ],
                "fun": [
                    ["Cultural shows", "Folk dance", "Royal dining"],
                    ["Colorful markets", "Handicraft shopping", "Palace tours"],
                    ["Festival celebrations", "Traditional cuisine", "Local entertainment"]
                ],
                "peaceful": [
                    ["Palace gardens", "Quiet temples", "Lakeside meditation"],
                    ["Sunrise palace views", "Peaceful courtyards", "Garden walks"],
                    ["Traditional art viewing", "Quiet museums", "Spiritual sites"]
                ]
            }
        }
        
        # Get activities for the destination or use generic ones
        if destination in activity_database:
            activities = activity_database[destination].get(mood, [])
        else:
            # Generic activities based on mood
            generic_activities = {
                "adventurous": [
                    ["Local adventure sports", "Outdoor activities", "Hiking trails"],
                    ["Cultural exploration", "Local tours", "Adventure experiences"],
                    ["Nature activities", "Exciting experiences", "Local adventures"]
                ],
                "fun": [
                    ["Local entertainment", "Cultural shows", "Shopping"],
                    ["Social activities", "Local festivals", "Food tours"],
                    ["Nightlife exploration", "Local experiences", "Entertainment venues"]
                ],
                "peaceful": [
                    ["Nature walks", "Quiet places", "Meditation spots"],
                    ["Peaceful attractions", "Serene locations", "Relaxation"],
                    ["Spiritual sites", "Calm experiences", "Quiet exploration"]
                ]
            }
            activities = generic_activities.get(mood, [["Explore local attractions", "Visit famous sites", "Try local cuisine"]])
        
        # Extend activities if duration is longer than available activities
        while len(activities) < duration:
            activities.extend(activities[:duration-len(activities)])
        
        return activities[:duration]
    
    def _calculate_transport_cost(self, origin: str, destination: str, transport_mode: str) -> int:
        """Calculate transport costs"""
        base_costs = {
            "flight": 8000,
            "train": 2500,
            "bus": 1500,
            "car": 4000,
            "bike": 2000
        }
        return base_costs.get(transport_mode, 3000) * 2  # Round trip
    
    def _calculate_accommodation_cost(self, budget: str, duration: int) -> int:
        """Calculate accommodation costs"""
        per_night = {
            "budget": 1500,
            "mid-range": 4000,
            "luxury": 12000
        }
        return per_night.get(budget, 3000) * (duration - 1)  # One less night than days
    
    def _calculate_food_cost(self, budget: str, duration: int) -> int:
        """Calculate food costs"""
        per_day = {
            "budget": 800,
            "mid-range": 1500,
            "luxury": 3500
        }
        return per_day.get(budget, 1200) * duration
    
    def _calculate_activity_cost(self, mood: str, budget: str, duration: int) -> int:
        """Calculate activity costs"""
        mood_multipliers = {
            "adventurous": 1.5,
            "fun": 1.2,
            "peaceful": 0.8
        }
        
        budget_base = {
            "budget": 1000,
            "mid-range": 2500,
            "luxury": 6000
        }
        
        base = budget_base.get(budget, 2000)
        multiplier = mood_multipliers.get(mood, 1.0)
        
        return int(base * multiplier * duration)
    
    def _calculate_misc_cost(self, budget: str, duration: int) -> int:
        """Calculate miscellaneous costs"""
        per_day = {
            "budget": 500,
            "mid-range": 1000,
            "luxury": 2000
        }
        return per_day.get(budget, 750) * duration
    
    def _estimate_daily_cost(self, budget: str, mood: str, is_first_day: bool) -> int:
        """Estimate daily cost breakdown"""
        base_daily = {
            "budget": 2000,
            "mid-range": 4000,
            "luxury": 8000
        }
        
        daily_cost = base_daily.get(budget, 3000)
        
        # First day might have higher costs due to travel
        if is_first_day:
            daily_cost = int(daily_cost * 1.3)
        
        return daily_cost
    
    def translate_itinerary(self, itinerary: Dict, target_language: str) -> Dict:
        """Translate itinerary content to target language"""
        if not self.translation_available or target_language == "en":
            return itinerary
            
        translated_itinerary = itinerary.copy()
        
        try:
            # Translate key text fields
            if "reasoning" in itinerary:
                translated_itinerary["reasoning"] = self.translate_text(itinerary["reasoning"], target_language)
            
            # Translate daily plan activities
            if "daily_plan" in itinerary:
                translated_daily_plan = []
                for day in itinerary["daily_plan"]:
                    translated_day = day.copy()
                    if "theme" in day:
                        translated_day["theme"] = self.translate_text(day["theme"], target_language)
                    if "activities" in day and isinstance(day["activities"], list):
                        translated_day["activities"] = [
                            self.translate_text(activity, target_language) 
                            for activity in day["activities"]
                        ]
                    translated_daily_plan.append(translated_day)
                translated_itinerary["daily_plan"] = translated_daily_plan
                
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original if translation fails
            return itinerary
            
        return translated_itinerary
    
    def generate_itinerary(self, mood: str, budget: str, duration: int, user_city: str, destination_city: str, transport_mode: str, language: str = "en") -> Dict:
        """Generate a complete trip itinerary using AI with optional translation"""
        
        # Create the prompt
        prompt = self.prompts.create_trip_prompt(mood, budget, duration, user_city, destination_city, transport_mode)
        
        # Query the AI
        try:
            ai_response = self.query_huggingface_api(prompt)
            
            # Parse the response into structured format
            itinerary = self.parse_ai_response(ai_response, mood, budget, duration, user_city, destination_city, transport_mode)
            
            # Translate if language is not English
            if language != "en":
                itinerary = self.translate_itinerary(itinerary, language)
            
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
