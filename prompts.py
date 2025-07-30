def get_prompt(mood, location, days):
    return f"""
You are a travel assistant.
Generate a {days}-day itinerary for someone who wants a {mood} experience in {location}.
Include specific tourist places, local food suggestions, and activities. Write in an engaging and friendly tone.
"""
