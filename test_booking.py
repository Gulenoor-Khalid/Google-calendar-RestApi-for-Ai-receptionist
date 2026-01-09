import requests
import json
from datetime import datetime, timedelta

# Test the calendar booking functionality
def test_appointment_booking():
    base_url = "http://127.0.0.1:5000"
    
    # Calculate test times (1 hour from now)
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    # Format for Google Calendar API
    start_iso = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Test appointment data
    appointment_data = {
        "summary": "Test Dental Appointment",
        "start_time": start_iso,
        "end_time": end_iso
    }
    
    print(f"Testing appointment booking...")
    print(f"Appointment: {appointment_data['summary']}")
    print(f"Start: {start_iso}")
    print(f"End: {end_iso}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{base_url}/add_event",
            headers={"Content-Type": "application/json"},
            json=appointment_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Event created: {result.get('eventLink', 'No link provided')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask app. Make sure it's running on port 5000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_appointment_booking()