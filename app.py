from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================================
# РЕДАКТИРУЙТЕ РЕЦЕПТ ЗДЕСЬ (БЛОК ДАННЫХ)
# =====================================================================

# 1. Базовое количество порций/блинов, на которое рассчитан исходный рецепт
BASE_PORTIONS = 12

# 2. Словарь ингредиентов. 
# Формат: "Название": {"amount": число, "unit": "ед. изм."}
INGREDIENTS = {
    "Молоко": {"amount": 500, "unit": "мл"},
    "Мука": {"amount": 200, "unit": "г"},
    "Яйца": {"amount": 1-2, "unit": "шт."},
    "Сахар": {"amount": 5-6, "unit": "ст. л."},
    "Растительное масло": {"amount": 3, "unit": "ст. л."},
    "Соль": {"amount": 0.5, "unit": "ч. л."}
}

# 3. Список шагов приготовления. Просто добавляйте или удаляйте строки.
STEPS = [
    "В глубокой миске добавьте 0.5 л теплого молока.",
    "В эту миску добавьте яйца с сахаром а потом перемешайте все",
    "Постепенно просейте муку в миску, постоянно мешая, до той массы которая похожа на йогурт, чтобы не было комочков.",
    "Добавьте растительное масло, перемешайте до однородности. Дайте тесту постоять 10-15 минут.",
    "Хорошо разогрейте сковороду, слегка смазав её очень мало масла перед первым блином. Выпекайте блины с двух сторон до золотистого цвета."
]

# =====================================================================
# ЛОГИКА ПРИЛОЖЕНИЯ (НЕ ИЗМЕНЯЙТЕ, ЕСЛИ НЕ ТРЕБУЕТСЯ КОРРЕКЦИЯ ЛОГИКИ)
# =====================================================================

def calculate_recipe(target_portions):
    """Функция пропорционального пересчета ингредиентов"""
    # Вычисляем коэффициент масштабирования
    factor = target_portions / BASE_PORTIONS
    
    scaled_ingredients = {}
    for name, info in INGREDIENTS.items():
        # Округляем до 1 знака после запятой, чтобы избежать длинных дробей
        scaled_amount = round(info["amount"] * factor, 1)
        # Если число целое (например, 6.0), убираем плавающую точку для красоты
        if scaled_amount.is_integer():
            scaled_amount = int(scaled_amount)
            
        scaled_ingredients[name] = {
            "amount": scaled_amount,
            "unit": info["unit"]
        }
    return scaled_ingredients

@app.route("/", methods=["GET", "POST"])
def index():
    # По умолчанию берем базовое количество порций
    portions = BASE_PORTIONS
    
    if request.method == "POST":
        try:
            # Получаем количество порций от пользователя из формы
            user_portions = int(request.form.get("portions", BASE_PORTIONS))
            if user_portions > 0:
                portions = user_portions
        except ValueError:
            pass  # Если введено не число, сработает базовое значение
            
    # Пересчитываем ингредиенты под выбранные порции
    current_ingredients = calculate_recipe(portions)
    
    return render_template(
        "index.html", 
        ingredients=current_ingredients, 
        steps=STEPS, 
        portions=portions,
        base_portions=BASE_PORTIONS
    )

if __name__ == "__main__":
    app.run(debug=True)
