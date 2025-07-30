# AI Trip Planner 🌍

A GenAI-powered multilingual trip planner that builds mood-based, budget-friendly itineraries for Indian destinations using Hugging Face LLMs and Streamlit.

## 🌟 Features

- **Mood-Based Planning**: Choose from Adventurous, Fun, or Peaceful travel experiences
- **Dynamic Pricing**: Real-time cost calculations with transport options
- **Destination-Specific Activities**: Real tourist spots and attractions for each location
- **Budget-Aware Recommendations**: Budget-friendly to luxury trip options
- **Comprehensive Transport Options**: Flight, Train (multiple classes), Bus, Car, and Bike
- **Real Locations**: Activities based on actual places like Amber Fort (Jaipur), Rohtang Pass (Manali)

## 🗺️ Supported Destinations

### Hill Stations
- Manali (Rohtang Pass, Solang Valley, Hidimba Temple)
- Shimla (Mall Road, Christ Church, Jakhoo Temple)
- Rishikesh (Laxman Jhula, Beatles Ashram)

### Historical Cities
- Jaipur (Amber Fort, Hawa Mahal, City Palace)
- Agra (Taj Mahal, Agra Fort, Fatehpur Sikri)
- Udaipur (Lake Pichola, City Palace)

### Spiritual & Cultural
- Varanasi (Ganges Ghats, Kashi Vishwanath)
- Amritsar (Golden Temple, Wagah Border)

### Beach & Backwaters
- Goa (Beaches, Portuguese Heritage)
- Kochi (Backwaters, Chinese Fishing Nets)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Hugging Face Account (for API token)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-trip-planner.git
   cd ai-trip-planner
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   HUGGING_FACE_TOKEN=your_hugging_face_token_here
   ```
   
   Or set environment variable directly:
   ```bash
   export HUGGING_FACE_TOKEN=your_token_here
   ```

4. **Get Hugging Face API Token**
   - Visit [Hugging Face](https://huggingface.co)
   - Sign up/Login and go to Settings → Access Tokens
   - Create a new token with read permissions
   - Copy the token to your `.env` file

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:8501`
   - Start planning your trip!

## 💡 How to Use

1. **Select Your Location**: Choose your starting city
2. **Pick Your Mood**: Adventurous, Fun, or Peaceful
3. **Set Your Budget**: Budget-friendly (₹15K-50K), Mid-range (₹50K-1.5L), or Luxury (₹1.5L+)
4. **Choose Destination**: Select from 70+ Indian destinations
5. **Select Transport**: Flight, Train, Bus, Car, or Bike options
6. **Generate Trip**: Get your personalized itinerary!

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit for interactive web interface
- **Layout**: Responsive design with sidebar inputs and main content area
- **State Management**: Session-based state management

### Backend
- **AI Integration**: Hugging Face Inference API with multiple model fallbacks
- **Prompt Engineering**: Context-aware prompts for different moods and destinations
- **Cost Calculation**: Dynamic pricing based on distance, transport mode, and budget

### Key Components
- `app.py` - Main Streamlit application
- `trip_planner.py` - Core business logic and AI integration
- `prompts.py` - Prompt engineering and templates

## 🛠️ Configuration

### Environment Variables
```env
HUGGING_FACE_TOKEN=your_token_here  # Required: Hugging Face API token
```

### Streamlit Configuration
The app uses these Streamlit settings (`.streamlit/config.toml`):
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## 🔧 Development

### Project Structure
```
VoyageGPT/
├── app.py                 # Main Streamlit app
├── trip_planner.py        # Core trip planning logic
└── README.md            # This file
```

### Adding New Destinations
1. Add destination to the selectbox in `app.py`
2. Add destination-specific activities in `trip_planner.py`
3. Include real tourist spots and attractions
4. Test with different moods and budgets

### Model Configuration
The app uses multiple Hugging Face models for reliability:
- `facebook/blenderbot-400M-distill`
- `microsoft/DialoGPT-medium`
- `gpt2`
- `EleutherAI/gpt-neo-125M`

## 🎨 Features in Detail

### Dynamic Cost Calculation
- Transport costs based on actual distances between Indian cities
- Budget-appropriate accommodation and activity pricing
- Real-time total cost calculation

### Creative Content Generation
- Unique daily themes with creative variations
- Mood-based activity descriptions
- Random prefixes and enhancers to prevent repetition

### Real Tourist Spots
Instead of generic activities, the app includes:
- **Manali**: Rohtang Pass, Solang Valley, Hidimba Temple, Jogini Falls
- **Jaipur**: Amber Fort, Hawa Mahal, City Palace, Jantar Mantar
- **Agra**: Taj Mahal, Agra Fort, Fatehpur Sikri, Mehtab Bagh

## 🚦 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment
The app is configured for deployment on:
- Streamlit Cloud
- Heroku
- Railway
- Replit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co) for free LLM APIs
- [Streamlit](https://streamlit.io) for the amazing web framework
- Indian tourism data for authentic destination information

## 📞 Support

If you encounter any issues:
1. Check that your `HUGGING_FACE_TOKEN` is set correctly
2. Ensure you have internet connectivity
3. Verify all dependencies are installed
4. Open an issue on GitHub for bugs or feature requests

---

**Made with ❤️ for Indian Travel Enthusiasts**
