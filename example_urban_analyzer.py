from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("FORTYGUARD_API_KEY")   

"""
Urban Heat & Environment Analyzer
Combines Environmental Parameters + Satellite View
Perfect for FortGuard Hackathon submission
"""

import json
from datetime import datetime
from fortyguard_client import FortGuardClient


class UrbanAnalyzer:
    """Analyzes urban locations using environmental and satellite data"""
    
    def __init__(self, api_key: str):
        self.client = FortGuardClient(api_key)
        self.locations = {}
    
    def analyze_location(self, lat: float, lon: float, name: str) -> dict:
        """
        Analyze a single location with both endpoints
        
        Returns comprehensive urban analysis
        """
        print(f"\n{'='*70}")
        print(f"🔍 ANALYZING: {name} ({lat}, {lon})")
        print(f"{'='*70}")
        
        analysis = {
            "name": name,
            "coordinates": {"latitude": lat, "longitude": lon},
            "timestamp": datetime.now().isoformat(),
            "environmental": None,
            "urban_composition": None,
            "risk_assessment": None
        }
        
        # PART 1: Environmental Parameters
        print(f"\n📊 Step 1/3: Fetching environmental data...")
        env_result = self.client.fetch_environmental_parameters(
            latitude=lat,
            longitude=lon,
            temperature=22.0,
            start_date=datetime.now().strftime("%Y-%m-%d"),
            parameters=[
                "heat_index_celsius",
                "apparent_temperature_celsius",
                "relative_humidity_percent",
                "air_quality_idv",
                "precipitation_mm",
                "cloud_cover_octas"
            ]
        )
        
        if env_result.get("success"):
            env_data = env_result["data"]["data"]["result"]
            analysis["environmental"] = {
                "heat_index": env_data.get("heat_index_celsius"),
                "apparent_temp": env_data.get("apparent_temperature_celsius"),
                "humidity": env_data.get("relative_humidity_percent"),
                "air_quality": env_data.get("air_quality_idv"),
                "precipitation": env_data.get("precipitation_mm"),
                "cloud_cover": env_data.get("cloud_cover_octas")
            }
            
            print(f"✅ Environmental data received:")
            print(f"   Heat Index: {analysis['environmental']['heat_index']} °C")
            print(f"   Humidity: {analysis['environmental']['humidity']} %")
            print(f"   Air Quality Index: {analysis['environmental']['air_quality']}")
        else:
            print(f"❌ Environmental fetch failed: {env_result.get('error')}")
        
        # PART 2: Satellite View
        print(f"\n🛰️  Step 2/3: Submitting satellite segmentation...")
        sat_task = self.client.submit_satellite_view_task(
            latitude=lat,
            longitude=lon,
            vertical_angle=0,
            horizontal_angle=0
        )
        
        if sat_task.get("success"):
            activity_id = sat_task["activity_id"]
            print(f"   Task ID: {activity_id}")
            print(f"   Polling for results...")
            
            sat_result = self.client.poll_task_until_complete(
                activity_id=activity_id,
                max_polls=30,
                poll_interval=2
            )
            
            if sat_result.get("success"):
                seg_data = sat_result["data"]["data"]["result"]["segmentation"]
                analysis["urban_composition"] = seg_data.get("segments", {})
                
                print(f"\n✅ Satellite segmentation received:")
                for category, percentage in analysis["urban_composition"].items():
                    print(f"   {category.capitalize()}: {percentage}%")
            else:
                print(f"❌ Satellite processing failed: {sat_result.get('error')}")
        else:
            print(f"❌ Satellite task submission failed: {sat_task.get('error')}")
        
        # PART 3: Risk Assessment
        print(f"\n⚠️  Step 3/3: Calculating risk assessment...")
        analysis["risk_assessment"] = self._calculate_risk(analysis)
        
        print(f"\n🎯 RISK ASSESSMENT:")
        print(f"   Heat Island Risk: {analysis['risk_assessment']['heat_island_risk']}")
        print(f"   Air Quality Risk: {analysis['risk_assessment']['air_quality_risk']}")
        print(f"   Urban Density: {analysis['risk_assessment']['urban_density']}")
        print(f"   Green Space Score: {analysis['risk_assessment']['green_space_score']}/100")
        print(f"   Overall Livability: {analysis['risk_assessment']['livability_score']}/100")
        
        self.locations[name] = analysis
        return analysis
    
    def _calculate_risk(self, analysis: dict) -> dict:
        """Calculate risk scores based on collected data"""
        
        risk = {
            "heat_island_risk": "LOW",
            "air_quality_risk": "LOW",
            "urban_density": "LOW",
            "green_space_score": 100,
            "livability_score": 100
        }
        
        # Heat Island Assessment
        if analysis.get("environmental"):
            env = analysis["environmental"]
            heat_index = env.get("heat_index", 0)
            
            if heat_index > 35:
                risk["heat_island_risk"] = "CRITICAL"
                risk["livability_score"] -= 30
            elif heat_index > 30:
                risk["heat_island_risk"] = "HIGH"
                risk["livability_score"] -= 20
            elif heat_index > 25:
                risk["heat_island_risk"] = "MODERATE"
                risk["livability_score"] -= 10
            
            # Air Quality Assessment
            aqi = env.get("air_quality", 0)
            if aqi > 150:
                risk["air_quality_risk"] = "CRITICAL"
                risk["livability_score"] -= 25
            elif aqi > 100:
                risk["air_quality_risk"] = "HIGH"
                risk["livability_score"] -= 15
            elif aqi > 50:
                risk["air_quality_risk"] = "MODERATE"
                risk["livability_score"] -= 5
        
        # Urban Density Assessment
        if analysis.get("urban_composition"):
            comp = analysis["urban_composition"]
            building_pct = comp.get("building", 0)
            vegetation_pct = comp.get("vegetation", 0)
            
            if building_pct > 60:
                risk["urban_density"] = "VERY HIGH"
            elif building_pct > 40:
                risk["urban_density"] = "HIGH"
            elif building_pct > 20:
                risk["urban_density"] = "MODERATE"
            
            # Green Space Score
            risk["green_space_score"] = vegetation_pct
            
            # If vegetation is low, increase heat risk
            if vegetation_pct < 15:
                risk["livability_score"] -= 20
            elif vegetation_pct < 25:
                risk["livability_score"] -= 10
        
        # Clamp livability score
        risk["livability_score"] = max(0, min(100, risk["livability_score"]))
        
        return risk
    
    def compare_locations(self) -> dict:
        """Compare all analyzed locations"""
        
        if len(self.locations) < 2:
            return {"error": "Need at least 2 locations to compare"}
        
        print(f"\n{'='*70}")
        print(f"📊 LOCATION COMPARISON")
        print(f"{'='*70}\n")
        
        comparison = {}
        
        for name, data in self.locations.items():
            comparison[name] = {
                "heat_index": data["environmental"]["heat_index"] if data.get("environmental") else "N/A",
                "air_quality": data["environmental"]["air_quality"] if data.get("environmental") else "N/A",
                "green_space": data["urban_composition"].get("vegetation", "N/A") if data.get("urban_composition") else "N/A",
                "building_coverage": data["urban_composition"].get("building", "N/A") if data.get("urban_composition") else "N/A",
                "livability_score": data["risk_assessment"]["livability_score"]
            }
        
        # Print comparison table
        print(f"{'Location':<20} {'Heat Index':<12} {'Air Quality':<12} {'Green %':<10} {'Livability':<12}")
        print("-" * 70)
        
        for name, metrics in comparison.items():
            print(f"{name:<20} {str(metrics['heat_index']):<12} {str(metrics['air_quality']):<12} "
                  f"{str(metrics['green_space']):<10} {metrics['livability_score']:<12}")
        
        # Find best location
        best_location = max(self.locations.items(), 
                           key=lambda x: x[1]["risk_assessment"]["livability_score"])
        
        print(f"\n🏆 Best Location: {best_location[0]} "
              f"(Livability: {best_location[1]['risk_assessment']['livability_score']}/100)")
        
        return comparison
    
    def export_report(self, filename: str = "urban_analysis_report.json"):
        """Export analysis to JSON file"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "locations_analyzed": len(self.locations),
            "data": self.locations
        }
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report exported to: {filename}")
        return filename


def main():
    """Main execution - example usage"""
    
    # Initialize analyzer with your API key
    API_KEY = "e350b2eadcfad0b370d4426270a57d4a"  # Replace with actual API key
    analyzer = UrbanAnalyzer(api_key=API_KEY)
    
    # Analyze multiple locations
    locations_to_analyze = [
     {"lat": 38.9072, "lon": -77.0369, "name": "Washington, DC"},
     {"lat": 47.6062, "lon": -122.3321, "name": "Seattle, WA"},
     {"lat": 39.9526, "lon": -75.1652, "name": "Philadelphia, PA"}
]
    
    
    # Analyze each location
    for loc in locations_to_analyze:
        try:
            analyzer.analyze_location(loc["lat"], loc["lon"], loc["name"])
        except Exception as e:
            print(f"\n❌ Error analyzing {loc['name']}: {str(e)}")
    
    # Compare all locations
    analyzer.compare_locations()
    
    # Export results
    analyzer.export_report()
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"✅ Analysis complete!")
    print(f"Locations analyzed: {len(analyzer.locations)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
