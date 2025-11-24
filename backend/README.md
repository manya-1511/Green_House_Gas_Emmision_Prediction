📦 Supply Chain Emissions Modeling (2010–2016)
This project predicts Supply Chain Emission Factors with Margins using US industry and commodity data from 2010 to 2016. It uses a Random Forest Regressor trained on various descriptive and quality metrics.

🔍 Objective
Predict GHG emission factors using features like:

Substance type (CO₂, CH₄, etc.)

Measurement unit

Source (Industry vs. Commodity)

Data quality indicators (reliability, correlation types)

🧰 Workflow Summary
Data Loading: Combined yearly Excel sheets (2010–2016)

Preprocessing: Cleaned columns, mapped categories, dropped IDs

EDA: Distribution plots & correlation heatmap

Modeling: Random Forest with GridSearchCV

Evaluation: RMSE & R² on test data

Export: Saved model and scaler with joblib

📁 Output
models/final_model.pkl – Trained model

models/scaler.pkl – Feature scaler

⚙️ Requirements

pip install pandas numpy seaborn matplotlib scikit-learn joblib openpyxl
