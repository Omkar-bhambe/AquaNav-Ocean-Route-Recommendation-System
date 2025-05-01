# 🌊 AquaNav-Ocean-Route-Recommendation-System
**AquaNav** is an intelligent ocean route optimization system that leverages AI-based pathfinding (D* Lite), real-time weather data, and marine traffic information to suggest the safest, most fuel-efficient maritime routes between global ports.

---

## 🚀 Features

- 📍 **Port-to-Port Navigation** using real-world geographic coordinates
- 🧠 **D* Lite Pathfinding Algorithm** for dynamic and responsive route planning
- 🌦️ **Real-Time Weather Integration** via OpenWeatherMap API
- 🚢 **Simulated Marine Traffic Risk Estimation**
- 🌐 **Interactive Map Visualization** using Folium
- 🧭 **Customizable Routes** based on weather and traffic constraints

---

## 📁 Project Structure

AquaNav/                    
  - D_Lite_Backend_Model.py 
  - db.py                   
  - main.py                 
  - remove_db.py            
  - templates/              
  - static/                 
    - utils/                  
    - *.html                  
- maps/                       
- requirements.txt            
- README.md  

Architecture: 
  <img src="">            


---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Flask**
- **NetworkX**
- **Geopy**
- **Folium**
- **OpenWeatherMap API**
- **D* Lite Algorithm**

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/AquaNav.git
   cd AquaNav
   
2. **Create a virtual environment (optional but recommended:**
    ```bash
        python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows

3

