# 🚀 VoyageGPT – AI Trip Planner for Indian Destinations

**VoyageGPT** is a GenAI-powered, multilingual trip planning app that creates **mood-based**, **budget-friendly**, and **real-location** itineraries for over 70 Indian destinations. It uses **Hugging Face LLMs**, dynamic prompt engineering, and a clean **Streamlit** interface to deliver highly personalized travel experiences.

---

## 🌟 Features

- 🧠 **Mood-Based Planning**: Adventurous, Fun, or Peaceful options
- 🌐 **Multilingual Support**: Kannada, Hindi, Tamil, Telugu, and more
- 🧳 **Dynamic Pricing**: Real-time transport and stay cost estimation
- 📍 **Authentic Indian Locations**: Uses real tourist spots and attractions
- 🎯 **Budget-Aware Output**: Custom plans for ₹15K to ₹1.5L+
- 🚗 **Transport Modes**: Flight, Train, Bus, Car, Bike – all considered
- 📅 **Day-Wise Itinerary**: Creative daily themes and structured activities

---

## 📍 Supported Destinations

Includes 70+ Indian cities across categories like:
- **Hill Stations**: Manali, Shimla, Rishikesh
- **Heritage Cities**: Jaipur, Agra, Udaipur
- **Spiritual**: Varanasi, Amritsar
- **Beaches & Backwaters**: Goa, Kochi

Each with **actual tourist places** (e.g., Amber Fort, Taj Mahal, Rohtang Pass).

---

## 🛠️ How It Works

1. **User Inputs**: Mood, budget, destination, transport mode
2. **Prompt Construction**: Templates crafted in `prompts.py`
3. **LLM Call**: Hugging Face models generate itineraries
4. **Postprocessing**: Fallbacks, dynamic pricing, translation if needed
5. **Display**: Clean output with itinerary + total cost on Streamlit

---

## 🚀 Quickstart

### Requirements
- Python 3.8+
- Hugging Face API Token

### Setup

```bash
git clone https://github.com/yourusername/voyagegpt.git
cd voyagegpt
pip install -r requirements_github.txt
```

Set your `.env` or export token:

```bash
HUGGING_FACE_TOKEN=your_token_here
```

### Run Locally

```bash
streamlit run app.py
```

---

## 🧠 AI Models Used

Fallback strategy among:
- `facebook/blenderbot-400M-distill`
- `microsoft/DialoGPT-medium`
- `EleutherAI/gpt-neo-125M`
- `gpt2`

---

## 📂 File Overview

```
voyagegpt/
├── app.py               # Main Streamlit frontend
├── trip_planner.py      # Core itinerary logic
├── README.md            # This file
```

---

## 🧾 Configuration

`.env`:
```env
HUGGING_FACE_TOKEN=your_token_here
```

`.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
```

---

## 📦 Deployment Options

- ✅ Streamlit Cloud
- ✅ Hugging Face Spaces (via gradio)
- ✅ Heroku / Render / Railway (manual env setup)

---

## 💡 Future Enhancements

- [ ] Voice-based input for accessibility
- [ ] Map visualization using Leaflet or Folium
- [ ] PDF export of itineraries
- [ ] Saved trip history

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Credits

- [Hugging Face](https://huggingface.co)
- [Streamlit](https://streamlit.io)
- Indian Tourism Boards for real location insights

---

**Made with ❤️ for Indian travel lovers & GenAI enthusiasts**
