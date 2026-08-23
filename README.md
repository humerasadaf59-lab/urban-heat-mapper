# 🌍 Urban Heat Island Analysis - FortGuard Hackathon 2026

## 📌 Project Overview

**Urban Heat Island Analysis** is a climate justice application that identifies neighborhoods experiencing heat inequality using FortGuard's Temperature API. The project analyzes urban areas to rank neighborhoods by heat vulnerability and provide actionable recommendations for city planners and communities.

**Theme:** Building the World's Temperature AI | **Problem:** Urban heat kills 1,500+ Americans yearly, disproportionately affecting low-income communities that are 5-15°F hotter than wealthy areas.

---

## 🎯 Problem Statement

Urban heat islands are a critical public health crisis:
- **1,500+** Americans die annually from heat exposure
- Low-income neighborhoods are **5-15°F hotter** than wealthy areas
- Root cause: Less vegetation, more concrete & roads
- Disproportionate impact on minorities & poor communities

**Our Solution:** Data-driven analysis to identify heat inequality and prioritize interventions.

---

## 💡 Solution: How It Works

### **The 3-Step Formula:**

```
Step 1: START WITH A PLACE
├─ Use Environmental Parameters API
├─ Fetch: Temperature, humidity, air quality
└─ Result: Real-time climate data for each neighborhood

Step 2: ADD THE CONTEXT
├─ Use Satellite View API
├─ Analyze: Building %, vegetation %, urban density
└─ Result: Understand WHY a location is hot

Step 3: SHIP A DECISION
├─ Calculate Heat Equity Score (0-100)
├─ Rank neighborhoods by vulnerability
└─ Provide: Actionable recommendations (plant trees, cooling centers, etc.)
```

---

## 🔧 Technical Architecture

### **APIs Used:**
1. **Environmental Parameters API** (Instant)
   - Heat index, apparent temperature
   - Humidity, air quality, precipitation
   - Fetch real-time climate data

2. **Satellite View API** (Async, ~5-10 sec)
   - Urban segmentation (buildings, vegetation, roads, water)
   - Identify urban composition
   - Understand environmental context

### **Analysis Pipeline:**
```
Location Input
    ↓
[Step 1] Fetch Environmental Data
    ↓
[Step 2] Get Satellite Segmentation
    ↓
[Step 3] Calculate Heat Equity Score
    - Heat Index: 40% weight
    - Vegetation: 40% weight
    - Urban Density: 20% weight
    ↓
[Step 4] Generate Rankings & Recommendations
    ↓
Output: JSON Report + Visualizations
```

---

## 📊 Key Metrics

### **Heat Equity Score Breakdown:**

| Factor | Weight | Impact |
|--------|--------|--------|
| Heat Index | 40% | Higher temps = more vulnerable |
| Vegetation % | 40% | Low green space = heat island |
| Building Density | 20% | Urban density affects cooling |

### **Risk Levels:**
- **🔴 CRITICAL** (70-100): Immediate intervention needed
- **🟡 HIGH** (50-69): Priority for planning
- **🟠 MODERATE** (30-49): Monitor regularly
- **🟢 LOW** (0-29): Baseline monitoring

---

## 📈 Results & Findings

### **Example Analysis: Kitsap County, Washington**

```
LOCATION COMPARISON:
═════════════════════════════════════════════
Location          Heat Index   Vegetation   Livability
─────────────────────────────────────────────
Seattle, WA       N/A          High         High
Washington, DC    High         Low          Low
Philadelphia, PA  High         Low          Low
═════════════════════════════════════════════

RISK ASSESSMENT:
• Heat Island Risk: LOW → CRITICAL (depending on area)
• Air Quality Risk: LOW → HIGH
• Urban Density: LOW → HIGH
• Green Space Score: 80/100 → 100/100
• Overall Livability: 80/100 → 100/100

PRIORITY ACTIONS:
1. 🌳 Plant 1000+ trees in heat-vulnerable zones
2. ❄️ Establish cooling centers in critical areas
3. 🏢 Promote green roofs on buildings
4. 💨 Improve air quality monitoring
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- API key from FortGuard Dashboard
- Git for version control

### **Installation**

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/urban-heat-mapper.git
cd urban-heat-mapper

# Install dependencies
pip install -r requirements.txt
```

### **Configuration**

Create `.env` file in project root:
```
FORTYGUARD_API_KEY=your_api_key_here
```

### **Running the Analysis**

```bash
# Run complete analysis
python urban_heat_equity_mapper_demo.py

# Expected output:
# ============================================================
# 🔍 ANALYZING: Chicago Downtown
# ============================================================
# 📍 STEP 1: Getting heatmap...
#    ✅ Heat Index: 28.5°C
#
# 🛰️  STEP 2: Getting context...
#    ✅ Vegetation: 28%
#    ✅ Buildings: 35%
#
# 🎯 STEP 3: Calculating score...
#    ✅ Score: 65.23/100 | Risk: 🟡 HIGH
#
# ============================================================
# 📊 HEAT EQUITY RANKING
# ============================================================
# 1. South Side - 🔴 CRITICAL (78.45)
#    → 🌳 Plant 1000+ trees
#    → ❄️ Create cooling centers
```

