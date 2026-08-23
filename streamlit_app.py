import streamlit as st
import json

st.set_page_config(page_title="Urban Heat Island Analysis", layout="wide")

# Title
st.title("🌍 Urban Heat Island Analysis")
st.markdown("### FortGuard Hackathon 2026 - Climate Justice Tool")

# Subtitle
st.write("""
Urban Heat Island Analysis identifies neighborhoods experiencing heat inequality 
and ranks them by vulnerability using FortGuard's Temperature API.
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Problem", "Solution", "Results", "Impact"])

# TAB 1: Problem
with tab1:
    st.header("🔥 The Problem")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Urban Heat Crisis")
        st.write("• 1,500+ Americans die yearly from heat exposure")
        st.write("• Low-income neighborhoods are 5-15°F hotter")
        st.write("• Root cause: Less vegetation, more concrete")
        st.write("• Disproportionate impact on minorities & poor")
    
    with col2:
        st.subheader("Climate Injustice")
        st.write("• Wealthy areas have 40-50% vegetation")
        st.write("• Poor areas have only 8-12% vegetation")
        st.write("• Heat exposure = health crisis")
        st.write("• Needs data-driven solutions")

# TAB 2: Solution
with tab2:
    st.header("💡 The Solution")
    st.write("### 3-Step Formula")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Step 1: START WITH A PLACE")
        st.write("""
        **Environmental Parameters API**
        - Temperature data
        - Humidity levels
        - Air quality metrics
        - Real-time climate data
        """)
    
    with col2:
        st.subheader("Step 2: ADD THE CONTEXT")
        st.write("""
        **Satellite View API**
        - Building coverage %
        - Vegetation coverage %
        - Road & water coverage
        - Urban composition analysis
        """)
    
    with col3:
        st.subheader("Step 3: SHIP A DECISION")
        st.write("""
        **Heat Equity Score**
        - 0-100 vulnerability ranking
        - Priority recommendations
        - Actionable solutions
        - Community-focused insights
        """)

# TAB 3: Results
with tab3:
    st.header("📊 Analysis Results")
    
    # Try to load JSON report
    try:
        with open('urban_analysis_report.json', 'r') as f:
            data = json.load(f)
            
        st.write(f"### Total Neighborhoods Analyzed: {data['total_neighborhoods']}")
        
        for neighborhood in data['neighborhoods_analyzed']:
            with st.expander(f"📍 {neighborhood['neighborhood']} - {neighborhood['risk_level']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Vulnerability Score", f"{neighborhood['vulnerability_score']}/100")
                
                with col2:
                    st.metric("Heat Index", f"{neighborhood['heat_index']}°C")
                
                with col3:
                    st.metric("Vegetation", f"{neighborhood['vegetation_percent']}%")
                
                st.subheader("Recommendations:")
                for rec in neighborhood['recommendations']:
                    st.write(f"• {rec}")
    
    except FileNotFoundError:
        st.warning("⚠️ JSON report not found. Run analysis first.")

# TAB 4: Impact
with tab4:
    st.header("🌱 Climate Justice Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Who This Helps")
        st.write("""
        ✅ City planners prioritize investments
        ✅ Communities advocate for change
        ✅ Environmental agencies make decisions
        ✅ Vulnerable populations get support
        """)
    
    with col2:
        st.subheader("What We Can Do")
        st.write("""
        🌳 Plant 1,000+ trees in heat zones
        ❄️ Build cooling centers
        🏢 Promote green roofs
        💚 Ensure climate justice
        """)
    
    st.markdown("---")
    st.info("This tool puts data in communities' hands to fight heat inequality.")

# Footer
st.markdown("---")
st.write("""
**Built for FortGuard Hackathon 2026**  
Analyzing urban heat inequality using Temperature API  
[GitHub](https://github.com/humerasadaf59-lab/urban-heat-mapper)
""")