# FortGuard API Quick Start Guide
## Environmental Parameters + Satellite View

---

## 🔑 **Step 1: Get Your API Key**

1. Go to: `https://dashboard.fortyguard.com/login`
2. Log in with your hackathon account
3. Navigate to **Profile** (bottom-left)
4. Click **Generate API Key**
5. Copy and save it safely

---

## 📦 **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧪 **Step 3: Test Environmental Parameters (LIVE WEATHER DATA)**

### What it does:
- Fetches real-time weather/climate data for any location
- Returns: heat index, humidity, air quality, solar irradiance, etc.
- **No wait time** - instant response

### Code:

```python
from fortyguard_client import FortGuardClient
import json

# Initialize with your API key
client = FortGuardClient(api_key="YOUR_API_KEY_HERE")

# Fetch environmental parameters for a location
result = client.fetch_environmental_parameters(
    latitude=37.7749,          # San Francisco latitude
    longitude=-122.4194,       # San Francisco longitude
    temperature=22.5,          # Current temp in Celsius
    start_date="2024-07-15",   # Date (YYYY-MM-DD)
    parameters=[
        "heat_index_celsius",
        "relative_humidity_percent",
        "air_quality_idv"       # Air Quality Index
    ]
)

# Print the results
print(json.dumps(result, indent=2))

# Access specific data
if result.get("success"):
    data = result["data"]["data"]["result"]
    print(f"Heat Index: {data.get('heat_index_celsius')} °C")
    print(f"Humidity: {data.get('relative_humidity_percent')} %")
    print(f"Air Quality: {data.get('air_quality_idv')}")
```

### Expected Response:
```json
{
  "success": true,
  "data": {
    "error": false,
    "status_code": 200,
    "message": "Completed",
    "data": {
      "result": {
        "heat_index_celsius": 28.5,
        "relative_humidity_percent": 65,
        "air_quality_idv": 52,
        "solar_irradiance": {...}
      }
    }
  }
}
```

---

## 🛰️ **Step 4: Test Satellite View (ASYNC PROCESSING)**

### What it does:
- Submits satellite imagery segmentation request
- Returns: urban features, vegetation, roads, thermal characteristics
- **Async** - takes a few seconds to process

### Code:

```python
from fortyguard_client import FortGuardClient
import json

client = FortGuardClient(api_key="YOUR_API_KEY_HERE")

# STEP 1: Submit the task
print("📡 Submitting satellite view task...")
task_result = client.submit_satellite_view_task(
    latitude=37.7749,         # Location
    longitude=-122.4194,
    vertical_angle=0,         # Looking straight down
    horizontal_angle=0        # North view
)

print(json.dumps(task_result, indent=2))

# STEP 2: Get the activity_id
if task_result.get("success"):
    activity_id = task_result["activity_id"]
    print(f"\n✅ Task submitted! Activity ID: {activity_id}")
    
    # STEP 3: Poll until complete
    print("\n⏳ Waiting for satellite processing...")
    final_result = client.poll_task_until_complete(
        activity_id=activity_id,
        max_polls=30,
        poll_interval=2
    )
    
    # STEP 4: Access results
    if final_result.get("success"):
        result_data = final_result["data"]["data"]["result"]
        print("\n✅ Satellite data ready!")
        print(json.dumps(result_data, indent=2))
        
        # Access segmentation data
        coords = result_data.get("coordinates")
        segmentation = result_data.get("segmentation")
        print(f"Coordinates: {coords}")
        print(f"Segmentation output: {segmentation}")
```

### What the Response Contains:
```json
{
  "coordinates": {
    "latitude": "37.7749",
    "longitude": "-122.4194"
  },
  "segmentation": {
    "image_dimensions": {
      "height": 350,
      "width": 350
    },
    "segments": {          // Class coverage percentages
      "building": 35,
      "vegetation": 25,
      "road": 20,
      "water": 5,
      "other": 15
    },
    "image_content": "BASE64_ENCODED_IMAGE",  // Segmentation mask
    "image_legend": {      // Color coding
      "building": "#FF0000",
      "vegetation": "#00FF00",
      "road": "#CCCCCC"
    }
  }
}
```

---

## 🎨 **Step 5: Combine Both for a Mini Dashboard**

