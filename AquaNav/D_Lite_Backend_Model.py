import heapq
import networkx as nx
import requests
import folium
from geopy.distance import geodesic
import math

# API Key (replace with your OpenWeatherMap key if needed)
OPENWEATHER_API_KEY = "257b3704eba714be791e6d893c5cc894"

# Ports Data with coordinates (latitude, longitude)
PORTS = {
    "San Francisco": (37.7749, -122.4194),
    "Tokyo": (35.6895, 139.6917),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Singapore": (1.3521, 103.8198),
    "Mumbai": (19.0760, 72.8777),
    "Cape Town": (-33.9249, 18.4241),
    "Sydney": (-33.8688, 151.2093),
    "Rio de Janeiro": (-22.9068, -43.1729)
}

# Maritime Navigation Points (important waypoints for ocean shipping)
WAYPOINTS = {
    # Major straits, canals and navigation points
    "Panama Canal East": (9.3080, -79.9150),
    "Panama Canal West": (8.8909, -79.5250),
    "Suez Canal North": (31.2156, 32.3471),
    "Suez Canal South": (29.9368, 32.5519),
    "Strait of Gibraltar": (35.9897, -5.6075),
    "Strait of Malacca": (1.7081, 101.4430),
    "Cape of Good Hope": (-34.3568, 18.4734),
    "Cape Horn": (-55.9833, -67.2667),
    "English Channel": (50.1970, -1.5820),
    "Bab el-Mandeb": (12.5611, 43.3421),
    "Strait of Hormuz": (26.5907, 56.2602),
    # Oceanic waypoints
    "North Pacific 1": (35.0000, -160.0000),
    "North Pacific 2": (35.0000, -140.0000),
    "South Pacific 1": (-20.0000, -120.0000),
    "North Atlantic 1": (40.0000, -40.0000),
    "South Atlantic 1": (-20.0000, -20.0000),
    "Indian Ocean 1": (-10.0000, 80.0000),
    "Southern Ocean 1": (-50.0000, 100.0000),
    "Southern Ocean 2": (-50.0000, 0.0000),
}

# Define valid connections between ports and waypoints
# This ensures ships follow realistic shipping lanes
VALID_CONNECTIONS = {
    # San Francisco connections
    "San Francisco": ["Panama Canal West", "North Pacific 1", "North Pacific 2"],

    # Tokyo connections
    "Tokyo": ["North Pacific 1", "North Pacific 2"],

    # New York connections
    "New York": ["Panama Canal East", "North Atlantic 1", "English Channel"],

    # London connections
    "London": ["English Channel", "Strait of Gibraltar"],

    # Singapore connections
    "Singapore": ["Strait of Malacca", "Indian Ocean 1"],

    # Mumbai connections
    "Mumbai": ["Indian Ocean 1", "Bab el-Mandeb", "Strait of Hormuz"],

    # Cape Town connections
    "Cape Town": ["Cape of Good Hope", "South Atlantic 1", "Southern Ocean 2"],

    # Sydney connections
    "Sydney": ["Southern Ocean 1", "South Pacific 1"],

    # Rio de Janeiro connections
    "Rio de Janeiro": ["South Atlantic 1", "Cape Horn", "Panama Canal East"],

    # Waypoint connections
    "Panama Canal East": ["Panama Canal West", "New York", "Rio de Janeiro"],
    "Panama Canal West": ["Panama Canal East", "San Francisco", "South Pacific 1"],
    "Suez Canal North": ["Suez Canal South", "English Channel", "Strait of Gibraltar"],
    "Suez Canal South": ["Suez Canal North", "Bab el-Mandeb", "Indian Ocean 1"],
    "Strait of Gibraltar": ["Suez Canal North", "London", "North Atlantic 1", "South Atlantic 1"],
    "Strait of Malacca": ["Singapore", "Indian Ocean 1", "South Pacific 1"],
    "Cape of Good Hope": ["Cape Town", "Indian Ocean 1", "Southern Ocean 2", "South Atlantic 1"],
    "Cape Horn": ["Rio de Janeiro", "South Pacific 1", "Southern Ocean 2", "South Atlantic 1"],
    "English Channel": ["London", "North Atlantic 1", "Suez Canal North"],
    "Bab el-Mandeb": ["Suez Canal South", "Mumbai", "Indian Ocean 1"],
    "Strait of Hormuz": ["Mumbai", "Indian Ocean 1"],
    "North Pacific 1": ["San Francisco", "Tokyo", "North Pacific 2", "South Pacific 1"],
    "North Pacific 2": ["San Francisco", "Tokyo", "North Pacific 1"],
    "South Pacific 1": ["Panama Canal West", "North Pacific 1", "Sydney", "Cape Horn", "Strait of Malacca"],
    "North Atlantic 1": ["New York", "English Channel", "Strait of Gibraltar", "South Atlantic 1"],
    "South Atlantic 1": ["North Atlantic 1", "Rio de Janeiro", "Cape of Good Hope", "Cape Horn", "Strait of Gibraltar"],
    "Indian Ocean 1": ["Strait of Malacca", "Singapore", "Mumbai", "Cape of Good Hope", "Suez Canal South",
                       "Bab el-Mandeb", "Strait of Hormuz", "Southern Ocean 1"],
    "Southern Ocean 1": ["Indian Ocean 1", "Sydney", "Southern Ocean 2"],
    "Southern Ocean 2": ["Southern Ocean 1", "Cape of Good Hope", "Cape Horn"],
}

