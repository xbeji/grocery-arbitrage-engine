import firebase_admin
from firebase_admin import credentials, firestore
import pulp
import pandas as pd
import matplotlib.pyplot as plt

# Connect to Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

MY_SHOPPING_LIST = ["Milk", "Eggs", "Chicken", "Rice"]
FIXED_GAS_A = 5.0 # Supermarket A is always close

def get_data():
    docs = db.collection('grocery_prices').stream()
    prices = {}
    stores = set()
    for doc in docs:
        d = doc.to_dict()
        if d['item'] in MY_SHOPPING_LIST:
            if d['item'] not in prices: prices[d['item']] = {}
            prices[d['item']][d['store']] = d['price']
            stores.add(d['store'])
    return prices, list(stores)

def run_simulation(variable_gas_cost, prices, stores):
    prob = pulp.LpProblem("Sim", pulp.LpMinimize)
    buy = pulp.LpVariable.dicts("buy", ((i, s) for i in MY_SHOPPING_LIST for s in stores), cat='Binary')
    visit = pulp.LpVariable.dicts("visit", stores, cat='Binary')
    
    # Objective
    # We test changing the gas cost for Supermarket B (the far one)
    prob += sum(prices[i][s] * buy[(i, s)] for i in MY_SHOPPING_LIST for s in stores) + \
            sum(visit[s] * (FIXED_GAS_A if s == "Supermarket A" else variable_gas_cost) for s in stores)

    # Constraints
    for i in MY_SHOPPING_LIST: prob += sum(buy[(i, s)] for s in stores) == 1
    for s in stores:
        for i in MY_SHOPPING_LIST: prob += buy[(i, s)] <= visit[s]
            
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # Return 1 if we visited Supermarket B, 0 if not
    # Use .get() to avoid errors if Supermarket B isn't in the list for some reason
    visit_b_val = visit['Supermarket B'].varValue if 'Supermarket B' in visit else 0
    return visit_b_val, pulp.value(prob.objective)

# --- RUN THE LOOP ---
prices, stores = get_data()
results = []

print("Running simulation on 30 gas price scenarios for Supermarket B...")
for gas in range(0, 31):
    visited_b, total_cost = run_simulation(gas, prices, stores)
    results.append({"Gas_Cost_B": gas, "Total_Bill": total_cost, "Went_To_B": visited_b})

df = pd.DataFrame(results)

# Plotting

plt.figure(figsize=(10, 6))
plt.plot(df['Gas_Cost_B'], df['Total_Bill'], marker='o', color='green')
plt.title("Impact of Distance on Strategy (Supermarket A vs B)")
plt.xlabel("Cost to Drive to Supermarket B (SAR)")
plt.ylabel("Total Shopping Bill (SAR)")
plt.grid(True)

# Find the tipping point (Where we stopped going to Supermarket B)
changes = df[df['Went_To_B'].diff() != 0]
if len(changes) > 1:
    tipping_point = changes.iloc[1]['Gas_Cost_B']
    plt.axvline(x=tipping_point, color='red', linestyle='--', label=f'Tipping Point ({tipping_point} SAR)')
    plt.legend()
    print(f"The Strategy shifts when Supermarket B Gas Price hits {tipping_point} SAR")

plt.show()