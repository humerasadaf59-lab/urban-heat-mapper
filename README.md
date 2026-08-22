# 🌍 **Urban Heat Island Analysis Tool**

> **FortGuard Hackathon 2026** | Climate Justice Tool for Identifying Urban Heat Inequality

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active Development](https://img.shields.io/badge/Status-Active-brightgreen)]()

---

## 🎯 **Project Overview**

This project analyzes **urban heat inequality** using satellite imagery and environmental data from the FortGuard API. It combines two powerful endpoints to identify heat islands, assess climate justice concerns, and provide actionable insights for urban planning.

### What It Does

✅ **Fetches Real-Time Environmental Data** (heat index, humidity, air quality)  
✅ **Analyzes Satellite Urban Composition** (buildings, vegetation, roads, water)  
✅ **Calculates Heat Equity Scores** (identifies vulnerable neighborhoods)  
✅ **Generates Vulnerability Rankings** (prioritizes heat island hotspots)  
✅ **Exports Comprehensive JSON Reports** (ready for visualization/analysis)

---

## 📊 **Key Findings**

### Kitsap County, Washington Analysis (July 2026)

| Metric | Value |
|--------|-------|
| **Temperature Range** | 67.49°F - 74.39°F |
| **Heat Island Difference** | 6.9°F |
| **Hottest Zone** | Purdy/Wauna (urban core) |
| **Coolest Zone** | Henderson Bay (water + vegetation) |
| **Data Granularity** | 100m × 100m resolution |
| **Coverage Area** | 33.46 mi² |
| **Accuracy Tier** | 1 (Most Ideal) |

### 🔴 Red Zones (Heat Islands)
- Highway 16 corridors
- Commercial/industrial areas
- Downtown centers
- **Impact**: 6-7°F hotter → increased cooling costs, health risks

### 🟢 Green Zones (Cool Areas)
- Water bodies (Henderson Bay)
- Vegetated/forest areas
- Parks and green corridors
- **Benefit**: Natural cooling effect, biodiversity

---

## 🚀 **Quick Start**

### 1️⃣ **Get Your API Key**
```
1. Visit: https://dashboard.fortyguard.com/login
2. Navigate to: Profile → Generate API Key
3. Copy and save securely
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Configure API Key**
```bash
# Create .env file
echo "FORTYGUARD_API_KEY=your_api_key_here" > .env
```

### 4️⃣ **Run Analysis**
```bash
python example_urban_analyzer.py
```

**Expected Output:**
```
======================================================================
🔍 ANALYZING: Washington, DC (38.9072, -77.0369)
======================================================================

📊 Step 1/3: Fetching environmental data...
✅ Environmental data received:
   Heat Index: 28.5 °C
   Humidity: 65 %
   Air Quality Index: 52

🛰️  Step 2/3: Submitting satellite segmentation...
   Task ID: 3e1c68b-1cc3-46bc-8589-1faa3f0ef30a
   Polling for results...
   Attempt 3/30: Status = Completed

✅ Satellite segmentation received:
   Building: 35%
   Vegetation: 28%
   Road: 25%
   Water: 2%

🎯 RISK ASSESSMENT:
   Heat Island Risk: MODERATE
   Air Quality Risk: LOW
   Urban Density: HIGH
   Green Space Score: 28/100
   Overall Livability: 85/100
```

---

## 📁 **Project Structure**

```
urban-heat-mapper/
├── example_urban_analyzer.py      # Main analysis engine
├── fortyguard_client.py            # API client (handles auth + requests)
├── requirements.txt                # Python dependencies
├── .env                            # API key (git ignored)
├── .gitignore                      # Files to exclude from Git
├── README.md                       # This file
├── QUICK_START.md                  # Detailed API reference
└── urban_analysis_report.json      # Sample output
```

---

## 🛠️ **How It Works**

### **Endpoint 1: Environmental Parameters** ⚡ (Instant)
Fetches real-time weather and climate data for any location.

```python
from fortyguard_client import FortGuardClient

client = FortGuardClient(api_key="YOUR_API_KEY")

result = client.fetch_environmental_parameters(
    latitude=37.7749,
    longitude=-122.4194,
    temperature=22.5,
    start_date="2024-07-15",
    parameters=[
        "heat_index_celsius",
        "air_quality_idv",
        "relative_humidity_percent"
    ]
)

# Returns:
# - Heat index (feels-like temperature)
# - Humidity levels
# - Air quality index
# - Solar irradiance
# - Cloud cover
# - Precipitation
```

### **Endpoint 2: Satellite View** 🛰️ (Async, ~5-10 seconds)
Segments satellite imagery to identify urban features.

```python
# Step 1: Submit task
task = client.submit_satellite_view_task(
    latitude=37.7749,
    longitude=-122.4194
)

# Step 2: Poll until complete
result = client.poll_task_until_complete(task["activity_id"])

# Returns:
# - Building coverage %
# - Vegetation %
# - Road coverage %
# - Water coverage %
# - Segmentation image (Base64)
```

### **Risk Assessment Algorithm**
Combines both endpoints to calculate:
- **Heat Island Risk** (based on temperature + vegetation %)
- **Air Quality Risk** (based on AQI levels)
- **Urban Density** (based on building coverage)
- **Green Space Score** (0-100)
- **Livability Score** (0-100)

---

## 💡 **Use Cases**

### 🌡️ **Urban Heat Island Detection**
Identify neighborhoods most affected by heat islands for targeted cooling interventions.

### 🏗️ **Climate-Aware Development**
Score potential building sites based on temperature, air quality, and green space availability.

### 📍 **Climate Justice Analysis**
Identify vulnerable populations in high-heat neighborhoods lacking green space and air quality issues.

### 🌳 **Green Infrastructure Planning**
Prioritize tree planting and park creation in hottest, least-green areas.

### 📊 **Environmental Monitoring**
Track temperature and urban composition changes over time.

---

## 📚 **API Reference**

### Environmental Parameters Available
| Parameter | Description | Example |
|-----------|-------------|---------|
| `heat_index_celsius` | Feels-like temperature | 32.5 |
| `apparent_temperature_celsius` | Apparent temperature | 31.2 |
| `relative_humidity_percent` | Humidity level | 65 |
| `air_quality_idv` | Air Quality Index | 52 |
| `precipitation_mm` | Rainfall | 0.5 |
| `cloud_cover_octas` | Cloud coverage | 3 |
| `solar_irradiance` | Solar energy | {...} |
| `wind_speed` | Wind speed | 12.5 |

### Satellite Segmentation Output
| Segment | Meaning |
|---------|---------|
| `building` | Built structures (%) |
| `vegetation` | Trees and greenery (%) |
| `road` | Paved surfaces (%) |
| `water` | Water bodies (%) |
| `other` | Remaining (%) |

---

## 🔧 **Configuration**

### Environment Variables
Create a `.env` file:
```env
FORTYGUARD_API_KEY=your_api_key_here
```

### Customize Locations
Edit `example_urban_analyzer.py` line ~160:
```python
locations_to_analyze = [
    {"lat": 38.9072, "lon": -77.0369, "name": "Washington, DC"},
    {"lat": 47.6062, "lon": -122.3321, "name": "Seattle, WA"},
    {"lat": 39.9526, "lon": -75.1652, "name": "Philadelphia, PA"}
]
```

---

## 📤 **Output Files**

The analysis generates:

1. **Console Report** - Real-time analysis and insights
2. **JSON Export** - `urban_analysis_report.json`
```json
{
  "timestamp": "2026-08-21T21:59:00.722144",
  "locations_analyzed": 3,
  "data": {
    "Washington, DC": {
      "environmental": {
        "heat_index": 28.5,
        "humidity": 65,
        "air_quality": 52
      },
      "urban_composition": {
        "building": 35,
        "vegetation": 28,
        "road": 25
      },
      "risk_assessment": {
        "heat_island_risk": "MODERATE",
        "livability_score": 85
      }
    }
  }
}
```

3. **Comparison Table** - Side-by-side location metrics

---

## ⚙️ **Requirements**

- Python 3.8+
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🐛 **Troubleshooting**

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong/missing API key | Verify key in dashboard |
| `422 Invalid Request` | Bad coordinates/date format | Check: lat (-90,90), lon (-180,180), date YYYY-MM-DD |
| `429 Rate Limited` | Too many requests | Add delay between calls: `time.sleep(2)` |
| `Task timeout` | Satellite processing takes too long | Increase `max_polls` to 60+ |

---

## 💡 **Performance Tips**

1. **Batch Requests**: Submit multiple satellite tasks before polling
2. **Cache Results**: Save API responses to avoid reprocessing
3. **Parallel Processing**: Use threading for multiple locations
4. **Optimize Parameters**: Request only environmental data you need

```python
# Good - specific parameters
params = ["heat_index_celsius", "air_quality_idv"]

# Avoid - requests everything
params = None
```

---

## 🏆 **Hackathon Achievements**

✅ Integrated Environmental Parameters API  
✅ Integrated Satellite View API  
✅ Created heat equity scoring algorithm  
✅ Generated neighborhood vulnerability rankings  
✅ Built climate justice analysis tool  
✅ Identified urban heat inequality patterns  
✅ Exported actionable insights for urban planners  

---

## 📞 **Support & Resources**

- **FortGuard API Docs**: https://docs-api.fortyguard.com/docs
- **Dashboard**: https://dashboard.fortyguard.com/login
- **Technical Help**: support@fortyguard.com
- **Hackathon Q&A**: hackathon@fortyguard.com

---

## 📝 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 **Author**

Created for FortGuard Hackathon 2026  
Focus: Climate Justice & Urban Heat Equity

---

## 🌟 **Next Steps**

1. Clone this repository
2. Get your FortGuard API key
3. Configure `.env` file with your key
4. Run `python example_urban_analyzer.py`
5. Analyze your city!
6. Share insights on climate justice

**Ready to map urban heat inequality? Let's go! 🚀**

---

*Last updated: August 2026 | FortGuard Hackathon 2026*
