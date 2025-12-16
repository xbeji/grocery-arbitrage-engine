import firebase_admin
from firebase_admin import credentials, firestore
import pulp

# Connect to Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- THE USER INPUT ---
MY_SHOPPING_LIST = ["Milk", "Eggs", "Chicken", "Rice"]

# Real-world Constraint: Gas & Time Cost
# Supermarket A is close (5 SAR to drive there)
# Supermarket B is far (15 SAR to drive there)
COST_TO_DRIVE_A = 5.0
COST_TO_DRIVE_B = 15.0 

def solve_logistics():
    # 1. Download Data
    print("Fetching live prices from Firestore...")
    docs = db.collection('grocery_prices').stream()
    
    prices = {}
    stores = set()
    
    # Organize data
    for doc in docs:
        data = doc.to_dict()
        if data['item'] in MY_SHOPPING_LIST:
            if data['item'] not in prices: prices[data['item']] = {}
            prices[data['item']][data['store']] = data['price']
            stores.add(data['store'])

    # 2. Setup Linear Programming
    prob = pulp.LpProblem("Shopping_Optimizer", pulp.LpMinimize)

    # Variables
    # buy[item, store]: Should I buy Item I at Store S? (1 = Yes, 0 = No)
    buy = pulp.LpVariable.dicts("buy", ((i, s) for i in MY_SHOPPING_LIST for s in stores), cat='Binary')
    
    # visit[store]: Should I visit Store S? (1 = Yes, 0 = No)
    visit = pulp.LpVariable.dicts("visit", stores, cat='Binary')

    # Objective: Minimize (Item Costs + Gas Costs)
    item_cost = sum(prices[i][s] * buy[(i, s)] for i in MY_SHOPPING_LIST for s in stores)
    
    # Dynamic gas cost assignment
    gas_cost = sum(visit[s] * (COST_TO_DRIVE_A if s == "Supermarket A" else COST_TO_DRIVE_B) for s in stores)
    
    prob += item_cost + gas_cost

    # Constraints
    # A. Must buy every item once
    for i in MY_SHOPPING_LIST:
        prob += sum(buy[(i, s)] for s in stores) == 1
    
    # B. If I buy at a store, I must visit it
    for s in stores:
        for i in MY_SHOPPING_LIST:
            prob += buy[(i, s)] <= visit[s]

    # 3. Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # 4. Print Report
    print("-" * 40)
    print(f"OPTIMAL STRATEGY (Total Cost: {pulp.value(prob.objective)} SAR)")
    print("-" * 40)
    
    for s in stores:
        if visit[s].varValue == 1:
            current_gas = COST_TO_DRIVE_A if s == 'Supermarket A' else COST_TO_DRIVE_B
            print(f"Go to {s} (Gas Cost: {current_gas} SAR):")
            for i in MY_SHOPPING_LIST:
                if buy[(i, s)].varValue == 1:
                    print(f"  - Buy {i} ({prices[i][s]} SAR)")
            print("")

if __name__ == "__main__":
    solve_logistics()