# All locations - ports and waypoints combined
ALL_LOCATIONS = {**PORTS, **WAYPOINTS}


# Get Weather Data
def get_weather_data(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url).json()
        return {
            "description": response.get("weather", [{}])[0].get("description", "Clear"),
            "wind_speed": response.get("wind", {}).get("speed", 5),
            "temp": response.get("main", {}).get("temp", 298) - 273.15
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {"description": "Clear", "wind_speed": 5, "temp": 25}



def get_ship_traffic(location_name):
    # Set traffic levels based on location
    high_traffic = ["Panama Canal East", "Panama Canal West", "Suez Canal North",
                    "Suez Canal South", "Strait of Gibraltar", "Strait of Malacca",
                    "Singapore", "Tokyo", "New York"]
    medium_traffic = ["English Channel", "Mumbai", "London", "San Francisco",
                      "Bab el-Mandeb", "Strait of Hormuz", "Cape Town"]

    if location_name in high_traffic:
        return "High"
    elif location_name in medium_traffic:
        return "Medium"
    else:
        return "Low"


# Create Graph with weighted edges
def create_ocean_graph():
    G = nx.Graph()

    # Add nodes with location names
    for name, coords in ALL_LOCATIONS.items():
        G.add_node(name, pos=coords)

    # Add edges for valid connections only
    for location, connections in VALID_CONNECTIONS.items():
        for connection in connections:
            if connection in ALL_LOCATIONS:
                # Calculate distance
                loc1_coords = ALL_LOCATIONS[location]
                loc2_coords = ALL_LOCATIONS[connection]
                dist = geodesic(loc1_coords, loc2_coords).km

                # Get weather and traffic data
                weather1 = get_weather_data(*loc1_coords)
                weather2 = get_weather_data(*loc2_coords)
                traffic1 = get_ship_traffic(location)
                traffic2 = get_ship_traffic(connection)

                # Calculate risk factor based on weather and traffic
                risk_factor = 1.0

                # Weather factors
                for weather in [weather1, weather2]:
                    if "storm" in weather["description"].lower() or "thunderstorm" in weather["description"].lower():
                        risk_factor += 1.5
                    elif "rain" in weather["description"].lower() or "shower" in weather["description"].lower():
                        risk_factor += 0.5
                    elif "fog" in weather["description"].lower() or "mist" in weather["description"].lower():
                        risk_factor += 0.7

                    # Wind speed factor
                    if weather["wind_speed"] > 10:
                        risk_factor += 0.5

                # Traffic factors
                if traffic1 == "High" or traffic2 == "High":
                    risk_factor += 0.8
                elif traffic1 == "Medium" or traffic2 == "Medium":
                    risk_factor += 0.4

                # Special cases for difficult passages
                if "Canal" in location or "Canal" in connection or "Strait" in location or "Strait" in connection:
                    dist *= 1.2  # Canals and straits take longer to navigate

                # Edge weight is distance times risk factor
                cost = dist * risk_factor
                G.add_edge(location, connection, weight=cost, distance=dist, risk=risk_factor)

    return G


# Dijkstra's Algorithm for Path Finding
def find_shortest_path(graph, start, goal):
    # Dictionary to store shortest distance to each node
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0

    # Dictionary to store previous node in shortest path
    previous = {node: None for node in graph.nodes}

    # Priority queue of nodes to visit
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # If we've reached the goal, we're done
        if current_node == goal:
            break

        # If we've found a worse path, skip
        if current_distance > distances[current_node]:
            continue

        # Check all neighbors
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            # If we've found a better path, update
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = previous[current]

    # Reverse to get path from start to goal
    path.reverse()

    return path


# Calculate total distance and sailing time
def calculate_route_stats(graph, path):
    total_distance = 0
    total_risk_weighted = 0
    segments = []

    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        distance = graph[node1][node2]['distance']
        risk = graph[node1][node2]['risk']

        segments.append({
            'from': node1,
            'to': node2,
            'distance': distance,
            'risk': risk
        })

        total_distance += distance
        total_risk_weighted += distance * risk

    # Calculate estimated sailing time (assuming average speed of 20 knots = 37 km/h)
    avg_speed = 37  # km/h
    sailing_time_hours = total_distance / avg_speed

    # Convert to days and hours
    sailing_days = math.floor(sailing_time_hours / 24)
    sailing_hours = round(sailing_time_hours % 24)

    return {
        'total_distance': total_distance,
        'total_risk_weighted': total_risk_weighted,
        'sailing_time_hours': sailing_time_hours,
        'sailing_days': sailing_days,
        'sailing_hours': sailing_hours,
        'segments': segments
    }


# Plot on Map
def plot_route_on_map(graph, path, start_name, goal_name):
    # Get the coordinates of the first port for map centering
    start_coords = ALL_LOCATIONS[path[0]]
    route_map = folium.Map(location=start_coords, zoom_start=2, tiles="cartodbpositron")

    # Calculate route statistics
    route_stats = calculate_route_stats(graph, path)

    # Add title
    title_html = f'''
    <h3 align="center" style="font-size:16px">
    <b>Maritime Route: {start_name} to {goal_name}</b><br>
    Distance: {route_stats['total_distance']:.0f} km | 
    Est. Time: {route_stats['sailing_days']} days, {route_stats['sailing_hours']} hours
    </h3>
    '''
    route_map.get_root().html.add_child(folium.Element(title_html))

    # Add markers for ports
    for port_name, (lat, lon) in PORTS.items():
        weather = get_weather_data(lat, lon)
        traffic = get_ship_traffic(port_name)

        # More detailed popup for ports
        popup_text = f"""
        <b>{port_name} Port</b><br>
        <b>Weather:</b> {weather['description']}<br>
        <b>Wind Speed:</b> {weather['wind_speed']} m/s<br>
        <b>Temperature:</b> {weather['temp']:.1f}°C<br>
        <b>Traffic:</b> {traffic}
        """

        # Use different colors for ports in the path
        if port_name in path:
            if port_name == path[0] or port_name == path[-1]:
                # Highlight start/end ports
                folium.Marker([lat, lon], popup=folium.Popup(popup_text, max_width=300),
                              icon=folium.Icon(color='green' if port_name == path[0] else 'red',
                                               icon='ship')).add_to(route_map)
            else:
                # Other ports on the route
                folium.Marker([lat, lon], popup=folium.Popup(popup_text, max_width=300),
                              icon=folium.Icon(color='blue', icon='ship')).add_to(route_map)
        else:
            # Ports not on the route
            folium.Marker([lat, lon], popup=folium.Popup(popup_text, max_width=300),
                          icon=folium.Icon(color='gray', icon='ship')).add_to(route_map)

    # Add markers for waypoints on the route
    for waypoint in path:
        if waypoint in WAYPOINTS:
            lat, lon = WAYPOINTS[waypoint]
            weather = get_weather_data(lat, lon)
            traffic = get_ship_traffic(waypoint)

            popup_text = f"""
            <b>{waypoint}</b><br>
            <b>Weather:</b> {weather['description']}<br>
            <b>Wind Speed:</b> {weather['wind_speed']} m/s<br>
            <b>Temperature:</b> {weather['temp']:.1f}°C<br>
            <b>Traffic:</b> {traffic}
            """

            # Use a circle marker for waypoints
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                popup=folium.Popup(popup_text, max_width=300),
                color='blue',
                fill=True,
                fill_opacity=0.7
            ).add_to(route_map)

    # Add lines for the route with tooltips
    route_points = []
    for location in path:
        route_points.append(ALL_LOCATIONS[location])

    # Create segments with different colors based on risk
    for i in range(len(path) - 1):
        segment = route_stats['segments'][i]
        loc1 = path[i]
        loc2 = path[i + 1]

        # Calculate color based on risk (green->yellow->red)
        risk = segment['risk']
        if risk < 1.3:
            color = 'green'
        elif risk < 2.0:
            color = 'orange'
        else:
            color = 'red'

        # Create tooltip
        tooltip = f"{loc1} → {loc2}: {segment['distance']:.0f} km, Risk: {risk:.1f}x"

        # Add the line segment
        folium.PolyLine(
            [ALL_LOCATIONS[loc1], ALL_LOCATIONS[loc2]],
            color=color,
            weight=3,
            opacity=0.8,
            tooltip=tooltip
        ).add_to(route_map)

    # Add legend for risk levels
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:12px;
                background-color:white; padding: 10px">
                &nbsp; <b>Risk Levels</b> <br>
                &nbsp; <i class="fa fa-circle" style="color:green"></i> &nbsp; Low Risk <br>
                &nbsp; <i class="fa fa-circle" style="color:orange"></i> &nbsp; Medium Risk <br>
                &nbsp; <i class="fa fa-circle" style="color:red"></i> &nbsp; High Risk <br>
    </div>
    '''
    route_map.get_root().html.add_child(folium.Element(legend_html))

    # Save the map
    filename = f"ocean_route_map_{start_name.replace(' ', '')}_to_{goal_name.replace(' ', '')}.html"
    route_map.save(filename)
    print(f" Route map saved as '{filename}'")


# User Input
def get_user_ports():
    print("\nAvailable Ports:")
    for port in sorted(PORTS.keys()):
        print(f" - {port}")

    start_port = input("\nEnter starting port name: ").strip()
    goal_port = input("Enter destination port name: ").strip()

    if start_port not in PORTS or goal_port not in PORTS:
        print(" Invalid port name(s). Please try again.")
        return get_user_ports()

    return start_port, goal_port


# Main Function
def main():
    start_name, goal_name = get_user_ports()
    print(f"\n Calculating optimal ocean route from {start_name} to {goal_name}...")

    # Create the graph with ocean routes
    print(" Building maritime network and checking weather conditions...")
    graph = create_ocean_graph()

    # Find the shortest path
    print(" Finding optimal shipping route...")
    path = find_shortest_path(graph, start_name, goal_name)

    # Calculate stats
    route_stats = calculate_route_stats(graph, path)

    # Print the path
    print("\n Optimal Ocean Route:")
    print(f" Total distance: {route_stats['total_distance']:.0f} km")
    print(f" Estimated sailing time: {route_stats['sailing_days']} days, {route_stats['sailing_hours']} hours")
    print("\n Route waypoints:")

    for i, location in enumerate(path):
        location_type = "Port" if location in PORTS else "Waypoint"
        print(f" {i + 1}. {location} ({location_type})")

    # Plot the route
    print("\n Generating interactive map...")
    plot_route_on_map(graph, path, start_name, goal_name)
    print(" Route calculation complete!")


# Run it
if __name__ == "__main__":
    main()