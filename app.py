import streamlit as st
import os
from trip_planner import TripPlanner

# Page configuration
st.set_page_config(
    page_title="VoyageGPT - AI Trip Planner",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better styling with dark mode support
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .section-header {
        color: var(--text-color);
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #F24236;
        padding-bottom: 0.5rem;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .section-header {
            color: #4ECDC4;
        }
    }
    
    /* Streamlit dark theme detection */
    [data-theme="dark"] .section-header {
        color: #4ECDC4;
    }
    
    /* Remove default Streamlit metric styling to prevent white boxes */
    .stMetric > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Ensure text is readable in both themes */
    .stMarkdown, .stWrite {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'trip_data' not in st.session_state:
    st.session_state.trip_data = None
if 'planning_complete' not in st.session_state:
    st.session_state.planning_complete = False

# Main header
st.markdown('<h1 class="main-header">✈️ VoyageGPT - AI Trip Planner</h1>', unsafe_allow_html=True)
st.markdown("### Plan your perfect Indian adventure with AI-powered mood-based recommendations")

# Indian destinations list
DESTINATIONS = [
    "Goa", "Manali", "Shimla", "Jaipur", "Udaipur", "Rishikesh", "Darjeeling", 
    "Ooty", "Agra", "Varanasi", "Amritsar", "Kerala", "Munnar", "Hampi", 
    "Ladakh", "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"
]

# Sidebar for inputs
with st.sidebar:
    st.markdown("## 🎯 Plan Your Trip")
    
    # Language selection for translation
    st.markdown("### 🌐 Language Preference")
    language_options = {
        "English": "en",
        "हिंदी (Hindi)": "hi",
        "বাংলা (Bengali)": "bn", 
        "தமிழ் (Tamil)": "ta",
        "తెలుగు (Telugu)": "te",
        "ગુજરાતી (Gujarati)": "gu",
        "ಕನ್ನಡ (Kannada)": "kn",
        "मराठी (Marathi)": "mr",
        "ਪੰਜਾਬੀ (Punjabi)": "pa",
        "മലയാളം (Malayalam)": "ml"
    }
    
    selected_language = st.selectbox(
        "Choose output language:",
        list(language_options.keys()),
        help="Select the language for your trip recommendations"
    )
    language_code = language_options[selected_language]
    
    # Check for API token
    hf_token = os.getenv("HUGGING_FACE_TOKEN")
    if not hf_token:
        st.error("⚠️ Hugging Face token not found! Please set HUGGING_FACE_TOKEN environment variable.")
        st.info("To get a token: Visit https://huggingface.co/settings/tokens")
        st.stop()
    
    # User inputs
    user_city = st.selectbox(
        "🏠 From City",
        options=DESTINATIONS,
        index=0
    )
    
    destination_city = st.selectbox(
        "🎯 To Destination",
        options=DESTINATIONS,
        index=1
    )
    
    mood = st.selectbox(
        "🎭 Travel Mood",
        options=["adventurous", "fun", "peaceful"],
        format_func=lambda x: {
            "adventurous": "🏔️ Adventurous",
            "fun": "🎉 Fun & Entertainment", 
            "peaceful": "🧘 Peaceful & Relaxing"
        }[x]
    )
    
    budget = st.selectbox(
        "💰 Budget Level",
        options=["budget", "mid-range", "luxury"],
        format_func=lambda x: {
            "budget": "💸 Budget (Under ₹50K)",
            "mid-range": "💳 Mid-range (₹50K-₹1.5L)",
            "luxury": "💎 Luxury (₹1.5L+)"
        }[x]
    )
    
    duration = st.slider("📅 Trip Duration (days)", min_value=1, max_value=14, value=5)
    
    transport_mode = st.selectbox(
        "🚗 Transport Mode",
        options=["flight", "train", "bus", "car", "bike"],
        format_func=lambda x: {
            "flight": "✈️ Flight",
            "train": "🚂 Train",
            "bus": "🚌 Bus",
            "car": "🚗 Car",
            "bike": "🏍️ Bike"
        }[x]
    )
    
    st.markdown("---")
    
    # Generate trip button
    if st.button("🚀 Generate Trip Plan", type="primary", use_container_width=True):
        if user_city == destination_city:
            st.error("Please select different cities for origin and destination!")
        else:
            with st.spinner("🤖 AI is crafting your perfect trip..."):
                try:
                    # Initialize trip planner
                    planner = TripPlanner()
                    
                    # Generate trip
                    trip_data = planner.generate_itinerary(
                        mood=mood,
                        budget=budget,
                        duration=duration,
                        user_city=user_city,
                        destination_city=destination_city,
                        transport_mode=transport_mode,
                        language=language_code
                    )
                    
                    st.session_state.trip_data = trip_data
                    st.session_state.planning_complete = True
                    st.success("✅ Trip plan generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating trip: {str(e)}")

# Main content area
if st.session_state.planning_complete and st.session_state.trip_data:
    trip = st.session_state.trip_data
    
    # Trip overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Destination", trip.get('destination', 'N/A'))
    with col2:
        st.metric("📅 Duration", f"{trip.get('duration', 0)} days")
    with col3:
        total_cost = trip.get('total_cost', 0)
        if isinstance(total_cost, str):
            st.metric("💰 Total Cost", total_cost)
        else:
            st.metric("💰 Total Cost", f"₹{total_cost:,}")
    
    st.markdown("---")
    
    # AI Reasoning
    if trip.get('reasoning'):
        st.markdown('<div class="section-header">🤖 Why This Destination?</div>', unsafe_allow_html=True)
        st.write(trip["reasoning"])
    
    # Daily Itinerary
    st.markdown('<div class="section-header">📋 Daily Itinerary</div>', unsafe_allow_html=True)
    
    for i, day in enumerate(trip.get('daily_plan', []), 1):
        with st.expander(f"📅 Day {i}: {day.get('theme', 'Exploration')}", expanded=i <= 2):
            
            # Activities for the day
            activities = day.get('activities', [])
            if activities:
                st.markdown("**🎯 Activities:**")
                for activity in activities:
                    st.markdown(f"• {activity}")
            
            # Estimated cost for the day
            day_cost = day.get('estimated_cost', 0)
            if day_cost > 0:
                st.markdown(f"**💰 Estimated Cost:** ₹{day_cost:,}")
    
    # Cost Breakdown
    if trip.get('cost_breakdown'):
        st.markdown('<div class="section-header">💰 Cost Breakdown</div>', unsafe_allow_html=True)
        
        cost_breakdown = trip['cost_breakdown']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚗 Transport Costs:**")
            st.write(f"• {transport_mode.title()}: ₹{cost_breakdown.get('transport', 0):,}")
            
            st.markdown("**🍽️ Food & Dining:**")
            st.write(f"• Total food: ₹{cost_breakdown.get('food', 0):,}")
        
        with col2:
            st.markdown("**🏨 Accommodation:**")
            st.write(f"• Total stay: ₹{cost_breakdown.get('accommodation', 0):,}")
            
            st.markdown("**🎭 Activities & Misc:**")
            st.write(f"• Activities: ₹{cost_breakdown.get('activities', 0):,}")
            st.write(f"• Miscellaneous: ₹{cost_breakdown.get('miscellaneous', 0):,}")
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Plan Another Trip", use_container_width=True):
        st.session_state.trip_data = None
        st.session_state.planning_complete = False
        st.rerun()

else:
    # Welcome screen
    st.markdown("## 🌟 Welcome to VoyageGPT!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎭 Mood-Based Planning
        Choose from **Adventurous**, **Fun**, or **Peaceful** moods to get personalized recommendations that match your travel style.
        """)
    
    with col2:
        st.markdown("""
        ### 🌐 AI-Powered Recommendations
        Get intelligent trip suggestions powered by advanced language models that understand your preferences and budget.
        """)
    
    with col3:
        st.markdown("""
        ### 💰 Smart Budgeting
        Get realistic cost breakdowns with transport, accommodation, food, and activity estimates for Indian destinations.
        """)
    
    st.markdown("---")
    
    # Featured destinations
    st.markdown("### 🗺️ Popular Destinations")
    
    featured_destinations = [
        ("🏔️ Adventurous", ["Ladakh", "Rishikesh", "Manali", "Himachal Pradesh"]),
        ("🎉 Fun", ["Goa", "Mumbai", "Delhi", "Bangalore"]),
        ("🧘 Peaceful", ["Kerala", "Ooty", "Shimla", "Darjeeling"])
    ]
    
    for mood_type, destinations in featured_destinations:
        st.markdown(f"**{mood_type}:** {' • '.join(destinations)}")
    
    st.markdown("---")
    st.markdown("### 🚀 Get Started")
    st.markdown("Use the sidebar to select your preferences and generate your personalized AI-powered trip plan!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 2rem 0;">
    Made with ❤️ for Indian travel lovers | Powered by Hugging Face AI
</div>
""", unsafe_allow_html=True)
