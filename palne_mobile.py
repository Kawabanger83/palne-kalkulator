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
.stApp {background-color: #0e1117; color: #fafafa;}
.stButton>button {
    width: 100%;
    height: 55px;
    font-size: 18px !important;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⛽ Витрата пального")
st.caption("Норма № 1 + Методика Держспецзв’язок")

st.subheader("1. Автомобіль")

popular = {
    "Renault Duster 1.5 dCi": {"Hs": 5.1, "fuel": "дизель"},
    "Toyota Hilux 2.4": {"Hs": 7.8, "fuel": "дизель"},
    "VW Transporter T5": {"Hs": 8.2, "fuel": "дизель"},
    "КамАЗ-5410": {"Hs": 25.0, "fuel": "дизель"},
    "ГАЗ-2705 Газель (Sofim)": {"Hs": 11.9, "fuel": "дизель"},
    "УАЗ-3962": {"Hs": 18.3, "fuel": "бензин"},
    "Власна норма": None
}

quick = st.selectbox("Оберіть модель", list(popular.keys()))

if quick != "Власна норма":
    data = popular[quick]
    Hs = data["Hs"]
    fuel_type = data["fuel"]
    st.success(f"**{quick}**  •  {Hs} л/100 км  •  {fuel_type}")
else:
    Hs = st.number_input("Базова норма Hs (л/100 км)", min_value=1.0, value=8.0, step=0.1)
    fuel_type = st.selectbox("Тип пального", ["дизель", "бензин"])

S = st.number_input("Пробіг (км)", min_value=0.0, value=100.0, step=1.0)

st.subheader("2. Умови експлуатації")

winter_options = {
    "Без зимової надбавки": 0,
    "0°C … -5°C (до +2%)": 2,
    "-5°C … -10°C (до +4%)": 4,
    "-10°C … -15°C (до +6%)": 6,
    "-15°C … -20°C (до +8%)": 8,
    "-20°C … -25°C (до +10%)": 10,
    "нижче -25°C (до +12%)": 12
}
k_winter = st.selectbox("Зимова надбавка (температура)", list(winter_options.keys()))
k_winter_val = winter_options[k_winter]

k_traffic = st.slider("Затори / інтенсивний міський рух", 0, 15, 0)
k_ac = st.slider("Кондиціонер / клімат-контроль", 0, 10, 0)
k_bad_road = st.slider("Погані дороги / бездоріжжя", 0, 35, 0)
k_combat = st.slider("Зона бойових дій / рух під обстрілом", 0, 50, 0)
k_mountain = st.slider("Гірська місцевість", 0, 20, 0)
k_tech = st.slider("Технічний стан авто", 0, 10, 0)
k_highway = st.slider("Понижувальний (траса)", -30, 0, 0)

K_sum = k_winter_val + k_traffic + k_ac + k_bad_road + k_combat + k_mountain + k_tech + k_highway
st.info(f"**Сумарний KΣ = {K_sum}%**")

with st.expander("📋 Довідка по коефіцієнтах"):
    st.markdown("""
**Зима:**
- 0…-5°C → до 2%
- -5…-10°C → до 4%
- -10…-15°C → до 6%
- -15…-20°C → до 8%
- -20…-25°C → до 10%
- нижче -25°C → до 12%

**Бойові умови / надважкі дороги** → до 50%  
**Затори** → до 15%  
**Кондиціонер** → до 10%  
**Траса (понижувальний)** → від -5% до -30%
    """)

if st.button("РОЗРАХУВАТИ", use_container_width=True, type="primary"):
    Qn = 0.01 * Hs * S * (1 + 0.01 * K_sum)
    
    st.markdown(f"""
    <div style="background-color:#1e3a2f; padding:20px; border-radius:12px; text-align:center;">
        <h2 style="color:#00ff88; margin:0;">Qн = {Qn:.2f} л</h2>
        <p>{fuel_type.upper()} • KΣ = {K_sum}%</p>
    </div>
    """, unsafe_allow_html=True)

st.caption("Згідно з Методикою нормування витрат пального")
