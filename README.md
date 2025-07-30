# 🌍 AI Trip Planner – VoyageGPT

**VoyageGPT** is an intelligent, Streamlit-based GenAI application that generates **personalized travel itineraries** for Indian destinations using **Hugging Face LLMs**. It supports mood-based planning, budget considerations, and real tourist locations.

---

## 🌟 Features

* 🧠 **Mood-Based Planning** – Adventurous, Fun, or Peaceful
* 📊 **Dynamic Pricing** – Real-time cost calculation with transport
* 🗺️ **Destination-Specific Activities** – Includes authentic tourist spots
* 💰 **Budget Awareness** – Options from ₹15K to ₹1.5L+
* 🚗 **Comprehensive Transport Modes** – Flight, Train, Bus, Car, Bike
* 📍 **Real Indian Locations** – Like Amber Fort, Rohtang Pass, Taj Mahal

---

## 🏔️ Supported Destinations

### Hill Stations

* Manali – Rohtang Pass, Solang Valley, Hidimba Temple
* Shimla – Mall Road, Christ Church, Jakhoo Temple
* Rishikesh – Laxman Jhula, Beatles Ashram

### Historical Cities

* Jaipur – Amber Fort, Hawa Mahal, City Palace
* Agra – Taj Mahal, Agra Fort, Fatehpur Sikri
* Udaipur – Lake Pichola, City Palace

### Spiritual & Cultural

* Varanasi – Ganges Ghats, Kashi Vishwanath
* Amritsar – Golden Temple, Wagah Border

### Beaches & Backwaters

* Goa – Beaches, Portuguese Heritage
* Kochi – Backwaters, Chinese Fishing Nets

---

## 🚀 Quick Start

### ✅ Prerequisites

* Python 3.8+
* Hugging Face API token

### 🛠️ Installation

```bash
git clone https://github.com/yourusername/ai-trip-planner.git
cd ai-trip-planner
pip install -r requirements.txt
```

### 🔐 Set Up Your API Token

Create a `.env` file:

```env
HUGGING_FACE_TOKEN=your_hugging_face_token_here
```

Or set it in your terminal:

```bash
export HUGGING_FACE_TOKEN=your_token_here
```

---

### ▶️ Run Locally

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🧠 How It Works

1. Choose mood, budget, and destination
2. Backend builds a dynamic prompt (`prompts.py`)
3. Hugging Face model generates itinerary
4. Output is post-processed and displayed
5. Estimated cost shown based on distance & mode

---

## 🏗️ Architecture

### Frontend

* **Streamlit** for UI
* Sidebar + main display layout
* Session-managed interactions

### Backend

* **LLM Integration** via Hugging Face Inference API
* Prompt engineering logic for personalization
* Distance-based dynamic pricing

---

## 📁 Project Structure

```
ai-trip-planner/
├── app.py                # Main app UI
├── trip_planner.py       # Itinerary generation logic
├── prompts.py            # Prompt templates
├── .streamlit/
│   └── config.toml       # Streamlit config
├── .env.example          # Token template
├── README.md             # This file
```

---

## ⚙️ Configuration

### `.env`

```env
HUGGING_FACE_TOKEN=your_token_here
```

### `.streamlit/config.toml`

```toml
[server]
headless = true
port = 8501
enableCORS = false
```

---

## 🧪 Models Used

The app rotates among:

* `facebook/blenderbot-400M-distill`
* `microsoft/DialoGPT-medium`
* `gpt2`
* `EleutherAI/gpt-neo-125M`

---

## ✨ Special Features

### 🌟 Dynamic Pricing

* Distance-aware transport costs
* Budget category adjustments
* Tiered accommodations

### 📚 Real Content Generation

* No generic text — every plan includes real places
* Unique plans with themed descriptions
* Fun language with emotional tone

---

## 🚀 Deployment Options

* ✅ **Streamlit Cloud**
* ✅ **Railway**
* ✅ **Render**
* ✅ **Replit**

To deploy:

```bash
streamlit run app.py --server.port 8501
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Your feature"`
4. Push and open a Pull Request

---

## 📜 License

MIT License – See `LICENSE` for details.

---

## 🙏 Acknowledgments

* [Hugging Face](https://huggingface.co)
* [Streamlit](https://streamlit.io)
* Indian tourism websites for authentic data

---

> **Made with ❤️ for Indian travel lovers & GenAI explorers**
