# Green House Gas Emission Prediction  
### Supply Chain Emission Factor Modeling (2010–2016)

This project predicts **Supply Chain Emission Factors with Margins** using U.S. industry and commodity datasets from **2010–2016**. A **Random Forest Regressor** is trained on substance types, measurement units, sources, and data-quality indicators to estimate greenhouse gas emissions.
## 🎯 Objective

Predict GHG emission factors using:

- Substance type (CO₂, CH₄, N₂O, etc.)  
- Measurement unit  
- Data source (Industry / Commodity)  
- Quality indicators (reliability, correlation type)

---

## 🔍 Workflow Summary

### **1. Data Loading**
- Combined yearly Excel sheets (2010–2016)
- Standardized column names  
- Removed IDs and non-predictive metadata  

### **2. Preprocessing**
- Missing value handling  
- Label encoding for categorical features  
- Train-test split  
- Feature scaling  

### **3. EDA**
- Distribution analysis  
- Substance-level comparisons  
- Correlation heatmap  

### **4. Modeling**
- Random Forest Regressor  
- Hyperparameter tuning using GridSearchCV  
- Evaluation with RMSE and R²  

### **5. Output Files**
- `models/final_model.pkl` – trained Random Forest model  
- `models/scaler.pkl` – fitted scaler  

---

## ⚙️ Requirements

Install all required packages:
```bash
pip install pandas numpy seaborn matplotlib scikit-learn joblib openpyxl flask
```
## How to Run the Entire Project
### Step 1: Clone or Download the Project
```bash
git clone https://github.com/your-repo-url.git
cd Green_House_Gas_Emmision_Prediction
```
### Step 2: Move into the Backend Folder
```bash
cd backend
```
### Step 3: Verify Model Files

Ensure the following exist:

backend/models/final_model.pkl
backend/models/scaler.pkl


If they are missing, run the training notebook inside:

backend/notebooks/

### Step 4: Start the Backend Server

Run:
```bash
python app.py
```

You should see:

Running on http://127.0.0.1:5000

This means the prediction API is live.

### Step 5: Open the Frontend (UI)

Open this file in any browser:

frontend/index.html
