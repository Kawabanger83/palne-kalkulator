import streamlit as st

st.set_page_config(page_title="Калькулятор витрати пального", page_icon="⛽", layout="centered")

st.title("⛽ Калькулятор витрати пального")
st.caption("Норма № 1 + Методика нормування")

# ========== БАЗА АВТО (розширена) ==========
cars = {
    "Renault Duster 1.5 dCi": 5.1,
    "Renault Dokker 1.5 dCi": 4.9,
    "Toyota Hilux 2.4": 7.8,
    "Toyota Hilux 2.5": 8.3,
    "VW Transporter T5": 8.2,
    "VW T6 Caravelle": 7.7,
    "КамАЗ-5410": 25.0,
    "КамАЗ-5511": 34.0,
    "ГАЗ-2705 Газель (Sofim)": 11.9,
    "ГАЗ-2705 Газель (ЗМЗ)": 15.0,
    "УАЗ-3962": 18.3,
    "УАЗ-452": 17.8,
    "МАЗ-5432": 26.0,
    "КрАЗ-255В": 40.0,
    "ВАЗ-2110": 7.6,
    "Daewoo Lanos 1.5": 9.3,
    "Skoda Fabia 1.2": 6.0,
    "Ford Transit": 8.1,
    "Mercedes Sprinter": 12.3,
    "Власна норма": 0
}

# Пошук
search = st.text_input("🔍 Пошук моделі авто", placeholder="Введіть назву авто...")

filtered_cars = {k: v for k, v in cars.items() if search.lower() in k.lower()} if search else cars

model = st.selectbox("Оберіть модель", list(filtered_cars.keys()))

if model == "Власна норма":
    Hs = st.number_input("Введіть базову норму Hs (л/100 км)", min_value=1.0, value=8.0, step=0.1)
else:
    Hs = filtered_cars[model]
    st.write(f"**Базова норма:** {Hs} л/100 км")

S = st.number_input("Пробіг (км)", min_value=0.0, value=100.0, step=1.0)

st.divider()
st.subheader("Умови експлуатації (з Методики)")

# Зима
winter = st.selectbox("Зимова надбавка (температура)", [
    "Без надбавки (0%)",
    "0°C до -5°C (+2%)",
    "-5°C до -10°C (+4%)",
    "-10°C до -15°C (+6%)",
    "-15°C до -20°C (+8%)",
    "-20°C до -25°C (+10%)",
    "нижче -25°C (+12%)"
])
winter_val = int(winter.split("(")[-1].replace("%)","").replace("+","")) if "+" in winter else 0

# Інші
k_traffic = st.slider("Затори / інтенсивний рух", 0, 15, 0)
k_ac = st.slider("Кондиціонер / клімат-контроль", 0, 10, 0)
k_bad = st.slider("Погані дороги / бездоріжжя", 0, 35, 0)
k_combat = st.slider("Зона бойових дій / під обстрілом", 0, 50, 0)
k_mountain = st.slider("Гірська місцевість", 0, 20, 0)
k_highway = st.slider("Понижувальний коефіцієнт (траса)", -30, 0, 0)

K_sum = winter_val + k_traffic + k_ac + k_bad + k_combat + k_mountain + k_highway

st.info(f"**Сумарний коефіцієнт KΣ = {K_sum} %**")

if st.button("РОЗРАХУВАТИ", use_container_width=True):
    Qn = 0.01 * Hs * S * (1 + 0.01 * K_sum)
    st.success(f"### Нормативна витрата: **{Qn:.2f} л**")
    st.write(f"Модель: {model} | Пробіг: {S} км | KΣ: {K_sum}%")

with st.expander("Довідка по коефіцієнтах (Методика)"):
    st.markdown("""
**Зима (п. 3.1.1):**
- 0…-5°C → до 2%
- -5…-10°C → до 4%
- -10…-15°C → до 6%
- -15…-20°C → до 8%
- -20…-25°C → до 10%
- нижче -25°C → до 12%

**Інші надбавки:**
- Затори / місто → до 15%
- Кондиціонер → до 10%
- Погані дороги → до 35%
- Бойові дії / під обстрілом → до **50%**
- Гірська місцевість → до 20%

**Понижувальний (траса):** від -5% до -30%
    """)
