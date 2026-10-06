import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PizzaFlow AI",
    layout="wide"
)

if "orders" not in st.session_state:
    st.session_state.orders = []

st.title("🍕 PizzaFlow AI")

tab1, tab2 = st.tabs(
    ["🍕 הזמנות", "📊 Dashboard"]
)

# =====================
# הזמנות
# =====================

with tab1:

    st.header("הזמנת פיצה")

    pizza_count = st.number_input(
        "מספר פיצות",
        min_value=1,
        max_value=10,
        value=1
    )

    toppings = st.selectbox(
        "מספר תוספות לכל פיצה",
        [0, 1, 2, 3]
    )

    drink = st.selectbox(
        "שתייה",
        [
            "ללא",
            "פחית",
            "בקבוק גדול"
        ]
    )

    distance = st.slider(
        "מרחק מהמטבח (ק״מ)",
        1,
        15,
        5
    )

    if st.button("בצע הזמנה"):

        order_id = len(
            st.session_state.orders
        ) + 1

        revenue = (
            pizza_count *
            (60 + toppings * 10)
        )

        cost = (
            pizza_count *
            (14 + toppings * 2)
        )

        profit = revenue - cost

        eta = (
            2 +
            toppings +
            7 +
            1 +
            distance
        )

        priority = round(
            profit / eta,
            2
        )

        st.session_state.orders.append(
            {
                "OrderID": order_id,
                "Revenue": revenue,
                "Profit": profit,
                "ETA": eta,
                "Priority": priority,
                "Distance": distance,
                "Drink": drink
            }
        )

        st.success(
            f"הזמנה #{order_id} נקלטה"
        )


# =====================
# Dashboard
# =====================
with tab2:

    st.header("Dashboard")

    st.metric(
        "הזמנות",
        len(st.session_state.orders)
    )

    if len(st.session_state.orders) > 0:

        df = pd.DataFrame(
            st.session_state.orders
        )

        df = df.sort_values(
            by="Priority",
            ascending=False
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        best_order = df.iloc[0]

        st.success(
            f"""
🤖 PizzaFlow AI בחרה בהזמנה #{best_order['OrderID']}

Priority: {best_order['Priority']}

Profit: ₪{best_order['Profit']}

ETA: {best_order['ETA']} דקות
"""
        )

    else:

        st.info(
            "אין הזמנות"
        )