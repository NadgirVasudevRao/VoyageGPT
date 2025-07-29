import streamlit as st
import os
from trip_planner import TripPlanner
import json

# Configure page
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize trip planner
@st.cache_resource
def get_trip_planner():
    return TripPlanner()

def main():
    st.title("🌍 AI-Powered Trip Planner")
    st.markdown("### Discover your perfect trip based on your mood and budget!")
    
    # Initialize session state
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = None
    if 'generating' not in st.session_state:
        st.session_state.generating = False
    
    # Sidebar for inputs
    st.sidebar.header("Plan Your Trip")
    
    # User location input
    st.sidebar.subheader("📍 Your Location")
    user_city = st.sidebar.selectbox(
        "Select your city:",
        ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivali", "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli-Dharwad", "Tiruchirappalli", "Bareilly", "Mysore", "Tiruppur", "Gurgaon", "Aligarh", "Jalandhar", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Warangal", "Guntur", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi", "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur", "Ajmer", "Akola", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu", "Sangli-Miraj & Kupwad", "Mangalore", "Erode", "Belgaum", "Ambattur", "Tirunelveli", "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala", "Other"],
        help="Select the city you'll be traveling from"
    )
    
    if user_city == "Other":
        user_city = st.sidebar.text_input("Enter your city name:", placeholder="Type your city name")

    # Mood selection
    st.sidebar.subheader("🎭 What's your travel mood?")
    mood = st.sidebar.selectbox(
        "Choose your mood:",
        ["Adventurous", "Fun", "Peaceful"],
        help="Your mood will influence the type of activities and destinations recommended"
    )
    
    # Budget selection
    st.sidebar.subheader("💰 What's your budget range?")
    budget_ranges = {
        "Budget-friendly (₹15,000 - ₹50,000)": "budget",
        "Mid-range (₹50,000 - ₹1,50,000)": "mid-range", 
        "Luxury (₹1,50,000+)": "luxury"
    }
    
    selected_budget = st.sidebar.selectbox(
        "Choose your budget:",
        list(budget_ranges.keys()),
        help="Budget affects accommodation, dining, and activity recommendations"
    )
    budget = budget_ranges[selected_budget]
    
    # Additional preferences
    st.sidebar.subheader("🌎 Additional Preferences")
    duration = st.sidebar.slider("Trip duration (days):", 3, 14, 7)
    # Destination city selection
    st.sidebar.subheader("🏖️ Destination City")
    destination_city = st.sidebar.selectbox(
        "Select your destination:",
        ["Goa", "Manali", "Shimla", "Rishikesh", "Udaipur", "Jaipur", "Agra", "Varanasi", "Kochi", "Munnar", "Ooty", "Darjeeling", "Gangtok", "Leh-Ladakh", "Amritsar", "Haridwar", "Pushkar", "Mount Abu", "Nainital", "Mussoorie", "Kasauli", "McLeod Ganj", "Bir Billing", "Spiti Valley", "Kasol", "Tosh", "Malana", "Kedarnath", "Badrinath", "Hemkund Sahib", "Valley of Flowers", "Rohtang Pass", "Solang Valley", "Kullu", "Dharamshala", "Dalhousie", "Khajjiar", "Chamba", "Kinnaur", "Kalpa", "Sangla", "Chitkul", "Tirthan Valley", "Jibhi", "Shangarh", "Great Himalayan National Park", "Pin Valley", "Kaza", "Langza", "Hikkim", "Komic", "Chandratal", "Baralacha La", "Sarchu", "Tsomoriri", "Pangong Tso", "Nubra Valley", "Khardung La", "Magnetic Hill", "Hemis Monastery", "Thiksey Monastery", "Shey Palace", "Alchi Monastery", "Lamayuru Monastery", "Diskit Monastery", "Hunder Sand Dunes", "Other"],
        help="Choose your destination city"
    )
    
    if destination_city == "Other":
        destination_city = st.sidebar.text_input("Enter destination city:", placeholder="Type destination city name")

    # Transport mode selection
    st.sidebar.subheader("🚗 Transport Mode")
    transport_mode = st.sidebar.selectbox(
        "How do you plan to travel?",
        ["Flight", "Train (AC 1st Class)", "Train (AC 2nd Class)", "Train (AC 3rd Class)", "Bus (Volvo AC)", "Bus (Non-AC)", "Car (Own)", "Car (Rental)", "Bike (Own)", "Bike (Rental)"],
        help="Select your preferred mode of transportation"
    )
    
    # Generate button
    if st.sidebar.button("🚀 Generate My Trip", type="primary", use_container_width=True):
        st.session_state.generating = True
        st.session_state.itinerary = None
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.generating:
            st.header("✨ Generating Your Perfect Trip...")
            
            # Show loading animation
            with st.spinner("Our AI is crafting your personalized itinerary..."):
                try:
                    trip_planner = get_trip_planner()
                    
                    # Generate itinerary with new parameters
                    itinerary = trip_planner.generate_itinerary(
                        mood=mood.lower(),
                        budget=budget,
                        duration=duration,
                        user_city=user_city,
                        destination_city=destination_city,
                        transport_mode=transport_mode
                    )
                    
                    st.session_state.itinerary = itinerary
                    st.session_state.generating = False
                    st.success("🎉 Your trip has been generated!")
                    st.rerun()
                    
                except Exception as e:
                    st.session_state.generating = False
                    st.error(f"❌ Error generating trip: {str(e)}")
                    st.info("💡 Please check your internet connection and try again.")
        
        elif st.session_state.itinerary:
            st.header("🗺️ Your Personalized Itinerary")
            
            # Display the generated itinerary
            itinerary = st.session_state.itinerary
            
            # Overview section
            st.subheader("📋 Trip Overview")
            overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
            
            with overview_col1:
                st.metric("Duration", f"{duration} days")
            with overview_col2:
                st.metric("Route", f"{user_city} → {destination_city}")
            with overview_col3:
                st.metric("Transport", transport_mode)
            with overview_col4:
                st.metric("Mood", mood)
            
            # AI Reasoning
            if "reasoning" in itinerary:
                st.subheader("🤖 AI Reasoning")
                st.info(itinerary["reasoning"])
            
            # Destination
            if "destination" in itinerary:
                st.subheader("🏖️ Recommended Destination")
                st.write(f"**{itinerary['destination']}**")
                if "destination_description" in itinerary:
                    st.write(itinerary["destination_description"])
            
            # Daily itinerary
            if "daily_plan" in itinerary:
                st.subheader("📅 Day-by-Day Itinerary")
                
                for day_info in itinerary["daily_plan"]:
                    with st.expander(f"📆 {day_info['day']}", expanded=True):
                        st.markdown(f"**Theme:** **{day_info.get('theme', 'Exploration')}**")
                        
                        if "activities" in day_info:
                            st.write("**Activities:**")
                            for activity in day_info["activities"]:
                                st.write(f"• {activity}")
                        
                        if "estimated_cost" in day_info:
                            st.write(f"**Estimated cost:** {day_info['estimated_cost']}")
            
            # Budget breakdown
            if "budget_breakdown" in itinerary:
                st.subheader("💸 Budget Breakdown")
                budget_data = itinerary["budget_breakdown"]
                
                for category, amount in budget_data.items():
                    if category.lower() == "total" or "total" in category.lower():
                        st.markdown(f"**{category.title()}:** **{amount}**")
                    else:
                        st.write(f"**{category.title()}:** {amount}")
            
            # Transport Information
            if "transport_info" in itinerary:
                st.subheader("🚗 Transport Information")
                transport_info = itinerary["transport_info"]
                
                col_t1, col_t2, col_t3 = st.columns(3)
                with col_t1:
                    st.metric("Distance", f"{transport_info['distance']} km")
                with col_t2:
                    st.metric("One Way Cost", f"₹{transport_info['one_way_cost']}")
                with col_t3:
                    st.metric("Round Trip Cost", f"₹{transport_info['round_trip_cost']}")
                
                st.info(f"**Route:** {user_city} ↔ {destination_city} via {transport_mode}")

            # Tips and recommendations
            if "tips" in itinerary:
                st.subheader("💡 Travel Tips")
                for tip in itinerary["tips"]:
                    st.write(f"• {tip}")
            
            # Generate new trip button
            if st.button("🔄 Generate Another Trip", use_container_width=True):
                st.session_state.itinerary = None
                st.session_state.generating = False
                st.rerun()
        
        else:
            # Welcome screen
            st.header("Welcome to Your AI Travel Companion! ✈️")
            
            st.markdown("""
            🎯 **How it works:**
            1. Select your travel mood from the sidebar
            2. Choose your budget range
            3. Set your preferences
            4. Let our AI create your perfect itinerary!
            
            🤖 **Powered by AI:** Our advanced language model understands your preferences and creates personalized recommendations with detailed reasoning.
            
            🌟 **Mood-Based Planning:** Whether you're feeling adventurous, fun-loving, or seeking peaceful hill station experiences, we'll tailor your trip accordingly.
            """)
            
            # Feature highlights
            col_feat1, col_feat2, col_feat3 = st.columns(3)
            
            with col_feat1:
                st.markdown("""
                #### 🎭 Mood-Based
                - Adventurous trips
                - Fun experiences  
                - Peaceful hill stations
                """)
            
            with col_feat2:
                st.markdown("""
                #### 💰 Budget-Aware
                - Budget-friendly options
                - Mid-range comfort
                - Luxury experiences
                """)
            
            with col_feat3:
                st.markdown("""
                #### 🤖 AI-Powered
                - Personalized recommendations
                - Detailed reasoning
                - Smart cost estimation
                """)
    
    with col2:
        # Tips and information sidebar
        st.subheader("💡 Planning Tips")
        
        st.markdown("""
        **Mood Guide:**
        - 🏃 **Adventurous**: Hiking, extreme sports, off-the-beaten-path destinations
        - 🎉 **Fun**: Entertainment, nightlife, festivals, social activities  
        - 🧘 **Peaceful**: Hill stations, serene nature spots, tranquil mountain experiences
        
        **Budget Tips:**
        - Consider season and location
        - Look for package deals
        - Budget extra for unexpected experiences
        """)

if __name__ == "__main__":
    main()
