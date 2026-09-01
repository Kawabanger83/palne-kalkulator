
import streamlit as st

st.set_page_config(page_title="Калькулятор витрати пального", page_icon="⛽", layout="centered")

st.title("⛽ Калькулятор витрати пального")
st.caption("Норма № 1 + Методика")

cars = {
    "Renault": {
        "Duster 1.5 dCi (дизель)": 5.1,
        "Dokker 1.5 dCi (дизель)": 4.9,
        "Trafic (дизель)": 6.7,
        "Master (дизель)": 8.8,
        "Logan (бензин)": 7.1
    },
    "Toyota": {
        "Hilux 2.4 (дизель)": 7.8,
        "Hilux 2.5 (дизель)": 8.3
    },
    "Volkswagen": {
        "Transporter T5 (дизель)": 8.2,
        "T6 Caravelle (дизель)": 7.7
    },
    "Ford": {
        "Transit (дизель)": 8.1,
        "Transit Connect (дизель)": 6.4
    },
    "КамАЗ": {
        "5410 (дизель)": 25.0,
        "5511 (дизель)": 34.0
    },
    "ГАЗ": {
        "Газель Sofim (дизель)": 11.9,
        "Газель ЗМЗ (бензин)": 15.0,
        "Соболь (бензин)": 13.1
    },
    "УАЗ": {
        "3962 (бензин)": 18.3,
        "452 (бензин)": 17.8
    },
    "МАЗ": {
        "5432 (дизель)": 26.0
    },
    "КрАЗ": {
        "255В (дизель)": 40.0,
        "256 (дизель)": 48.0
    },
    "Mercedes": {
        "Sprinter (дизель)": 12.3
    },
    "Власна норма": {
        "Вручну": 0
    }
}

st.subheader("1. Автомобіль")
brand = st.selectbox("Марка", list(cars.keys()))
model = st.selectbox("Модель", list(cars[brand].keys()))

if brand == "Власна норма":
    Hs = st.number_input("Hs (л/100 км)", min_value=1.0, value=8.0, step=0.1)
else:
    Hs = cars[brand][model]
    st.success(f"{brand} {model} - {Hs} л/100 км")

st.subheader("2. Відстань")
S_city = st.number_input("По місту (км)", min_value=0.0, value=0.0, step=1.0)
S_out = st.number_input("За містом (км)", min_value=0.0, value=100.0, step=1.0)
st.write(f"Загальний пробіг: {S_city + S_out} км")

st.subheader("3. Умови експлуатації")

winter = st.selectbox("Зима", [
    "0% - без надбавки",
    "2% - 0C до -5C",
    "4% - -5C до -10C",
    "6% - -10C до -15C",
    "8% - -15C до -20C",
    "10% - -20C до -25C",
    "12% - нижче -25C"
])

city = st.selectbox("Місто", [
    "0% - за межами міста",
    "5% - міста зі світлофорами",
    "10% - середні міста",
    "15% - Київ, Харків, Львів, Одеса, Дніпро, Запоріжжя, Донецьк"
])

tech = st.selectbox("Технічний стан", [
    "0% - нормальний",
    "3% - більше 5 років + пробіг >100 тис",
    "5% - більше 8 років або >150 тис",
    "7% - більше 11 років або >250 тис",
    "9% - більше 14 років або >400 тис"
])

road = st.selectbox("Дороги / бойові умови", [
    "0% - нормальні дороги",
    "20% - важкі умови",
    "35% - бездоріжжя",
    "50% - зона бойових дій / під обстрілом"
])

mountain = st.selectbox("Гори", [
    "0% - рівнина",
    "5% - 300-800 м",
    "10% - 801-2000 м",
    "15% - 2001-3000 м",
    "20% - вище 3001 м"
])

ac = st.selectbox("Кондиціонер", [
    "0%",
    "5%",
    "7%",
    "10%"
])

highway = st.selectbox("Траса (пониження)", [
    "0%",
    "-10%",
    "-15%",
    "-20%",
    "-25%",
    "-30%"
])

def get_val(text):
    return int(text.split("%")[0].strip())

K = (get_val(winter) + get_val(city) + get_val(tech) +
     get_val(road) + get_val(mountain) + get_val(ac) + get_val(highway))

st.info(f"KΣ = {K}%")

if st.button("РОЗРАХУВАТИ", use_container_width=True):
    Q_city = 0.01 * Hs * S_city * (1 + 0.01 * K)
    Q_out = 0.01 * Hs * S_out * (1 + 0.01 * K)
    Q_total = Q_city + Q_out
    st.success(f"Загальна витрата: {Q_total:.2f} л")
    st.write(f"По місту: {Q_city:.2f} л | За містом: {Q_out:.2f} л")
