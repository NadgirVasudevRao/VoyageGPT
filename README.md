# VoyageGPT - AI-Powered Indian Trip Planner

VoyageGPT is an intelligent travel planning application that creates personalized itineraries for Indian destinations using AI-powered recommendations and multilingual support.

## Features

### 🤖 AI-Powered Planning
- **Hugging Face Integration**: Uses advanced language models for intelligent trip recommendations
- **Mood-Based Recommendations**: Choose from Adventurous, Fun, or Peaceful travel styles
- **Budget-Aware Planning**: Tailored suggestions for Budget, Mid-range, or Luxury preferences
- **Authentic Destinations**: Curated database of 20+ popular Indian destinations

### 🌐 Multilingual Support
- **10 Indian Languages**: Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Marathi, Punjabi, Malayalam
- **Real-time Translation**: Automatic translation of itineraries using Google Translate
- **Fallback System**: Multiple translation services for reliability

### 📋 Comprehensive Itineraries
- **Daily Activity Plans**: Detailed day-by-day schedules with themed activities
- **Cost Breakdowns**: Transparent pricing with transport, accommodation, food, and activity costs
- **Transport Options**: Support for flights, trains, buses, cars, and bikes
- **Duration Flexibility**: Plan trips from 1 to 14 days

## Installation

### Prerequisites
- Python 3.8 or higher
- Hugging Face API token (free)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voyagegpt.git
   cd voyagegpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r github_requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "HUGGING_FACE_TOKEN=your_token_here" > .env
   ```

4. **Get Hugging Face API Token**
   - Visit [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Create a new token
   - Copy the token starting with "hf_"

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

### Basic Trip Planning

1. **Select Your Preferences**
   - Choose origin and destination cities
   - Pick your travel mood (Adventurous/Fun/Peaceful)
   - Set budget level and trip duration
   - Select transport mode

2. **Choose Language**
   - Select from 10 supported Indian languages
   - All recommendations will be translated automatically

3. **Generate Your Trip**
   - Click "Generate Trip Plan"
   - Get AI-powered personalized recommendations
   - View detailed itineraries with cost breakdowns

### Example Usage

```python
# Initialize the trip planner
planner = TripPlanner()

# Generate a trip
itinerary = planner.generate_itinerary(
    mood="adventurous",
    budget="mid-range", 
    duration=7,
    user_city="Delhi",
    destination_city="Manali",
    transport_mode="flight",
    language="hi"  # Hindi
)
```

## Supported Destinations

**Hill Stations**: Manali, Shimla, Darjeeling, Ooty, Munnar
**Beach Destinations**: Goa, Kerala
**Heritage Cities**: Jaipur, Udaipur, Agra, Varanasi
**Adventure Spots**: Rishikesh, Ladakh
**Metro Cities**: Mumbai, Delhi, Bangalore, Chennai, Kolkata

## API Integration

### Hugging Face Models
The application uses multiple Hugging Face models with automatic fallback:
- EleutherAI/gpt-neo-125M
- GPT-2
- Facebook/blenderbot-400M-distill
- Microsoft/DialoGPT-small

### Translation Services
- **Primary**: Deep Translator (Google Translate API)
- **Fallback**: Google Translate Python library
- **Graceful Degradation**: Returns English if translation fails

## File Structure

```
voyagegpt/
├── app.py                 # Main Streamlit application
├── trip_planner.py        # Core AI trip planning logic
├── prompts.py            # AI prompt templates
├── github_requirements.txt  # Python dependencies
├── README.md             # This file
├── .env.example          # Environment variable template
└── replit.md            # Project documentation
```

## Configuration

### Environment Variables
```env
HUGGING_FACE_TOKEN=your_hf_token_here
```

### Streamlit Configuration
The app includes optimized settings for deployment:
- Server address: 0.0.0.0
- Port: 5000 (configurable)
- Headless mode enabled

## Deployment

### Streamlit Cloud
1. Fork this repository
2. Connect to Streamlit Cloud
3. Add `HUGGING_FACE_TOKEN` to secrets
4. Deploy directly from GitHub

### Local Development
```bash
# Development mode
streamlit run app.py --server.port 8501

# Production mode  
streamlit run app.py --server.port 5000 --server.address 0.0.0.0
```

## Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 standards
2. **Documentation**: Update README.md for new features
3. **Testing**: Test with multiple languages and destinations
4. **Dependencies**: Use minimal, stable packages

### Adding New Features
- **New Destinations**: Update destination database in `trip_planner.py`
- **Languages**: Add language codes to translation system
- **AI Models**: Add new models to fallback list

## Error Handling

The application includes comprehensive error handling:
- **API Failures**: Automatic fallback to alternative models
- **Translation Errors**: Graceful degradation to English
- **Network Issues**: User-friendly error messages
- **Invalid Inputs**: Input validation and suggestions

## Performance

### Optimization Features
- **Model Fallback**: Multiple AI models for reliability
- **Caching**: Streamlit caching for better performance
- **Lightweight Models**: Optimized for free-tier APIs
- **Minimal Dependencies**: Fast installation and startup

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

### Getting Help
- **Issues**: Report bugs via GitHub Issues
- **Features**: Request features via GitHub Issues
- **Documentation**: Refer to `replit.md` for technical details

### API Limits
- **Hugging Face**: Free tier includes generous limits
- **Translation**: Google Translate has daily limits
- **Fallback**: Application works offline with basic features

## Changelog

### v1.0.0 (2025-01-30)
- ✅ Initial release with AI-powered trip planning
- ✅ Multilingual support for 10 Indian languages
- ✅ Mood-based recommendations
- ✅ Budget-aware cost calculations
- ✅ Comprehensive destination database
- ✅ Multiple transport modes
- ✅ Responsive Streamlit interface

---

**Built with ❤️ for Indian travelers**

*Experience the future of travel planning with AI-powered personalization and multilingual support.*
