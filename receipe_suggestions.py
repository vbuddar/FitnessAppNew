from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

# Example recipes
recipes = [
    {
        "name": "Grilled Chicken Salad",
        "ingredients": ["Chicken breast", "Lettuce", "Cherry tomatoes", "Olive oil", "Lemon juice"],
        "steps": ["Grill the chicken breast.", "Chop lettuce and tomatoes.", "Mix and drizzle with olive oil."],
        "calories": 350,
        "macros": {"protein": 30, "carbs": 10, "fat": 15},
        "goal": ["muscle_gain", "weight_loss"],
        "type": "lunch"
    },
    {
        "name": "Greek Yogurt Parfait",
        "ingredients": ["Greek yogurt", "Granola", "Mixed berries"],
        "steps": ["Layer Greek yogurt, granola, and mixed berries.", "Serve chilled."],
        "calories": 200,
        "macros": {"protein": 12, "carbs": 20, "fat": 5},
        "goal": ["maintenance", "weight_loss"],
        "type": "snack"
    }
]

@app.route('/recipes', methods=['GET'])
def get_recipes():
    goal = request.args.get('goal', 'maintenance')  # Default goal if none is specified
    meal_type = request.args.get('type', None)     # Optional meal type filter
    
    # Filter recipes by fitness goal and type
    filtered_recipes = [recipe for recipe in recipes if goal in recipe["goal"]]
    if meal_type:
        filtered_recipes = [recipe for recipe in filtered_recipes if recipe["type"] == meal_type]

    # Rotate recipes randomly
    suggested_recipes = random.sample(filtered_recipes, min(3, len(filtered_recipes)))

    return jsonify(suggested_recipes)

@app.route('/recipes_page')
def recipes_page():
    return render_template('recipes.html')  # Renders a separate page for Recipe Suggestions
