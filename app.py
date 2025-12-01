import streamlit as st
import pandas as pd
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(page_title="FinCoach AI", layout="centered", initial_sidebar_state="expanded")
st.title("FinCoach AI")
st.markdown("#### Your real-time AI personal finance coach – built for everyone")

# Permanent ethics banner
st.markdown(
    """
    <div style='background-color:#FF9800;padding:10px;border-radius:10px;text-align:center;'>
    <strong>Ethics & Transparency Notice:</strong> Advice is AI-generated and for educational purposes only. 
    Not personalized investment advice. We perform quarterly bias audits. Consult a licensed advisor for complex decisions.
    </div>
    """, unsafe_allow_html=True
)

# ========================= MOCK DATA – GUARANTEED TO ALWAYS SHOW UP =========================
if "transactions" not in st.session_state:
    # Force all transactions into the CURRENT REAL MONTH so they are NEVER filtered out
    from datetime import datetime, timedelta
    today = datetime.now()  # Uses your actual computer date TODAY

    st.session_state.transactions = pd.DataFrame([
        {"date": today - timedelta(days=1), "description": "Starbucks",          "amount": -19.50, "category": "Food & Dining"},
        {"date": today - timedelta(days=2), "description": "Chipotle",           "amount": -26.80, "category": "Food & Dining"},
        {"date": today - timedelta(days=3), "description": "Whole Foods",         "amount": -112.40,"category": "Groceries"},
        {"date": today - timedelta(days=4), "description": "Uber Eats",           "amount": -38.20, "category": "Food & Dining"},
        {"date": today - timedelta(days=5), "description": "Netflix",            "amount": -15.99, "category": "Entertainment"},
        {"date": today - timedelta(days=6), "description": "Amazon",             "amount": -89.70, "category": "Shopping"},
        {"date": today - timedelta(days=10),"description": "Salary Deposit",     "amount": 4000,   "category": "Income"},
    ])
    st.session_state.goal = "Save $500/month"
    st.session_state.risk = "Moderate"

# ========================= SIDEBAR =========================
with st.sidebar:
    st.header("User Profile")
    st.info("Connected via Plaid Sandbox")
    income = st.number_input("Monthly Income ($)", value=4000, step=500, key="income")  # Now used dynamically
    st.selectbox("Primary Goal", ["Save $500/month", "Pay off debt", "Build emergency fund", "Invest more"], key="goal")
    st.radio("Risk Profile", ["Conservative", "Moderate", "Aggressive"], key="risk")
    
    st.markdown("---")
    st.markdown("### Language / Idioma")
    lang = st.selectbox("Select", ["English", "Español"], index=0)

# ========================= MAIN DASHBOARD (Now Dynamic!) =========================
df = st.session_state.transactions.copy()
df['date'] = pd.to_datetime(df['date'])

# NEW: Always count transactions from the last 30 days — works forever
from datetime import datetime, timedelta
cutoff_date = datetime.now() - timedelta(days=30)
current_month = df['date'] >= cutoff_date

# Dynamic calculations
total_spent = abs(df[current_month & (df['amount'] < 0)]['amount'].sum())
food_spent = abs(df[current_month & df['category'].str.contains("Food|Groceries") & (df['amount'] < 0)]['amount'].sum())
food_budget = 200  # Realistic budget (tweak to 6 for exact screenshot match, but 200 is better)
food_delta = food_spent - food_budget
savings_rate = round(((income - total_spent) / income * 100), 1) if income > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Spent (Dec)", f"${total_spent:,.0f}")
with col2:
    st.metric("Food & Dining", f"${food_spent:.0f}", delta=f"${food_delta:+.0f} vs budget")
with col3:
    st.metric("Current Savings Rate", f"{savings_rate}%", delta=f"↑ {savings_rate-10:.0f}%")  # Example delta

st.divider()

# ========================= AI COACH CHAT (Unchanged) =========================
st.subheader("Ask Your AI Coach Anything")
user_q = st.text_input(
    "",
    placeholder="e.g., Why am I overspending on food? | ¿Por qué gasto tanto en comida?" if lang == "English" else "ej. ¿Por qué gasto tanto en comida?"
)

if user_q:
    with st.spinner("Thinking…"):
        q = user_q.lower()
        if "food" in q or "comida" in q:
            response = f"You're currently spending **${food_spent}** on food this month (budget was ${food_budget}). Try meal-prepping on Sundays — our users save an average of 31% doing this. Want me to create a new ${food_budget} food budget?"
        elif "save" in q or "ahorrar" in q:
            response = f"With your ${income:,} income and current spending, you can easily save **${savings_rate}%/month** ({(income * savings_rate / 100):.0f}). I recommend auto-investing ${(income * 0.15):.0f} into VTI."
        elif "invest" in q or "invertir" in q:
            response = "Moderate risk profile → recommended allocation: 60% stocks (VTI), 30% bonds (BND), 10% cash. Start with 15% of income recurring?"
        else:
            response = "I'm learning every day! Try asking about food, savings, or investment questions."
        
        if lang == "Español":
            # Simple mock translations (expand as needed)
            response = response.replace("Try meal-prepping", "Prueba preparar comidas los domingos")
        
        st.success(response)

# ========================= ONE-TAP BUDGET OPTIMIZER (Now Uses Income) =========================
st.subheader("One-Tap Budget Re-Optimization")
if st.button("Generate Optimized Budget Now", type="primary"):
    savings_target = income * 0.15  # 15% of income to savings
    new_budget = {
        "Groceries": food_budget,
        "Dining Out": 80,
        "Transport": 120,
        "Entertainment": 80,
        "Savings/Investing": savings_target
    }
    st.json(new_budget)
    st.balloons()
    st.success(f"New budget applied! You're now on track to save **${savings_target:.0f}/month** ({savings_rate:.0f}% rate)")

# ========================= MICRO-INVESTMENT SUGGESTION (Unchanged) =========================
st.subheader("Today's Micro-Investment Idea")
if st.session_state.risk == "Conservative":
    idea = f"High-yield savings at 5.1% APY → ${income * 0.05:.0f}/month"
elif st.session_state.risk == "Moderate":
    idea = f"VTI (Total Stock Market ETF) → recurring ${income * 0.075:.0f}/month"
else:
    idea = f"QQQ (Nasdaq-100) + small allocation to Bitcoin ETF → ${income * 0.1:.0f}/month"

st.info(f"**Risk profile: {st.session_state.risk}**  \nRecommended: {idea}")

st.caption("FinCoach AI © 2025 | Ramon • Jorge • Nathaly | FIN 6778 Final Project")