```python
from fortyguard_client import FortGuardClient
import json
from datetime import datetime

def create_location_report(latitude, longitude, location_name):
    """Create a combined report using both endpoints"""
    
    client = FortGuardClient(api_key="YOUR_API_KEY_HERE")
    
    print("\n" + "="*60)
    print(f"📍 LOCATION REPORT: {location_name}")
    print("="*60)
    
    # 1. Get real-time weather
    print("\n🌡️  Fetching real-time environmental data...")
    env_data = client.fetch_environmental_parameters(
        latitude=latitude,
        longitude=longitude,
        temperature=22.0,
        start_date=datetime.now().strftime("%Y-%m-%d"),
        parameters=[
            "heat_index_celsius",
            "relative_humidity_percent",
            "air_quality_idv",
            "apparent_temperature_celsius"
        ]
    )
    
    if env_data.get("success"):
        result = env_data["data"]["data"]["result"]
        print(f"\n✅ Environmental Data:")
        print(f"   Heat Index: {result.get('heat_index_celsius')} °C")
        print(f"   Feels Like: {result.get('apparent_temperature_celsius')} °C")
        print(f"   Humidity: {result.get('relative_humidity_percent')} %")
        print(f"   Air Quality: {result.get('air_quality_idv')} (higher=worse)")
    
    # 2. Get satellite segmentation
    print(f"\n📡 Submitting satellite view task...")
    sat_task = client.submit_satellite_view_task(
        latitude=latitude,
        longitude=longitude
    )
    
    if sat_task.get("success"):
        activity_id = sat_task["activity_id"]
        print(f"   Activity ID: {activity_id}")
        
        sat_result = client.poll_task_until_complete(activity_id)
        
        if sat_result.get("success"):
            seg = sat_result["data"]["data"]["result"]["segmentation"]
            segments = seg.get("segments", {})
            print(f"\n✅ Urban Coverage:")
            print(f"   Buildings: {segments.get('building', 0)}%")
            print(f"   Vegetation: {segments.get('vegetation', 0)}%")
            print(f"   Roads: {segments.get('road', 0)}%")
            print(f"   Water: {segments.get('water', 0)}%")
            
            # Analysis
            green_coverage = segments.get('vegetation', 0)
            building_coverage = segments.get('building', 0)
            
            if green_coverage < 20:
                print(f"\n⚠️  WARNING: Low vegetation ({green_coverage}%). Heat island risk!")
            else:
                print(f"\n✅ Good green space: {green_coverage}%")
    
    print("\n" + "="*60)


# Test it
if __name__ == "__main__":
    create_location_report(
        latitude=37.7749,
        longitude=-122.4194,
        location_name="San Francisco, CA"
    )
```

---

## 💡 **Project Ideas to Build**

### Idea 1: Urban Heat Island Detector
```
Use BOTH endpoints:
- Environmental Parameters → Get heat index + humidity
- Satellite View → Get vegetation % 
- Analysis: Low vegetation + high heat = heat island
- Output: Interactive map showing risk areas
```

### Idea 2: Climate-Aware Site Suitability Tool
```
Use BOTH endpoints:
- Environmental Parameters → Air quality, temp, humidity
- Satellite View → Building/vegetation coverage
- Analysis: Score locations for livability/development
- Output: Ratings for different cities/neighborhoods
```

### Idea 3: Real-Time Urban Monitoring Dashboard
```
Use BOTH endpoints:
- Environmental Parameters → Live weather trends
- Satellite View → Urban composition changes
- Analysis: Track changes over time
- Output: Dashboard showing urban growth + climate impact
```

---

## ❌ **Common Errors & Fixes**

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong/missing API key | Double-check API key in dashboard |
| `422 Invalid Request` | Bad latitude/longitude | Ensure: lat (-90,90), lon (-180,180) |
| `429 Rate Limit` | Too many requests | Wait a few seconds between calls |
| `500 Server Error` | FortGuard backend issue | Retry in a few moments |
| `Task timeout` | Task takes too long | Increase `max_polls` parameter |

---

## 📋 **Parameter Reference**

### Environmental Parameters (Available):
- `heat_index_celsius` - "Feels like" temperature
- `apparent_temperature_celsius` - Apparent temperature
- `relative_humidity_percent` - Humidity percentage
- `air_quality_idv` - Air Quality Index
- `precipitation_mm` - Rainfall
- `cloud_cover_octas` - Cloud coverage
- `solar_irradiance` - Solar energy
- `wind_speed` - Wind speed

### Satellite View (Available):
- `latitude`, `longitude` - Location
- `vertical_angle` - Tilt (-90 to 90)
- `horizontal_angle` - Pan (0-360)
- `back_view` - Capture rear view (boolean)

---

## 🚀 **Next Steps**

1. **Get your API key** → Dashboard → Profile
2. **Copy `fortyguard_client.py`** into your project
3. **Replace `YOUR_API_KEY_HERE`** with actual key
4. **Run the examples** above
5. **Build your idea** using both endpoints
6. **Deploy/present** at hackathon!

---

## 📞 **Help**

- **Technical Issues**: support@fortyguard.com
- **General Questions**: hackathon@fortyguard.com
- **API Docs**: https://docs-api.fortyguard.com/docs
