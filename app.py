import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE SETTINGS ----------

st.set_page_config(
    page_title="CashPilota AI",
    page_icon="💰",
    layout="wide"
)

# ---------- SESSION DATA ----------

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ---------- CUSTOM UI ----------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------

st.markdown(
    '<div class="main-title">💰 CashPilota AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart Personal Finance Assistant</div>',
    unsafe_allow_html=True
)

# ---------- SIDEBAR ----------

st.sidebar.title("⚙️ Finance Controls")

st.sidebar.subheader("➕ Add Transaction")

transaction_type = st.sidebar.selectbox(
    "Transaction Type",
    ["Income", "Expense"]
)

amount = st.sidebar.number_input(
    "Amount (₹)",
    min_value=0.0,
    step=100.0
)

category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Education", "Bills", "Other"]
)

if st.sidebar.button("Add Transaction", use_container_width=True):

    if amount > 0:

        st.session_state.transactions.append(
            {
                "Type": transaction_type,
                "Amount": amount,
                "Category": category
            }
        )

        st.sidebar.success("Transaction added!")

    else:

        st.sidebar.warning("Enter an amount greater than 0.")

# ---------- BUDGET ----------

st.sidebar.subheader("🎯 Monthly Budget")

budget = st.sidebar.number_input(
    "Budget (₹)",
    min_value=0.0,
    step=500.0
)

# ---------- DATA ----------

df = pd.DataFrame(st.session_state.transactions)

# ---------- DASHBOARD ----------

if not df.empty:

    income = df.loc[
        df["Type"] == "Income",
        "Amount"
    ].sum()

    expense = df.loc[
        df["Type"] == "Expense",
        "Amount"
    ].sum()

    balance = income - expense

    # ---------- METRICS ----------

    st.markdown(
        '<div class="section-title">📊 Financial Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Income",
        f"₹{income:,.0f}"
    )

    col2.metric(
        "💸 Expenses",
        f"₹{expense:,.0f}"
    )

    col3.metric(
        "💰 Balance",
        f"₹{balance:,.0f}"
    )

    if budget > 0:
        remaining = budget - expense

        col4.metric(
            "🎯 Budget Left",
            f"₹{remaining:,.0f}"
        )
    else:
        col4.metric(
            "🎯 Budget",
            "Not Set"
        )

    # ---------- BUDGET ----------

    if budget > 0:

        st.markdown(
            '<div class="section-title">🎯 Budget Monitor</div>',
            unsafe_allow_html=True
        )

        progress = min(expense / budget, 1.0)

        st.progress(progress)

        percentage = (expense / budget) * 100

        if expense > budget:

            st.error(
                f"⚠️ Budget exceeded by ₹{expense - budget:,.0f}"
            )

        elif percentage >= 80:

            st.warning(
                f"⚠️ You have used {percentage:.1f}% of your budget."
            )

        else:

            st.success(
                f"✅ You have used {percentage:.1f}% of your budget."
            )

    # ---------- CHARTS ----------

    expenses = df[df["Type"] == "Expense"]

    if not expenses.empty:

        st.markdown(
            '<div class="section-title">📈 Spending Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        category_total = (
            expenses
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        with col1:

            pie_chart = px.pie(
                values=category_total.values,
                names=category_total.index,
                title="Expenses by Category"
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        with col2:

            bar_chart = px.bar(
                x=category_total.index,
                y=category_total.values,
                title="Category Spending"
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True
            )

        # ---------- AI INSIGHTS ----------

        st.markdown(
            '<div class="section-title">🤖 AI Spending Insights</div>',
            unsafe_allow_html=True
        )

        highest_category = category_total.index[0]
        highest_amount = category_total.iloc[0]

        st.info(
            f"💡 Your highest spending category is "
            f"**{highest_category}** with "
            f"₹{highest_amount:,.0f} spent."
        )

        if budget > 0:

            if expense > budget:

                st.error(
                    "🚨 AI Alert: Your expenses are above "
                    "your monthly budget. Consider reducing "
                    "non-essential spending."
                )

            elif expense >= budget * 0.8:

                st.warning(
                    "⚠️ AI Alert: You are close to your "
                    "monthly budget limit."
                )

            else:

                st.success(
                    "✅ AI Insight: Your spending is currently "
                    "within your budget."
                )

        if balance > 0:

            st.success(
                f"💰 AI Tip: Your current balance is "
                f"₹{balance:,.0f}. Consider saving part of it."
            )

    # ---------- TRANSACTIONS ----------

    st.markdown(
        '<div class="section-title">📋 Transaction History</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "👋 Welcome to CashPilota AI! "
        "Add your first transaction using the sidebar."
    )

# ---------- FOOTER ----------

st.markdown("---")

st.caption(
    "CashPilota AI • Smart Personal Finance Assistant"
)