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

# Фиксированные винрейты для героев
WINRATES = {
    "Axe": 55.3,
    "Джаггернаут": 50.1,
    "Invoker": 48.2,
    "Cristal maiden": 50.5,
    "Pudge": 51.2
}

# Фиксированная популярность героев (% выборки)
POPULARITY = {
    "Pudge": 28.5,      # Самый популярный
    "Axe": 22.3,
    "Invoker": 18.7,
    "Cristal maiden": 15.8,
    "Джаггернаут": 14.7 # Самый непопулярный
}

# =================== ЗАГОЛОВОК ===================
st.title("🎮 Интеллектуальная система анализа баланса и генерации контента")
st.markdown("---")

# =================== ВКЛАДКИ ===================
tab1, tab2, tab3, tab4 = st.tabs(["Дашборд", "Балансировка", "Генератор контента", "Загрузка данных"])

# =================== ВКЛАДКА 1: ДАШБОРД ===================
with tab1:
    st.header("Общая статистика баланса")
    
    # Используем фиксированные винрейты и популярность
    df_winrate = pd.DataFrame(list(WINRATES.items()), columns=["Герой", "Винрейт (%)"])
    df_popularity = pd.DataFrame(list(POPULARITY.items()), columns=["Герой", "Частота выбора (%)"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Топ-5 героев по винрейту")
        fig1 = px.bar(df_winrate.sort_values(by="Винрейт (%)", ascending=False), 
                      x="Герой", y="Винрейт (%)", color="Винрейт (%)",
                      color_continuous_scale="RdYlGn")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Статистика по винрейтам
        avg_winrate = df_winrate["Винрейт (%)"].mean()
        max_winrate = df_winrate["Винрейт (%)"].max()
        min_winrate = df_winrate["Винрейт (%)"].min()
        
        st.metric("Средний винрейт", f"{avg_winrate:.1f}%")
        st.metric("Самый высокий винрейт", f"{max_winrate}% (Axe)")
        st.metric("Самый низкий винрейт", f"{min_winrate}% (Invoker)")
    
    with col2:
        st.subheader("Популярность героев")
        fig2 = px.pie(df_popularity, names="Герой", values="Частота выбора (%)",
                     color="Герой", 
                     color_discrete_map={
                         "Pudge": "#FF6B6B",      # Красный для самого популярного
                         "Axe": "#4ECDC4",        # Бирюзовый
                         "Invoker": "#45B7D1",    # Голубой
                         "Cristal maiden": "#96CEB4", # Зеленый
                         "Джаггернаут": "#FFEAA7" # Желтый для самого непопулярного
                     })
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Статистика по популярности
        max_popularity = df_popularity["Частота выбора (%)"].max()
        min_popularity = df_popularity["Частота выбора (%)"].min()
        most_popular = df_popularity.loc[df_popularity["Частота выбора (%)"].idxmax(), "Герой"]
        least_popular = df_popularity.loc[df_popularity["Частота выбора (%)"].idxmin(), "Герой"]
        
        st.metric("Самый популярный", f"{max_popularity}% ({most_popular})")
        st.metric("Самый непопулярный", f"{min_popularity}% ({least_popular})")
        st.metric("Разница в популярности", f"{(max_popularity/min_popularity - 1)*100:.0f}%")
    
    st.subheader("📊 Корреляция винрейта и популярности")
    
    # Создаем DataFrame для анализа
    df_correlation = pd.DataFrame({
        "Герой": list(WINRATES.keys()),
        "Винрейт (%)": list(WINRATES.values()),
        "Популярность (%)": [POPULARITY[h] for h in WINRATES.keys()]
    })
    
    # График рассеяния
    fig_corr = px.scatter(df_correlation, x="Популярность (%)", y="Винрейт (%)",
                         text="Герой", size="Популярность (%)",
                         color="Винрейт (%)", color_continuous_scale="RdYlGn",
                         title="Зависимость винрейта от популярности",
                         labels={"Популярность (%)": "Популярность (% выборки)", 
                                "Винрейт (%)": "Винрейт (%)"})
    fig_corr.update_traces(textposition='top center')
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Анализ корреляции
    correlation = df_correlation["Винрейт (%)"].corr(df_correlation["Популярность (%)"])
    
    col_corr1, col_corr2, col_corr3 = st.columns(3)
    with col_corr1:
        if correlation > 0.5:
            st.success(f"✅ Сильная положительная корреляция: {correlation:.2f}")
        elif correlation > 0.2:
            st.info(f"ℹ️ Умеренная корреляция: {correlation:.2f}")
        elif correlation > -0.2:
            st.warning(f"⚠️ Слабая корреляция: {correlation:.2f}")
        else:
            st.error(f"❌ Отрицательная корреляция: {correlation:.2f}")
    
    with col_corr2:
        # Самый эффективный герой (винрейт / популярность)
        df_correlation["Эффективность"] = df_correlation["Винрейт (%)"] / df_correlation["Популярность (%)"]
        most_efficient = df_correlation.loc[df_correlation["Эффективность"].idxmax(), "Герой"]
        st.metric("Самый эффективный", most_efficient)
    
    with col_corr3:
        # Самый неэффективный герой
        least_efficient = df_correlation.loc[df_correlation["Эффективность"].idxmin(), "Герой"]
        st.metric("Самый неэффективный", least_efficient)
    
    st.subheader("Отчёт о дисбалансе")
    
    # Динамический отчет на основе данных
    imbalance_data = []
    
    # Проверяем дисбалансы для каждого героя
    for hero in HEROES:
        problems = []
        recommendations = []
        
        # Проверка винрейта
        if WINRATES[hero] > 54:
            problems.append("Слишком высокий винрейт")
            recommendations.append("Уменьшить базовые характеристики на 5-10%")
        elif WINRATES[hero] < 46:
            problems.append("Слишком низкий винрейт")
            recommendations.append("Увеличить базовые характеристики на 5-10%")
        
        # Проверка популярности
        if POPULARITY[hero] < 10:
            problems.append("Очень низкая популярность")
            recommendations.append("Добавить новые способности или улучшить существующие")
        elif POPULARITY[hero] > 25 and WINRATES[hero] > 52:
            problems.append("Оверпауэр: популярный и сильный")
            recommendations.append("Рассмотреть нерф в следующем патче")
        
        if problems:  # Если есть проблемы
            imbalance_data.append({
                "Герой": hero,
                "Проблема": ", ".join(problems),
                "Рекомендация": "; ".join(recommendations)
            })
    
    # Добавляем статические примеры если нет динамических проблем
    if not imbalance_data:
        imbalance_data = [
            {
                "Герой": "Axe",
                "Проблема": "Высокий винрейт при хорошей популярности",
                "Рекомендация": "Уменьшить урон на 5% или здоровье на 8%"
            },
            {
                "Герой": "Джаггернаут",
                "Проблема": "Низкая популярность",
                "Рекомендация": "Увеличить базовое здоровье на 10%"
            },
            {
                "Герой": "Invoker",
                "Проблема": "Низкий винрейт",
                "Рекомендация": "Уменьшить стоимость способностей на 15%"
            }
        ]
    
    st.table(pd.DataFrame(imbalance_data))

# =================== ВКЛАДКА 2: БАЛАНСИРОВКА ===================
with tab2:
    st.header("What-if анализ баланса")
    
    # Статические характеристики для каждого героя
    HERO_STATS = {
        "Axe": {
            "Здоровье": 720,
            "Броня": 4.5,
            "Урон": 75,
            "Скорость атаки": 100,
            "Мана": 150
        },
        "Джаггернаут": {
            "Здоровье": 680,
            "Броня": 2.0,
            "Урон": 95,
            "Скорость атаки": 140,
            "Мана": 120
        },
        "Invoker": {
            "Здоровье": 620,
            "Броня": 0.5,
            "Урон": 55,
            "Скорость атаки": 80,
            "Мана": 350
        },
        "Cristal maiden": {
            "Здоровье": 600,
            "Броня": 1.0,
            "Урон": 50,
            "Скорость атаки": 70,
            "Мана": 300
        },
        "Pudge": {
            "Здоровье": 800,
            "Броня": 3.0,
            "Урон": 85,
            "Скорость атаки": 90,
            "Мана": 180
        }
    }
    
    hero = st.selectbox("Выберите героя:", HEROES, key="balance_hero")
    
    st.subheader(f"Характеристики героя: {hero}")
    
    # Показываем текущую статистику героя
    col_stats1, col_stats2 = st.columns(2)
    with col_stats1:
        st.metric("Текущий винрейт", f"{WINRATES[hero]}%")
    with col_stats2:
        st.metric("Популярность", f"{POPULARITY[hero]}%")
    
    # Получаем текущие статические параметры для выбранного героя
    current_params = HERO_STATS[hero]
    
    col1, col2 = st.columns(2)
    proposed_params = {}
    
    with col1:
        st.write("**Текущие статические значения:**")
        # Отображаем статические параметры
        st.metric("Здоровье", f"{current_params['Здоровье']} HP", 
                 delta=None, help="Базовое здоровье на уровне 1")
        st.metric("Броня", f"{current_params['Броня']}", 
                 delta=None, help="Базовая броня (может быть отрицательной)")
        st.metric("Урон", f"{current_params['Урон']}", 
                 delta=None, help="Базовый урон при атаке")
        st.metric("Скорость атаки", f"{current_params['Скорость атаки']}", 
                 delta=None, help="Базовая скорость атаки (чем выше, тем быстрее)")
        st.metric("Мана", f"{current_params['Мана']} MP", 
                 delta=None, help="Базовый запас маны")
    
    with col2:
        st.write("**Предлагаемые изменения:**")
        
        # Слайдеры с реалистичными диапазонами
        proposed_params["Здоровье"] = st.slider(
            "Здоровье (HP)", 
            min_value=300, 
            max_value=1200, 
            value=current_params["Здоровье"],
            step=10,
            key=f"slider_hp_{hero}",
            help="Изменение базового здоровья"
        )
        
        proposed_params["Броня"] = st.slider(
            "Броня", 
            min_value=-5.0, 
            max_value=20.0, 
            value=float(current_params["Броня"]),
            step=0.5,
            key=f"slider_armor_{hero}",
            help="Изменение базовой брони"
        )
        
        proposed_params["Урон"] = st.slider(
            "Урон", 
            min_value=30, 
            max_value=200, 
            value=current_params["Урон"],
            step=5,
            key=f"slider_damage_{hero}",
            help="Изменение базового урона"
        )
        
        proposed_params["Скорость атаки"] = st.slider(
            "Скорость атаки", 
            min_value=20, 
            max_value=300, 
            value=current_params["Скорость атаки"],
            step=5,
            key=f"slider_attack_speed_{hero}",
            help="Изменение базовой скорости атаки"
        )
        
        proposed_params["Мана"] = st.slider(
            "Мана (MP)", 
            min_value=50, 
            max_value=500, 
            value=current_params["Мана"],
            step=10,
            key=f"slider_mana_{hero}",
            help="Изменение базового запаса маны"
        )
    
    # Кнопка для расчета
    if st.button("Рассчитать влияние изменений", type="primary", key="calculate_impact"):
        # Расчет изменений в процентах
        health_change_pct = ((proposed_params["Здоровье"] / current_params["Здоровье"]) - 1) * 100
        armor_change_abs = proposed_params["Броня"] - current_params["Броня"]
        damage_change_pct = ((proposed_params["Урон"] / current_params["Урон"]) - 1) * 100
        attack_speed_change_pct = ((proposed_params["Скорость атаки"] / current_params["Скорость атаки"]) - 1) * 100
        mana_change_pct = ((proposed_params["Мана"] / current_params["Мана"]) - 1) * 100
        
        # Веса влияния параметров на винрейт (зависит от роли героя)
        if hero == "Axe" or hero == "Pudge":
            # Танки/иницииаторы
            weights = {"Здоровье": 0.35, "Броня": 0.3, "Урон": 0.15, "Скорость атаки": 0.1, "Мана": 0.1}
        elif hero == "Джаггернаут":
            # Керри/урон
            weights = {"Здоровье": 0.2, "Броня": 0.15, "Урон": 0.35, "Скорость атаки": 0.2, "Мана": 0.1}
        elif hero == "Invoker" or hero == "Cristal maiden":
            # Маги/саппорты
            weights = {"Здоровье": 0.25, "Броня": 0.2, "Урон": 0.1, "Скорость атаки": 0.1, "Мана": 0.35}
        else:
            weights = {"Здоровье": 0.25, "Броня": 0.25, "Урон": 0.2, "Скорость атаки": 0.2, "Мана": 0.1}
        
        # Расчет влияния на винрейт
        winrate_impact = (
            health_change_pct * weights["Здоровье"] * 0.3 +
            armor_change_abs * 10 * weights["Броня"] * 0.25 +
            damage_change_pct * weights["Урон"] * 0.4 +
            attack_speed_change_pct * weights["Скорость атаки"] * 0.35 +
            mana_change_pct * weights["Мана"] * 0.2
        )
        
        # Расчет влияния на популярность (сильнее зависит от урона и скорости атаки)
        popularity_weights = {"Здоровье": 0.1, "Броня": 0.05, "Урон": 0.4, "Скорость атаки": 0.35, "Мана": 0.1}
        popularity_impact = (
            health_change_pct * popularity_weights["Здоровье"] * 0.2 +
            armor_change_abs * 5 * popularity_weights["Броня"] * 0.1 +
            damage_change_pct * popularity_weights["Урон"] * 0.5 +
            attack_speed_change_pct * popularity_weights["Скорость атаки"] * 0.5 +
            mana_change_pct * popularity_weights["Мана"] * 0.1
        )
        
        # Ограничиваем диапазон изменения
        winrate_delta = max(-15, min(15, winrate_impact))
        popularity_delta = max(-10, min(10, popularity_impact))
        
        new_winrate = max(30, min(70, WINRATES[hero] + winrate_delta))
        new_popularity = max(5, min(40, POPULARITY[hero] + popularity_delta))
        
        st.subheader("📊 Результаты анализа баланса")
        
        # Отображаем изменения
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("Текущий винрейт", f"{WINRATES[hero]}%", 
                     delta=f"{winrate_delta:.1f}%", delta_color="inverse" if winrate_delta > 5 or winrate_delta < -5 else "normal")
            st.metric("Прогнозируемый винрейт", f"{new_winrate:.1f}%")
        
        with col_res2:
            st.metric("Текущая популярность", f"{POPULARITY[hero]}%", 
                     delta=f"{popularity_delta:.1f}%", delta_color="normal")
            st.metric("Прогнозируемая популярность", f"{new_popularity:.1f}%")
        
        with col_res3:
            # Расчет риска на основе величины изменений
            max_change_pct = max(
                abs(health_change_pct),
                abs(damage_change_pct),
                abs(attack_speed_change_pct),
                abs(mana_change_pct),
                abs(armor_change_abs * 5)
            )
            
            if max_change_pct > 25:
                risk = "🔴 Высокий"
            elif max_change_pct > 15:
                risk = "🟡 Средний"
            else:
                risk = "🟢 Низкий"
            
            st.metric("Уровень риска баланса", risk)
            
            # Эффективность изменений
            efficiency_score = abs(winrate_delta) / max(1, max_change_pct) * 10
            efficiency = "Высокая" if efficiency_score > 0.8 else "Средняя" if efficiency_score > 0.4 else "Низкая"
            st.metric("Эффективность изменений", efficiency)
        
        # Визуализация влияния параметров
        st.subheader("📈 Влияние параметров на показатели")
        
        # Создаем DataFrame для визуализации
        impact_data = []
        for param in weights.keys():
            impact_data.append({
                "Параметр": param,
                "Влияние на винрейт": weights[param] * 100,
                "Влияние на популярность": popularity_weights.get(param, 0) * 100
            })
        
        df_impact = pd.DataFrame(impact_data)
        fig_impact = px.bar(df_impact, x="Параметр", y=["Влияние на винрейт", "Влияние на популярность"],
                          barmode='group', title="Влияние параметров на ключевые показатели",
                          color_discrete_map={"Влияние на винрейт": "#4ECDC4", "Влияние на популярность": "#FF6B6B"})
        st.plotly_chart(fig_impact, use_container_width=True)
        
        # График изменений параметров
        st.subheader("📊 Сравнение старых и новых параметров")
        
        params_names = list(current_params.keys())
        old_values = list(current_params.values())
        new_values = list(proposed_params.values())
        
        fig_comparison = go.Figure(data=[
            go.Bar(name='Текущие', x=params_names, y=old_values, marker_color='lightblue'),
            go.Bar(name='Предлагаемые', x=params_names, y=new_values, marker_color='lightgreen')
        ])
        
        fig_comparison.update_layout(
            barmode='group',
            title=f"Сравнение параметров героя {hero}",
            xaxis_title="Параметры",
            yaxis_title="Значение",
            showlegend=True
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Рекомендации по балансировке
        st.subheader("🎯 Рекомендации по балансировке")
        
        # Специальные рекомендации для каждого героя
        hero_specific_recommendations = {
            "Axe": "Axe имеет слишком высокий винрейт (55.3%). Рекомендуется снизить его характеристики.",
            "Джаггернаут": "Джаггернаут имеет низкую популярность (14.7%). Рассмотрите улучшение его характеристик.",
            "Invoker": "Invoker имеет низкий винрейт (48.2%). Возможно, требуется усиление.",
            "Cristal maiden": "Cristal maiden сбалансирован, но можно улучшить выживаемость.",
            "Pudge": "Pudge самый популярный (28.5%), но винрейт в норме. Изменения должны быть осторожными."
        }
        
        st.info(hero_specific_recommendations.get(hero, ""))
        
        if winrate_delta > 8:
            st.error("### ⚠️ **ВЫСОКИЙ РИСК ДИСБАЛАНСА**")
            st.markdown(f"Герой **{hero}** станет слишком сильным (+{winrate_delta:.1f}% к винрейту).")
        elif winrate_delta > 4:
            st.warning("### ⚠️ **УМЕРЕННЫЙ РИСК УСИЛЕНИЯ**")
            st.markdown(f"Герой **{hero}** может стать сильнее оптимального (+{winrate_delta:.1f}% к винрейту).")
        elif winrate_delta < -8:
            st.error("### ⚠️ **ВЫСОКИЙ РИСК ОСЛАБЛЕНИЯ**")
            st.markdown(f"Герой **{hero}** станет слишком слабым ({winrate_delta:.1f}% к винрейту).")
        elif winrate_delta < -4:
            st.warning("### ⚠️ **УМЕРЕННЫЙ РИСК ОСЛАБЛЕНИЯ**")
            st.markdown(f"Герой **{hero}** может стать слабее оптимального ({winrate_delta:.1f}% к винрейту).")
        else:
            st.success("### ✅ **БЕЗОПАСНЫЙ ДИАПАЗОН**")
            st.markdown(f"Предлагаемые изменения находятся в безопасном диапазоне (±{abs(winrate_delta):.1f}% к винрейту).")
        
        # Кнопка для сохранения настроек
        if st.button("💾 Сохранить предложенные изменения", key="save_changes"):
            st.session_state[f'proposed_changes_{hero}'] = proposed_params
            st.session_state[f'calculated_winrate_{hero}'] = new_winrate
            st.session_state[f'calculated_popularity_{hero}'] = new_popularity
            st.success(f"Настройки для героя {hero} сохранены!")

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

# =================== ВКЛАДКА 4: ЗАГРУЗКА ДАННЫХ ===================
with tab4:
    st.header("Загрузка и обновление данных")
    
    data_source = st.radio("Источник данных:", ["OpenDota API", "Локальный файл", "Демо-данные"])
    
    if data_source == "OpenDota API":
        matches_limit = st.number_input("Количество матчей:", min_value=10, max_value=10000, value=100)
        if st.button("Загрузить данные с OpenDota"):
            with st.spinner("Загрузка данных..."):
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
            import time
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        st.success("✅ Данные обработаны и готовы к анализу")

# =================== ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ В САЙДБАР ===================
with st.sidebar:
    st.header("ℹ️ Статистика героев")
    
    selected_hero = st.selectbox("Выберите героя:", HEROES, key="sidebar_hero")
    
    if selected_hero in HERO_STATS:
        st.subheader(f"📊 {selected_hero}")
        
        # Винрейт с индикатором
        winrate = WINRATES[selected_hero]
        if winrate > 54:
            winrate_status = "🔴 Слишком высокий"
        elif winrate > 52:
            winrate_status = "🟡 Выше среднего"
        elif winrate < 46:
            winrate_status = "🔵 Слишком низкий"
        elif winrate < 48:
            winrate_status = "🟠 Ниже среднего"
        else:
            winrate_status = "🟢 Сбалансированный"
        
        st.metric("Винрейт", f"{winrate}%", winrate_status)
        
        # Популярность с индикатором
        popularity = POPULARITY[selected_hero]
        if popularity > 25:
            popularity_status = "🔥 Очень популярный"
        elif popularity > 20:
            popularity_status = "⭐ Популярный"
        elif popularity < 12:
            popularity_status = "📉 Непопулярный"
        else:
            popularity_status = "📊 Средняя популярность"
        
        st.metric("Популярность", f"{popularity}%", popularity_status)
        
        # Рейтинг героя
        st.markdown("---")
        st.subheader("🏆 Рейтинг героя")
        
        # Место по винрейту
        winrate_rank = sorted(WINRATES.items(), key=lambda x: x[1], reverse=True)
        winrate_position = [i for i, (h, _) in enumerate(winrate_rank) if h == selected_hero][0] + 1
        st.write(f"**Место по винрейту:** #{winrate_position} из {len(HEROES)}")
        
        # Место по популярности
        popularity_rank = sorted(POPULARITY.items(), key=lambda x: x[1], reverse=True)
        popularity_position = [i for i, (h, _) in enumerate(popularity_rank) if h == selected_hero][0] + 1
        st.write(f"**Место по популярности:** #{popularity_position} из {len(HEROES)}")
        
        # Общая оценка баланса
        balance_score = (winrate / 60 * 0.6 + popularity / 30 * 0.4) * 100
        st.progress(balance_score/100, text=f"Общая оценка: {balance_score:.1f}/100")
    
    st.markdown("---")
    st.subheader("📈 Топ-5 по популярности")
    
    # Сортировка по популярности
    sorted_popularity = sorted(POPULARITY.items(), key=lambda x: x[1], reverse=True)
    
    for i, (hero_name, pop_value) in enumerate(sorted_popularity, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        st.write(f"{medal} **{hero_name}**: {pop_value}%")
    
    st.markdown("---")
    st.caption("**Примечание:** Балансным считается винрейт 48-52%. Популярность выше 20% считается высокой.")

# =================== ФУТЕР ===================
st.markdown("---")
st.caption("Прототип интеллектуальной системы для анализа баланса и генерации игрового контента | 2024")
