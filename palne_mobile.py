import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Витрата пального",
    page_icon="⛽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stButton>button {
            width: 100%;
            height: 60px;
            font-size: 22px !important;
            font-weight: bold;
            background-color: #ff4b4b;
            color: white;
            border-radius: 12px;
        }
        .stMetric {
            background-color: #262730;
            padding: 15px;
            border-radius: 12px;
        }
        h1, h2, h3 {
            color: #ffffff !important;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⛽ Витрата пального")
st.caption("Норма № 1 + Методика (Держспецзв’язок)")

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Швидкий вибір")

popular = {
    "Renault Duster 1.5 dCi": {"Hs": 5.1, "fuel": "дизель"},
    "Toyota Hilux 2.4": {"Hs": 7.8, "fuel": "дизель"},
    "VW Transporter T5": {"Hs": 8.2, "fuel": "дизель"},
    "КамАЗ-5410": {"Hs": 25.0, "fuel": "дизель"},
    "ГАЗ-2705 Газель (Sofim)": {"Hs": 11.9, "fuel": "дизель"},
    "УАЗ-3962": {"Hs": 18.3, "fuel": "бензин"},
    "Власна норма": None
}

quick = st.selectbox("Популярні моделі", list(popular.keys()))

if quick != "Власна норма":
    data = popular[quick]
    Hs = data["Hs"]
    fuel_type = data["fuel"]
    st.success(f"**{quick}**  |  {Hs} л/100 км  |  {fuel_type}")
else:
    Hs = st.number_input("Базова норма Hs (л/100 км)", min_value=1.0, value=8.0, step=0.1)
    fuel_type = st.selectbox("Тип пального", ["дизель", "бензин"])

S = st.number_input("Пробіг (км)", min_value=0.0, value=100.0, step=1.0)

st.subheader("Умови експлуатації")

k_combat = st.slider("Зона бойових дій / під обстрілом (до +50%)", 0, 50, 0)
k_winter = st.slider("Зима / холод", 0, 30, 0)
k_bad_road = st.slider("Погані дороги / бездоріжжя", 0, 40, 0)
k_city = st.slider("Місто / інтенсивний рух", 0, 25, 0)
k_mountain = st.slider("Гірська місцевість", 0, 25, 0)
k_other = st.slider("Інші надбавки", 0, 30, 0)
k_reduce = st.slider("Понижувальні (траса)", -30, 0, 0)

K_sum = k_combat + k_winter + k_bad_road + k_city + k_mountain + k_other + k_reduce
st.info(f"**Сумарний коефіцієнт KΣ = {K_sum}%**")

if st.button("РОЗРАХУВАТИ", use_container_width=True):
    Qn = 0.01 * Hs * S * (1 + 0.01 * K_sum)
    
    record = {
        "час": datetime.now().strftime("%d.%m %H:%M"),
        "модель": quick,
        "пробіг":
