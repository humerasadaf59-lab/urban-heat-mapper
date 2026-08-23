# 🌍 FortGuard Hackathon: Environmental Parameters + Satellite View

A complete starter project for building an urban climate analysis tool using FortGuard's Temperature API.

---

## 📋 What's Included

```
├── fortyguard_client.py          # API client (handles auth + requests)
├── example_urban_analyzer.py     # Complete working example
├── QUICK_START.md                # Detailed API reference
├── requirements.txt              # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Getting Started (5 Minutes)

### 1️⃣ **Get Your API Key**

```
1. Go to: https://dashboard.fortyguard.com/login
2. Log in with your hackathon credentials
3. Click "Profile" (bottom-left corner)
4. Click "Generate API Key"
5. Copy and save the key
```

### 2️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3️⃣ **Update API Key in Code**

In `example_urban_analyzer.py`, line ~135:
```python
API_KEY = "YOUR_API_KEY_HERE"  # ← Replace with your actual key
```

### 4️⃣ **Run the Example**

```bash
python example_urban_analyzer.py
```

**Expected Output:**
```
======================================================================
🔍 ANALYZING: San Francisco, CA (37.7749, -122.4194)
======================================================================

📊 Step 1/3: Fetching environmental data...
✅ Environmental data received:
   Heat Index: 28.5 °C
   Humidity: 65 %
   Air Quality Index: 52

🛰️  Step 2/3: Submitting satellite segmentation...
   Task ID: 3e1c68b-1cc3-46bc-8589-1faa3f0ef30a
   Polling for results...
   Attempt 1/30: Status = Processing
   Attempt 2/30: Status = Processing
   Attempt 3/30: Status = Completed

✅ Satellite segmentation received:
   Building: 35%
   Vegetation: 28%
   Road: 25%
   Water: 2%

⚠️  Step 3/3: Calculating risk assessment...

🎯 RISK ASSESSMENT:
   Heat Island Risk: MODERATE
   Air Quality Risk: LOW
   Urban Density: HIGH
   Green Space Score: 28/100
   Overall Livability: 85/100
```

---

## 💡 How It Works

### **Endpoint 1: Environmental Parameters** ⚡ (Instant)
Fetches real-time weather and climate data for any location.

```python
from fortyguard_client import FortGuardClient

client = FortGuardClient(api_key="your_key")

result = client.fetch_environmental_parameters(
    latitude=37.7749,
    longitude=-122.4194,
    temperature=22.5,
    start_date="2024-07-15",
    parameters=["heat_index_celsius", "air_quality_idv"]
)

# Instant response with:
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
activity_id = task["activity_id"]

# Step 2: Poll until complete
result = client.poll_task_until_complete(activity_id)

# Response with:
# - Building coverage %
# - Vegetation %
# - Road coverage %
# - Water coverage %
# - Segmentation image (Base64)
```

---

## 🎯 What You Can Build

### **Idea 1: Urban Heat Island Detector** 🌡️
```
Use Environmental Parameters (heat index) + Satellite View (vegetation %)
→ Identify areas with high heat + low vegetation
→ Show heat island risk map
```

### **Idea 2: Climate-Aware Development Site Scorer** 🏗️
```
Use both endpoints to score locations for:
- Air quality
- Temperature comfort
- Green space availability
- Urban density
→ Export scores for real estate analysis
```

### **Idea 3: Real-Time Urban Monitor Dashboard** 📊
```
Batch analyze multiple cities
Compare environmental + urban metrics
Show trends over time
→ Interactive web dashboard
```

### **Idea 4: Livability Index App** 🏙️
```
Rate neighborhoods by:
- Temperature extremes
- Air quality
- Green space
- Building density
→ Mobile/web app with ratings
```

---

## 📚 API Reference

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

### Satellite View Segmentation Output

| Segment | Meaning |
|---------|---------|
| `building` | Built structures (%) |
| `vegetation` | Trees and greenery (%) |
| `road` | Paved surfaces (%) |
| `water` | Water bodies (%) |
| `other` | Remaining (%) |

---

## ⚙️ API Constraints to Know

| Constraint | API Basic | API Premium |
|-----------|----------|-----------|
| Monthly Credits | 1,000,000 | 5,000,000 |
| Heatmap Area | Up to 10 m² | Up to 50 m² |
| Environmental Params | Full | Full |
| Satellite Segmentation | Yes | Yes |
| Access | Monthly renew | Monthly renew |
| Coverage | US Only | US Only |

### Input Constraints

- **Coordinates**: Latitude (-90 to 90), Longitude (-180 to 180)
- **Dates**: Between 2019-01-01 and 12 hours in future
- **Forecast**: Up to 12 hours ahead only
- **Rate Limit**: Don't spam - wait between requests

---

## 🐛 Troubleshooting

### ❌ "401 Unauthorized"
**Cause**: Wrong API key  
**Fix**: Verify key in dashboard → Profile → copy exact key

### ❌ "422 Invalid Request"
**Cause**: Bad coordinates or date format  
**Fix**: 
- Latitude: -90 to 90
- Longitude: -180 to 180
- Date: YYYY-MM-DD format

### ❌ "429 Rate Limited"
**Cause**: Too many requests too fast  
**Fix**: Add delay between requests

```python
import time
time.sleep(2)  # Wait 2 seconds between calls
```

### ❌ Satellite task times out
**Cause**: Takes longer than expected  
**Fix**: Increase polling time

```python
client.poll_task_until_complete(
    activity_id=activity_id,
    max_polls=60,           # More attempts
    poll_interval=3         # Longer wait between polls
)
```

---

## 📈 Performance Tips

1. **Batch requests**: Submit multiple satellite tasks before polling
2. **Cache results**: Save API responses to avoid reprocessing
3. **Parallel processing**: Use threading for multiple locations
4. **Optimize parameters**: Only request environmental data you need

```python
# Good - specific parameters
params = ["heat_index_celsius", "air_quality_idv"]

# Bad - requests everything
params = None  # Omit for all parameters
```

---

## 🏆 Hackathon Tips

1. **Start Simple**: Get one endpoint working first
2. **Add Analysis**: Calculate risk scores (like in example)
3. **Visualize**: Use matplotlib/plotly to show results
4. **Compare**: Analyze multiple locations and rank them
5. **Tell a Story**: Show actionable insights (e.g., "Best neighborhoods for families")

---

## 📞 Support

- **API Docs**: https://docs-api.fortyguard.com/docs
- **Technical Help**: support@fortyguard.com
- **General Q&A**: hackathon@fortyguard.com
- **Dashboard**: https://dashboard.fortyguard.com/login

---

## 📝 Example Output

When you run the analyzer, it generates:

1. **Console Report** - Real-time analysis output
2. **JSON Export** - `urban_analysis_report.json` with all data
3. **Comparison Table** - Side-by-side location metrics

```json
{
  "timestamp": "2024-07-15T14:32:00.123456",
  "locations_analyzed": 3,
  "data": {
    "San Francisco, CA": {
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

---

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Add API key to code
3. ✅ Run `example_urban_analyzer.py`
4. ✅ Modify it for your idea
5. ✅ Deploy and present!

---

**Good luck with your FortGuard hackathon project! 🎉**

Questions? Reach out to hackathon@fortyguard.com
