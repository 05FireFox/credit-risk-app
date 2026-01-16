import streamlit as st
from utils import predict

st.set_page_config(page_title="Credit Risk App", page_icon="📊")
st.title("📊 Credit Risk Assessment")

# Inputs
st.subheader("Customer Info")
col1, col2 = st.columns(2)
age = col1.number_input("Age", 18, 100, 30)
income = col2.number_input("Annual Income", 0, value=500000)

st.subheader("Loan Info")
col3, col4 = st.columns(2)
loan_amount = col3.number_input("Loan Amount", 0, value=100000)
loan_tenure = col4.slider("Loan Tenure (Months)", 6, 240, 36)

st.subheader("Financial History")
credit_util = st.slider("Credit Utilization %", 0, 100, 30)
avg_dpd = st.number_input("Avg Days Past Due", 0, value=0)
total_loans = st.number_input("Total Loan Months History", 0, value=12)

st.subheader("Loan Details")
purpose = st.selectbox("Purpose", ['Education', 'Home', 'Auto', 'Personal'])
l_type = st.radio("Type", ['Unsecured', 'Secured'])
res_type = st.selectbox("Residence", ['Owned', 'Rented', 'Mortgage'])

if st.button("Calculate Risk"):
    # We pass 0 for dmtlm to keep it simple, or you can add an input for it
    prob, score, rating = predict(age, avg_dpd, credit_util, 0, income,
                                  loan_amount, loan_tenure, total_loans,
                                  purpose, l_type, res_type)

    st.success("Risk Calculated!")
    st.metric("Default Probability", f"{prob:.2%}")
    st.metric("Credit Score", score)
    st.write(f"**Rating:** {rating}")