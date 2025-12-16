import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# 1. Connect to 'cproject'
# Ensure 'serviceAccountKey.json' is in the same folder
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Define the Mock Data
# Supermarket A = Close, Expensive
# Supermarket B = Far, Cheap
market_data = [
    # Store A (Close, Standard Prices)
    {"item": "Milk", "store": "Supermarket A", "price": 8.00},
    {"item": "Eggs", "store": "Supermarket A", "price": 22.00},
    {"item": "Chicken", "store": "Supermarket A", "price": 18.00},
    {"item": "Rice", "store": "Supermarket A", "price": 35.00},

    # Store B (Far, Cheaper Prices)
    {"item": "Milk", "store": "Supermarket B", "price": 7.50},    # Cheaper
    {"item": "Eggs", "store": "Supermarket B", "price": 18.00},   # Much Cheaper
    {"item": "Chicken", "store": "Supermarket B", "price": 16.50}, # Cheaper
    {"item": "Rice", "store": "Supermarket B", "price": 34.00},
]

# 3. Upload loop
collection_name = 'grocery_prices'
print(f"Uploading data to Firestore project: cproject...")

for data in market_data:
    # Create a unique ID (e.g., 'SupermarketA_Milk')
    # replace spaces with underscores for clean IDs
    clean_store_name = data['store'].replace(" ", "")
    doc_id = f"{clean_store_name}_{data['item']}"
    
    # Add timestamp
    data['last_updated'] = datetime.now()
    
    # Send to cloud
    db.collection(collection_name).document(doc_id).set(data)
    print(f"Stored: {data['item']} at {data['store']}")

print("\nSuccess! Data is now in the Cloud.")
