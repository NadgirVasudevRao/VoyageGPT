from typing import Optional

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
