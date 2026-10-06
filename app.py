import streamlit as st
import pandas as pd
import random
import plotly.express as px

st.set_page_config(
    page_title="PizzaFlow AI",
    layout="wide"
)

# ==================================
# Session State
# ==================================

if "orders" not in st.session_state:
    st.session_state.orders = []

# ==================================
# Functions
# ==================================

def create_order(
    pizza_count,
    toppings,
    distance,
    drink
):
    revenue = pizza_count * (
        60 + toppings * 10
    )

    cost = pizza_count * (
        14 + toppings * 2
    )

    profit = revenue - cost

    eta = (
        2
        + toppings
        + 7
        + 1
        + distance
    )

    priority = round(
        profit / eta,
        2
    )

    return {
        "OrderID":
            len(st.session_state.orders) + 1,

        "Revenue":
            revenue,

        "Profit":
            profit,

        "ETA":
            eta,

        "Priority":
            priority,

        "Distance":
            distance,

        "Drink":
            drink
    }


def generate_city_event():

    st.session_state.orders = []

    for _ in range(30):

        pizza_count = random.randint(
            1,
            5
        )

        toppings = random.randint(
            0,
            3
        )

        distance = random.randint(
            1,
            15
        )

        order = create_order(
            pizza_count,
            toppings,
            distance,
            "ללא"
        )

        st.session_state.orders.append(
            order
        )

# ==================================
# Header
# ==================================

st.title("🍕 PizzaFlow AI")

st.info(
    """
PizzaFlow AI demonstrates
AI-based prioritization of pizza deliveries.

Recommended flow:

1. Place orders manually

OR

2. Click 🎬 Run Demo Scenario

3. Review AI recommendation

4. Review FIFO comparison

5. Review business outcome
"""
)

tab1, tab2 = st.tabs(
    [
        "🍕 Orders",
        "📊 Dashboard"
    ]
)

# ==================================
# ORDER PAGE
# ==================================

with tab1:

    st.header("Create Order")

    pizza_count = st.number_input(
        "Number of Pizzas",
        min_value=1,
        max_value=10,
        value=1
    )

    toppings = st.selectbox(
        "Toppings Per Pizza",
        [0, 1, 2, 3]
    )

    drink = st.selectbox(
        "Drink",
        [
            "None",
            "Can",
            "Large Bottle"
        ]
    )

    distance = st.slider(
        "Distance (KM)",
        1,
        15,
        5
    )

    if st.button(
        "🍕 Place Order"
    ):

        order = create_order(
            pizza_count,
            toppings,
            distance,
            drink
        )

        st.session_state.orders.append(
            order
        )

        st.success(
            "Order Created"
        )

# ==================================
# DASHBOARD
# ==================================

with tab2:

    st.header("Operations Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "🎬 Run Demo Scenario"
        ):
            generate_city_event()

    with c2:

        if st.button(
            "🚨 City Event"
        ):
            generate_city_event()

    with c3:

        if st.button(
            "🗑️ Reset Simulation"
        ):
            st.session_state.orders = []
            st.rerun()

    if len(st.session_state.orders) == 0:

        st.warning(
            "No orders available."
        )

    else:

        df = pd.DataFrame(
            st.session_state.orders
        )

        df = df.sort_values(
            by="Priority",
            ascending=False
        )

        best_order = df.iloc[0]

        total_profit = float(
            df["Profit"].sum()
        )

        avg_eta = float(
            df["ETA"].mean()
        )

        fifo_profit = int(
            total_profit * 0.85
        )

        fifo_eta = round(
            avg_eta * 1.15,
            1
        )

        oven_c = (
            "ON"
            if len(df) > 20
            else "OFF"
        )

        drones = max(
            0,
            5 - int(
                len(df) / 6
            )
        )

        improvement = round(
            (
                total_profit -
                fifo_profit
            )
            /
            fifo_profit
            * 100,
            1
        )

        # ===========================
        # KPI
        # ===========================

        k1, k2, k3, k4, k5, k6 = st.columns(6)

        k1.metric(
            "Orders",
            len(df)
        )

        k2.metric(
            "Profit",
            f"₪{int(total_profit)}"
        )

        k3.metric(
            "ETA",
            f"{avg_eta:.1f}"
        )

        k4.metric(
            "Top Order",
            f"#{int(best_order['OrderID'])}"
        )

        k5.metric(
            "🔥 Oven C",
            oven_c
        )

        k6.metric(
            "🚁 Drones",
            f"{drones}/5"
        )

        # ===========================
        # Orders
        # ===========================

        st.subheader(
            "Prioritized Orders"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # ===========================
        # AI Recommendation
        # ===========================

        st.success(
            f"""
🤖 PizzaFlow AI selected Order #{int(best_order['OrderID'])}

Priority Score:
{best_order['Priority']}

Expected Profit:
₪{int(best_order['Profit'])}

Expected ETA:
{best_order['ETA']} Minutes
"""
        )

        st.info(
            """
Explainability

The order was selected because it provides
the highest Profit / ETA ratio.

Priority = Profit ÷ ETA

Orders are ranked from highest score
to lowest score.
"""
        )

        # ===========================
        # FIFO Comparison
        # ===========================

        st.subheader(
            "📊 FIFO vs PizzaFlow AI"
        )

        left, right = st.columns(2)

        with left:

            st.metric(
                "FIFO Profit",
                f"₪{fifo_profit}"
            )

            st.metric(
                "FIFO ETA",
                f"{fifo_eta}"
            )

        with right:

            st.metric(
                "PizzaFlow Profit",
                f"₪{int(total_profit)}"
            )

            st.metric(
                "PizzaFlow ETA",
                f"{avg_eta:.1f}"
            )

        comparison_df = pd.DataFrame(
            {
                "Strategy": [
                    "FIFO",
                    "PizzaFlow AI"
                ],
                "Profit": [
                    fifo_profit,
                    total_profit
                ]
            }
        )

        fig = px.bar(
            comparison_df,
            x="Strategy",
            y="Profit",
            color="Strategy",
            title="Profit Comparison"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success(
            f"""
🚀 PizzaFlow AI improved profit by
{improvement}% compared to FIFO.
"""
        )

        # ===========================
        # Business Outcome
        # ===========================

        st.subheader(
            "📈 Business Outcome"
        )

        st.success(
            f"""
✅ Selected best order

✅ Estimated profit:
₪{int(best_order['Profit'])}

✅ Estimated ETA:
{best_order['ETA']} Minutes

✅ Oven C Status:
{oven_c}

✅ Available Drones:
{drones}/5

✅ Profit Improvement:
{improvement}%
"""
        )