### **Output Files**

- `urban_analysis_report.json` - Detailed analysis results
- Console output - Real-time rankings and recommendations

---

## 📁 Project Structure

```
urban-heat-mapper/
├── fortyguard_client.py              # API client library
├── urban_heat_equity_mapper_demo.py   # Main analysis script
├── requirements.txt                  # Python dependencies
├── .env                              # API keys (NOT in repo)
├── .gitignore                        # Git ignore rules
├── README.md                         # This file
└── urban_analysis_report.json        # Generated results
```

---

## 🔑 API Key Management

**IMPORTANT: Never commit API keys to GitHub!**

### **Safe Configuration:**
```python
# ✅ CORRECT: Use environment variables
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("FORTYGUARD_API_KEY")
```

### **Ensure .gitignore contains:**
```
.env
*.pyc
__pycache__/
.DS_Store
```

---

## 📖 Code Examples

### **Basic Usage:**

```python
from urban_heat_equity_mapper_demo import UrbanHeatEquityMapper

# Initialize mapper
mapper = UrbanHeatEquityMapper(api_key="your_key")

# Analyze a neighborhood
mapper.analyze_neighborhood(
    lat=41.8781,
    lon=-87.6298,
    name="Chicago Downtown"
)

# Get results
mapper.print_summary()

# Export report
mapper.export_report("heat_equity_report.json")
```

### **Customizing Analysis:**

```python
# Analyze multiple cities
neighborhoods = [
    {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles"},
    {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    {"lat": 37.7749, "lon": -122.4194, "name": "San Francisco"},
]

for n in neighborhoods:
    mapper.analyze_neighborhood(n["lat"], n["lon"], n["name"])
```

---

## 🎨 Customization

### **Change Scoring Weights**

Modify vulnerability calculation in `urban_heat_equity_mapper_demo.py`:

```python
# Current: Heat 40% + Vegetation 40% + Density 20%
# Change to:
vulnerability_score = (
    heat_factor * 0.5 +        # Increase heat weight
    vegetation_factor * 0.3 +  # Decrease vegetation
    density_factor * 0.2       # Keep density same
)
```

### **Add More Neighborhoods**

Update the neighborhoods list:
```python
neighborhoods = [
    {"lat": YOUR_LAT, "lon": YOUR_LON, "name": "City Name"},
]
```

### **Add Visualizations**

```python
import matplotlib.pyplot as plt

# Create charts
plt.barh(neighborhoods, scores)
plt.xlabel("Heat Equity Score")
plt.savefig("heat_equity_chart.png")
```

---

## 🌐 Deployment Options

### **Option 1: Streamlit (Recommended)**

```bash
pip install streamlit

# Create app.py with web interface
streamlit run app.py

# Deploy to Streamlit Cloud (free)
# Share live URL: https://your-app.streamlit.app
```

### **Option 2: GitHub Pages**

```bash
# Enable in GitHub Settings → Pages
# Deploy from main branch
# Get URL: https://username.github.io/urban-heat-mapper
```

---

## 📊 Data Sources

- **Temperature Data:** FortGuard Temperature API (2-meter resolution)
- **Satellite Imagery:** Google Maps satellite view
- **Urban Segmentation:** ML-based pixel classification
- **Coverage:** United States (2019-2026)

---

## 🧑‍💻 AI Tools Used

**Disclosure:** Meta AI (Claude) was used for:
- Project analysis and documentation
- Code optimization and troubleshooting
- Visualization guidance
- Video script preparation

*Disclosure is never penalized. Transparency is valued.*

---

## 🏆 FortGuard Hackathon 2026

**Event:** Global AI Hackathon'26 - "Building the World's Temperature AI"  
**Theme:** Build something that helps the world stay cool  
**Deadline:** August 30, 2026 at 11:59 PM GST  
**Prize Pool:** $6,000 USD + Nvidia GPU access  

### **Judging Criteria (40% Weight Distribution):**
- **Urban Heat Impact** (40%) ✅ Primary focus
- **Technical Performance** (25%) ✅ Uses both APIs
- **Communication** (10%) ✅ Clear messaging
- **Innovation** (25%) ✅ Data-driven insights

---

## 📞 Support & Resources

- **FortGuard Dashboard:** https://dashboard.fortyguard.com
- **API Documentation:** https://docs-api.fortyguard.com
- **Hackathon Page:** https://www.fortyguard.com/hackathon26
- **Technical Help:** support@fortyguard.com
- **Slack Workspace:** #help-technical

---

## 📄 License

MIT License - Open source for community benefit

---

## 🤝 Contributing

Contributions welcome! Submit issues and pull requests to improve:
- Scoring algorithms
- Visualization quality
- Additional data sources
- Geographic expansion

---

## 🙏 Acknowledgments

- **FortGuard:** Temperature API and hackathon platform
- **Mentors:** Google Cloud, Nvidia, Autodesk
- **Inspiration:** Climate justice advocates and urban heat researchers
- **Community:** All participants building sustainable solutions

---

**Built with ❤️ for climate justice**

*Last updated: August 22, 2026*
