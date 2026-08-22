"""
FortGuard Temperature API Client
Handles authentication and API calls for Environmental Parameters and Satellite View
"""

import requests
import time
import json
from typing import Dict, Any, Optional
import os

class FortGuardClient:
    def __init__(self, api_key: str):
        """
        Initialize FortGuard API client
        
        Args:
            api_key: Your FortGuard API key from dashboard
        """
        self.api_key = api_key
        self.base_url = "https://api.fortyguard.com/v1"
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def fetch_environmental_parameters(
        self,
        latitude: float,
        longitude: float,
        temperature: float,
        start_date: str,
        parameters: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Fetch real-time environmental parameters (weather/climate data)
        
        Args:
            latitude: Location latitude (-90 to 90)
            longitude: Location longitude (-180 to 180)
            temperature: Current temperature in Celsius
            start_date: Date in YYYY-MM-DD format
            parameters: Optional list of specific parameters to fetch
                       Examples: ["heat_index_celsius", "air_quality_idv", "relative_humidity_percent"]
        
        Returns:
            Dictionary with environmental data
        """
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature,
            "date_time": {
                "start_date": start_date,
                "start_time": "14:00",
                "filter_type": 1
            }
        }
        
        # If specific parameters requested, add them
        if parameters:
            payload["analysis"] = parameters
        
        try:
            response = requests.post(
                f"{self.base_url}/env_params",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"Error {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def submit_satellite_view_task(
        self,
        latitude: float,
        longitude: float,
        vertical_angle: int = 0,
        horizontal_angle: int = 0,
        back_view: bool = False
    ) -> Dict[str, Any]:
        """
        Submit a Satellite View segmentation task
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            vertical_angle: Vertical viewing angle (tilt up/down)
            horizontal_angle: Horizontal viewing angle (pan left/right, 0-360)
            back_view: Whether to capture back view
        
        Returns:
            Dictionary with activity_id to track task status
        """
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "vertical_angle": vertical_angle,
            "horizontal_angle": horizontal_angle,
            "back_view": back_view
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/satellite",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "activity_id": response.json().get("data", {}).get("activity_id"),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"Error {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def check_task_status(self, activity_id: str) -> Dict[str, Any]:
        """
        Check status of a submitted task (satellite view, etc.)
        
        Args:
            activity_id: The activity ID returned from task submission
        
        Returns:
            Dictionary with task status and results if completed
        """
        try:
            response = requests.get(
                f"{self.base_url}/status/{activity_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"Error {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def poll_task_until_complete(
        self,
        activity_id: str,
        max_polls: int = 120,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """
        Poll task status until it completes or times out
        
        Args:
            activity_id: The activity ID to poll
            max_polls: Maximum number of poll attempts
            poll_interval: Seconds to wait between polls
        
        Returns:
            Final task status and results
        """
        print(f"Starting to poll activity {activity_id}...")
        
        for attempt in range(max_polls):
            result = self.check_task_status(activity_id)
            
            if not result.get("success"):
                return result
            
            status = result["data"].get("data", {}).get("status", "unknown")
            print(f"Attempt {attempt + 1}/{max_polls}: Status = {status}")
            
            if status == "Completed":
                print("✅ Task completed!")
                return result
            elif status == "Failed":
                print("❌ Task failed!")
                return result
            elif status == "Processing":
                print(f"⏳ Processing... waiting {poll_interval}s")
                time.sleep(poll_interval)
            else:
                print(f"⏳ Status: {status}, waiting {poll_interval}s")
                time.sleep(poll_interval)
        
        return {
            "success": False,
            "error": f"Task did not complete within {max_polls * poll_interval} seconds"
        }


if __name__ == "__main__":
    # Example usage
    API_KEY = "YOUR_API_KEY_HERE"
    
    # Initialize client
    client = FortGuardClient(API_KEY)
    
    # Example: Fetch environmental parameters for San Francisco
    print("=" * 60)
    print("EXAMPLE 1: Fetch Environmental Parameters")
    print("=" * 60)
    
    env_result = client.fetch_environmental_parameters(
        latitude=37.7749,
        longitude=-122.4194,
        temperature=22.5,
        start_date="2024-07-15",
        parameters=["heat_index_celsius", "relative_humidity_percent"]
    )
    print(json.dumps(env_result, indent=2))
    
    # Example: Submit satellite view task
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Submit Satellite View Task")
    print("=" * 60)
    
    sat_result = client.submit_satellite_view_task(
        latitude=37.7749,
        longitude=-122.4194
    )
    print(json.dumps(sat_result, indent=2))
    
    # If successful, poll the task
    if sat_result.get("success") and sat_result.get("activity_id"):
        print("\n" + "=" * 60)
        print("EXAMPLE 3: Poll Task Status")
        print("=" * 60)
        
        completion_result = client.poll_task_until_complete(
            sat_result["activity_id"],
            max_polls=20,
            poll_interval=3
        )
        print(json.dumps(completion_result, indent=2))
