"""
API Testing Script for Basey Fare Guide
Demonstrates how to use the API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'
AUTH_URL = 'http://localhost:8000/api/auth'

class BFGAPITester:
    def __init__(self):
        self.token = None
        self.user = None
    
    def register_user(self, username, email, password, first_name, last_name):
        """Register a new user"""
        print(f"\n📝 Registering user: {username}")
        response = requests.post(f'{AUTH_URL}/register/', json={
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        })
        
        if response.status_code == 201:
            data = response.json()
            self.token = data['tokens']['access']
            self.user = data['user']
            print(f"✅ User registered: {self.user['username']}")
            print(f"🔑 Token: {self.token[:50]}...")
            return data
        else:
            print(f"❌ Registration failed: {response.json()}")
            return None
    
    def login(self, username, password):
        """Login and get JWT token"""
        print(f"\n🔐 Logging in as: {username}")
        response = requests.post(f'{AUTH_URL}/login/', json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['tokens']['access']
            self.user = data['user']
            print(f"✅ Logged in: {self.user['username']}")
            print(f"🔑 Token: {self.token[:50]}...")
            return data
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    
    def get_headers(self):
        """Get authorization headers"""
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def get_locations(self):
        """Get all locations"""
        print("\n📍 Fetching locations...")
        response = requests.get(f'{BASE_URL}/locations/')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['count']} locations")
            for loc in data['results'][:3]:
                print(f"   - {loc['name']} ({loc['type']})")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None
    
    def calculate_fare(self, origin, destination):
        """Calculate fare between two coordinates"""
        print(f"\n💰 Calculating fare...")
        print(f"   Origin: {origin}")
        print(f"   Destination: {destination}")
        
        response = requests.post(f'{BASE_URL}/routes/calculate/', json={
            'origin': origin,
            'destination': destination,
            'use_google_maps': False  # Use GPS fallback for demo
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Calculation complete!")
            print(f"   Method: {data['method']}")
            print(f"   Distance: {data['distance']['kilometers']:.2f} km")
            print(f"   Fare: ₱{data['fare']['fare']:.2f}")
            if data['fare']['discount_applied'] > 0:
                print(f"   Original Fare: ₱{data['fare']['original_fare']:.2f}")
                print(f"   Discount: -₱{data['fare']['discount_applied']:.2f}")
            print(f"   Breakdown:")
            print(f"     Base Fare: ₱{data['fare']['breakdown']['base_fare']:.2f}")
            print(f"     Additional Distance: {data['fare']['breakdown']['additional_distance_km']:.2f} km")
            print(f"     Additional Fare: ₱{data['fare']['breakdown']['additional_fare']:.2f}")
            return data
        else:
            print(f"❌ Failed: {response.json()}")
            return None
    
    def get_my_fare_history(self):
        """Get fare calculation history"""
        print("\n📊 Fetching fare calculation history...")
        response = requests.get(
            f'{BASE_URL}/fare-calculations/',
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['count']} calculations")
            for calc in data['results'][:3]:
                print(f"   - {calc['from_location']} → {calc['to_location']}: ₱{calc['calculated_fare']}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None
    
    def report_incident(self, incident_type, description, location):
        """Report an incident"""
        print(f"\n🚨 Reporting incident...")
        response = requests.post(
            f'{BASE_URL}/incidents/',
            headers=self.get_headers(),
            json={
                'incident_type': incident_type,
                'description': description,
                'location': location,
                'gps_coordinates': {'lat': 11.28026, 'lng': 125.06909},
                'vehicle_info': {
                    'plate_number': 'ABC-1234',
                    'type': 'Tricycle',
                    'color': 'Blue'
                },
                'status': 'PENDING',
                'priority': 'MEDIUM'
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Incident reported: #{data['id']}")
            print(f"   Type: {data['incident_type']}")
            print(f"   Status: {data['status']}")
            return data
        else:
            print(f"❌ Failed: {response.json()}")
            return None


def main():
    """Main test function"""
    print("=" * 70)
    print("🚀 BASEY FARE GUIDE - API TESTING")
    print("=" * 70)
    
    tester = BFGAPITester()
    
    # Test 1: Login
    tester.login('testuser', 'test123')
    
    # Test 2: Get locations
    tester.get_locations()
    
    # Test 3: Calculate fare (Basey Center to Basiao)
    # Coordinates from sample data
    center_coords = [11.28026, 125.06909]
    basiao_coords = [11.2768363, 125.0114879]
    tester.calculate_fare(center_coords, basiao_coords)
    
    # Test 4: Calculate another fare
    bacubac_coords = [11.3012, 125.0823]
    tester.calculate_fare(center_coords, bacubac_coords)
    
    # Test 5: Report incident
    tester.report_incident(
        'OVERCHARGING',
        'Driver charged ₱30 instead of ₱24 for standard route',
        'Basey Public Market'
    )
    
    print("\n" + "=" * 70)
    print("✅ API TESTING COMPLETE")
    print("=" * 70)
    print("\n💡 Tips:")
    print("   - Admin panel: http://localhost:8000/admin/")
    print("   - API root: http://localhost:8000/api/")
    print("   - Login: admin / admin123")
    print("\n📚 Available Endpoints:")
    print("   GET  /api/locations/")
    print("   GET  /api/routes/")
    print("   POST /api/routes/calculate/")
    print("   GET  /api/fare-calculations/")
    print("   POST /api/incidents/")
    print("   GET  /api/discount-cards/")
    print("   POST /api/auth/login/")
    print("   POST /api/auth/register/")
    print()


if __name__ == '__main__':
    # Check if server is running
    try:
        response = requests.get('http://localhost:8000/api/')
        if response.status_code == 200:
            main()
        else:
            print("⚠️  Server not responding correctly")
            print("   Please run: python manage.py runserver")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("   Please run: python manage.py runserver")
        print("   Then run this script again")
