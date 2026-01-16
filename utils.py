import joblib
import pandas as pd
import streamlit as st

# 1. LOAD THE MODEL
# This line looks for the file you pasted in Step 3
try:
    model_data = joblib.load("model/model_data.pkl")
except FileNotFoundError:
    st.error("Error: Could not find 'model/model_data.pkl'. Did you paste the file correctly?")
    st.stop()

model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
columns_to_scale = model_data['cols_to_scale']

# 2. PREPARE DATA FUNCTION
def data_preparation(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
                     loan_amount, loan_tenure_months, total_loan_months, 
                     loan_purpose, loan_type, residence_type):

    # Calculate Loan-to-Income ratio
    lti = loan_amount / income if income > 0 else 0

    # Create the dictionary of data
    data_input = {
        'age': age,
        'avg_dpd_per_dm': avg_dpd_per_dm,
        'credit_utilization_ratio': credit_utilization_ratio,
        'dmtlm': dmtlm,
        'income': income,
        'loan_amount': loan_amount,
        'lti': lti,
        'total_loan_months': total_loan_months,
        'loan_tenure_months': loan_tenure_months,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0
    }

    # Convert to DataFrame and fill missing columns with 0
    df = pd.DataFrame([data_input])
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Scale the columns
    df[columns_to_scale] = scaler.transform(df[columns_to_scale])
    df = df[features]
    return df

# 3. PREDICT FUNCTION
def predict(age, avg_dpd, credit_util, dmtlm, income, 
            loan_amt, loan_tenure, total_loans, 
            purpose, l_type, res_type):

    input_df = data_preparation(age, avg_dpd, credit_util, dmtlm, income, 
                                loan_amt, loan_tenure, total_loans, 
                                purpose, l_type, res_type)

    prob = model.predict_proba(input_df)[:, 1][0]

    # Calculate Score (300 to 900 scale)
    score = 300 + (1 - prob) * 600

    # Determine Rating
    if score < 500: rating = 'Poor'
    elif score < 650: rating = 'Average'
    elif score < 750: rating = 'Good'
    else: rating = 'Excellent'

    return prob, int(score), rating