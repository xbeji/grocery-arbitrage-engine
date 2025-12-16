# 🛒 Grocery Arbitrage Engine

A Business Analytics tool that uses Linear Programming to solve the "Travelling Purchaser Problem" for household logistics.

# 📌 Overview

Inflation is real, and gas prices vary. The Grocery Arbitrage Engine answers a complex question: "Is it worth driving 20 minutes to a cheaper store, or should I just buy everything at the expensive store next door?"

Instead of guessing, this project uses Mixed-Integer Linear Programming (MILP) to calculate the mathematically optimal shopping strategy. It balances Product Costs (Milk, Eggs, etc.) against Logistics Costs (Gas, Time, Vehicle Wear) to minimize total expenditure.

# 🚀 Key Features

- Cloud-Native Storage: Uses Google Firebase (Firestore) to store and retrieve real-time pricing data from multiple vendors.
- Optimization Algorithm: Implements the PuLP library to solve minimization problems with binary constraints.
- Sensitivity Analysis: Includes a simulation module that iterates through 30+ gas price scenarios to identify the exact "Tipping Point" where a shopping strategy becomes unviable.
- Data Visualization: Generates trend lines using Matplotlib to visualize the impact of logistics costs on purchasing decisions.

# 🛠️ Tech Stack

- Language: Python 3.x
- Database: Google Firebase (Firestore NoSQL)
- Libraries:
  - PuLP: For Linear Programming optimization.
  - firebase-admin: For database connectivity.
  - pandas: For data structuring and analysis.
  - matplotlib: For visualizing the sensitivity analysis.

# 📂 Project Structure

```
grocery-arbitrage-engine/
│
├── 1_upload_data.py        # ETL Script: Uploads mock pricing data to Firebase
├── 2_optimize.py           # Core Engine: Calculates the optimal shopping list
├── 3_analyze.py            # Analytics: Runs sensitivity simulation & graphs
├── serviceAccountKey.json  # (IGNORED) Your Firebase API Key DO NOT COMMIT THIS
├── README.md               # Documentation
└── requirements.txt        # Python dependencies
```

# ⚙️ Installation & Setup
```
1. Clone the Repository
git clone https://github.com/xbeji/grocery-arbitrage-engine.git
cd grocery-arbitrage-engine
```

2. Install Dependencies
```pip install firebase-admin pulp pandas matplotlib```

3. Firebase Configuration
  - Go to the Firebase Console.
  - Create a new project.
  - Navigate to Project Settings > Service Accounts.
  - Generate a New Private Key.
  - Download the .json file, rename it to serviceAccountKey.json, and place it in the project root.
Note: Ensure this file is added to your .gitignore so you don't expose your keys.

# 🏃‍♂️ Usage

Step 1: Seed the Database
Run the upload script to populate Firestore with sample data for "Supermarket A" (Close/Expensive) and "Supermarket B" (Far/Cheap).

```python 1_upload_data.py```


Step 2: Run the Optimizer
Calculate the best shopping strategy based on current parameters.

```python 2_optimize.py```


Output Example:

OPTIMAL STRATEGY (Total Cost: 91.50 SAR)
Go to Supermarket B: Buy Eggs, Chicken, Rice
Go to Supermarket A: Buy Milk

Step 3: Run Sensitivity Analysis
Visualize how rising gas costs impact the decision.

```python 3_analyze.py```


This will open a graph showing the "Tipping Point" where the strategy shifts.

# 📊 Business Logic

The model minimizes $Z$ (Total Cost):

$$Minimize \ Z = \sum (P_{ij} \times X_{ij}) + \sum (C_j \times Y_j)$$

Where:

$P_{ij}$ = Price of item $i$ at store $j$

$X_{ij}$ = Binary variable (1 if we buy item $i$ at store $j$)

$C_j$ = Gas/Travel cost to visit store $j$

$Y_j$ = Binary variable (1 if we visit store $j$)

📝 License

This project is open-source and available under the MIT License.
