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

3. Install dependencies:
    ```bash
       pip install -r requirements.txt

4. Set up your OpenWeatherMap API Key:
    - Create a .env file and add:
      ```bash 
          OPENWEATHER_API_KEY=your_api_key_here

5. Run the application:
   ```bash:
       python AquaNav/main.py

6. Access the web app:
    ```bash 
        Visit http://localhost:5000 in your browser.

## 🧪 Sample Use Case

1. Choose a starting port and destination.

2. AquaNav fetches real-time weather and simulates traffic.

3. The D* Lite algorithm calculates the safest and most efficient route.

4. A Folium map is generated showing the maritime path.

5. Download or visualize the route map from the browser.

## 📸 Screenshots

ADD

## 🤝 Acknowledgements
- OpenWeatherMap

- NetworkX

- Folium

## 👨‍💻 Authors
Author 1 – bhambeomkar@gmail.com
Author 2 - anuragsandbhor1111@gmail.com

Department of Artificial Intelligence & Data Science, Bachelor of Engineering
