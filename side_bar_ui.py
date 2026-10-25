import streamlit as st

def render_side_bar():
    st.sidebar.header("Your Financial Profile")
    
    input_mode = st.sidebar.radio("Select Input Mode", ["Slider", "Number Input"])
    
    # --- REPLACE pre_tax = st.sidebar.radio(...) WITH THESE TWO LINES ---
    income_type_selection = st.sidebar.radio("Income Type (the specific tax values may vary)", ["Before Tax", "After Tax"])
    pre_tax = True if income_type_selection == "Before Tax" else False
   

    salary_mode = st.sidebar.radio("Salary Period", ["Monthly", "Yearly"])

    # Initialize master session state for smooth syncing
    if "salary_monthly" not in st.session_state:
        st.session_state.salary_monthly = 5000

    # Handle Monthly vs Yearly UI cleanly without breaking widget states
    if salary_mode == "Monthly":
        current_val = int(st.session_state.salary_monthly)
        if input_mode == "Slider":
            salary = st.sidebar.slider("Monthly Salary", min_value=0, max_value=20000, value=current_val, step=100)
        else:
            salary = st.sidebar.number_input("Monthly Salary", min_value=0, max_value=10000000, value=current_val, step=100)
        
        # Save back to master state
        st.session_state.salary_monthly = salary
    else:
        current_yearly = int(st.session_state.salary_monthly * 12)
        if input_mode == "Slider":
            yearly_salary = st.sidebar.slider("Yearly Salary", min_value=0, max_value=240000, value=current_yearly, step=500)
        else:
            yearly_salary = st.sidebar.number_input("Yearly Salary", min_value=0, max_value=120000000, value=current_yearly, step=500)
        
        # Convert yearly down to monthly for calculations and update master state
        st.session_state.salary_monthly = yearly_salary / 12
        salary = st.session_state.salary_monthly

    # Additional inputs
    if input_mode == "Slider":
        item_cost = st.sidebar.slider("Target Item Cost", min_value=0, max_value=100000, value=30000, step=500)
    else:
        item_cost = st.sidebar.number_input("Target Item Cost", min_value=0, max_value=100000, value=30000, step=500)
    currency = st.sidebar.selectbox("Currency", ["CAD", "USD", "EUR", "GBP"])
   
   

   
    # --- DASHBOARD METRIC CARDS ---
    st.markdown("### Financial Overview")

    # Create 3 side-by-side columns
    col1, col2, col3 = st.columns(3)

    with col1:
    # Dynamically check salary mode to display Yearly vs Monthly properly
        if salary_mode == "Yearly":
            yearly_display = salary * 12  # Bring it back to the annual figure
            st.metric(
                label="Yearly Income", 
                value=f"{yearly_display:,.0f} {currency}"
            )
        else:
            st.metric(
                label="Monthly Income", 
                value=f"{salary:,.0f} {currency}"
            )
    with col2:
        # Display the target goal cost
        st.metric(
            label="Target Item Cost", 
            value=f"{item_cost:,.0f} {currency}"
        )
    with col3:
        # Display whether it's pre-tax or post-tax
        tax_label = "Before Tax" if pre_tax else "After Tax"
        st.metric(
            label="Tax Mode", 
            value=tax_label
        )

    st.divider()  # Adds a clean horizontal line separating metrics from the AI insights
        
        
        # CRITICAL: Return everything back to app.py!
    return salary, item_cost, currency, pre_tax, salary_mode