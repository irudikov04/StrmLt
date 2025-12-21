import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# =================== КОНФИГУРАЦИЯ ===================
st.set_page_config(page_title="Game Balance AI", layout="wide")

# Демо-данные
HEROES = ["Axe", "Джаггернаут", "Invoker", "Cristal maiden", "Pudge"]
PARAMS = ["Урон", "Здоровье", "Скорость атаки", "Броня", "Мана"]

# Инициализация session_state для хранения значений ползунков
if 'proposed_params' not in st.session_state:
    st.session_state.proposed_params = {}

# =================== ЗАГОЛОВОК ===================
st.title("🎮 Интеллектуальная система анализа баланса и генерации контента")
st.markdown("---")

# =================== ВКЛАДКИ ===================
tab1, tab2, tab3, tab4 = st.tabs(["Дашборд", "Балансировка", "Генератор контента", "Загрузка данных"])

# =================== ВКЛАДКА 1: ДАШБОРД ===================
with tab1:
    st.header("Общая статистика баланса")
    
    # Демо-данные для графиков
    winrates = {hero: round(random.uniform(40, 60), 1) for hero in HEROES}
    pickrates = {hero: random.randint(5, 30) for hero in HEROES}
    
    df_winrate = pd.DataFrame(list(winrates.items()), columns=["Герой", "Винрейт (%)"])
    df_pickrate = pd.DataFrame(list(pickrates.items()), columns=["Герой", "Частота выбора (%)"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Топ-5 героев по винрейту")
        fig1 = px.bar(df_winrate.sort_values(by="Винрейт (%)", ascending=False), 
                      x="Герой", y="Винрейт (%)", color="Винрейт (%)")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Популярность героев")
        fig2 = px.pie(df_pickrate, names="Герой", values="Частота выбора (%)")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Отчёт о дисбалансе")
    imbalance_report = {
        "Герой": ["Акс", "Джаггернаут", "Инвокер"],
        "Проблема": ["Слишком высокий винрейт", "Низкая популярность", "Сильная зависимость от маны"],
        "Рекомендация": ["Уменьшить урон на 5%", "Увеличить базовое здоровье", "Уменьшить стоимость способностей"]
    }
    st.table(pd.DataFrame(imbalance_report))

# =================== ВКЛАДКА 2: БАЛАНСИРОВКА ===================
with tab2:
    st.header("What-if анализ баланса")
    
    hero = st.selectbox("Выберите героя:", HEROES, key="balance_hero")
    
    # Инициализация current_params для выбранного героя
    if f'current_params_{hero}' not in st.session_state:
        st.session_state[f'current_params_{hero}'] = {param: random.randint(50, 150) for param in PARAMS}
    
    current_params = st.session_state[f'current_params_{hero}']
    
    st.subheader("Текущие параметры")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Текущие значения:**")
        for param, value in current_params.items():
            st.metric(param, value)
    
    with col2:
        st.write("**Предлагаемые изменения:**")
        
        # Инициализация значений для ползунков
        for param in PARAMS:
            param_key = f"{hero}_{param}"
            
            # Если значение еще не сохранено, используем текущее
            if param_key not in st.session_state.proposed_params:
                st.session_state.proposed_params[param_key] = current_params[param]
            
            # Ползунок с сохранением состояния
            new_value = st.slider(
                param, 
                min_value=int(current_params[param] * 0.5), 
                max_value=int(current_params[param] * 1.5), 
                value=st.session_state.proposed_params[param_key],
                key=param_key,
                on_change=lambda p=param, h=hero: None
            )
            
            # Сохраняем новое значение в session_state
            st.session_state.proposed_params[f"{hero}_{param}"] = new_value
    
    # Кнопка сброса значений
    if st.button("Сбросить к текущим значениям", key="reset_button"):
        for param in PARAMS:
            st.session_state.proposed_params[f"{hero}_{param}"] = current_params[param]
        st.rerun()
    
    if st.button("Рассчитать влияние", type="primary"):
        # Собираем текущие значения ползунков
        current_slider_values = {}
        for param in PARAMS:
            current_slider_values[param] = st.session_state.proposed_params[f"{hero}_{param}"]
        
        # Демо-расчёт изменения винрейта
        delta = random.uniform(-10, 10)
        st.subheader("Результаты анализа")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Прогнозируемое ΔWR", f"{delta:.1f}%", 
                      delta_color="inverse" if abs(delta) > 5 else "normal")
        
        with col_res2:
            risk = "🔴 Высокий" if abs(delta) > 7 else "🟡 Средний" if abs(delta) > 3 else "🟢 Низкий"
            st.metric("Уровень риска", risk)
        
        # Визуализация влияния параметров
        importance = {param: random.random() for param in PARAMS}
        df_importance = pd.DataFrame(list(importance.items()), columns=["Параметр", "Влияние"])
        fig3 = px.bar(df_importance.sort_values(by="Влияние"), x="Влияние", y="Параметр", orientation='h')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Рекомендация
        if delta > 5:
            st.warning("⚠️ Изменения могут сделать героя слишком сильным. Рекомендуется уменьшить влияние ключевых параметров.")
        elif delta < -5:
            st.warning("⚠️ Герой может стать слишком слабым. Рассмотрите увеличение параметров защиты.")
        else:
            st.success("✅ Предлагаемые изменения находятся в безопасном диапазоне.")

# =================== ВКЛАДКА 3: ГЕНЕРАТОР КОНТЕНТА ===================
with tab3:
    st.header("Генерация нового игрового контента")
    
    item_type = st.selectbox("Тип предмета:", ["Оружие", "Броня", "Артефакт", "Зелье"])
    style = st.selectbox("Стиль описания:", ["Фэнтези", "Киберпанк", "Исторический", "Мистический"])
    
    if st.button("Сгенерировать предмет", type="primary"):
        st.subheader("🎉 Новый предмет создан!")
        
        # Демо-характеристики
        characteristics = {
            "Урон": random.randint(10, 100),
            "Защита": random.randint(5, 50),
            "Редкость": random.choice(["Обычный", "Редкий", "Эпический", "Легендарный"]),
            "Стоимость": random.randint(100, 1000)
        }
        
        # Демо-описание
        descriptions = {
            "Фэнтези": f"Древний {item_type.lower()}, испещрённый рунами эльфов. Излучает мягкое свечение.",
            "Киберпанк": f"Высокотехнологичный {item_type.lower()} с голографическим интерфейсом. Пиксели мерцают неоновым светом.",
            "Исторический": f"Аутентичный {item_type.lower()} эпохи возрождения. Следы использования говорят о многих битвах.",
            "Мистический": f"{item_type.capitalize()}, хранящий тайны древних культов. При касании слышен шёпот теней."
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Характеристики")
            for key, value in characteristics.items():
                st.metric(key, value)
            
            # Оценка баланса
            balance_score = random.random()
            if balance_score > 0.7:
                st.success("✅ Сбалансирован")
            elif balance_score > 0.4:
                st.warning("⚠️ Требует доработки")
            else:
                st.error("❌ Дисбаланс")
        
        with col2:
            st.subheader("Описание")
            st.info(descriptions[style])
            
            if style == "Киберпанк" and item_type == "Оружие":
                st.warning("⚠️ Описание недостаточно соответствует стилю Киберпанк для оружия. Рекомендуется перегенерировать.")
                if st.button("Перегенерировать описание"):
                    st.rerun()

# =================== ВКЛАДКА 4: ЗАГРУЗКА ДАННЫХ ===================
with tab4:
    st.header("Загрузка и обновление данных")
    
    data_source = st.radio("Источник данных:", ["OpenDota API", "Локальный файл", "Демо-данные"])
    
    if data_source == "OpenDota API":
        matches_limit = st.number_input("Количество матчей:", min_value=10, max_value=10000, value=100)
        if st.button("Загрузить данные с OpenDota"):
            with st.spinner("Загрузка данных..."):
                # Имитация загрузки
                import time
                time.sleep(2)
                st.success(f"✅ Загружено {matches_limit} матчей")
    
    elif data_source == "Локальный файл":
        uploaded_file = st.file_uploader("Выберите файл (JSON, CSV)", type=["json", "csv"])
        if uploaded_file:
            st.success(f"✅ Файл {uploaded_file.name} загружен")
    
    else:
        st.info("Используются встроенные демо-данные для тестирования.")
    
    if st.button("Запустить ETL-пайплайн", type="primary"):
        progress_bar = st.progress(0)
        for i in range(100):
            # Имитация процесса
            import time
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        st.success("✅ Данные обработаны и готовы к анализу")

# =================== ФУТЕР ===================
st.markdown("---")
st.caption("Прототип интеллектуальной системы для анализа баланса и генерации игрового контента | 2024")
