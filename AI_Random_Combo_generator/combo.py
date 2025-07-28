from flask import Flask, jsonify, request, send_from_directory
import random
import os

app = Flask(__name__)

MENU = [
    {"item_name": "Paneer Butter Masala", "category": "main", "calories": 450, "taste_profile": "spicy", "popularity_score": 0.9},
    {"item_name": "Chicken Biryani", "category": "main", "calories": 600, "taste_profile": "spicy", "popularity_score": 0.95},
    {"item_name": "Vegetable Pulao", "category": "main", "calories": 400, "taste_profile": "savory", "popularity_score": 0.7},
    {"item_name": "Rajma Chawal", "category": "main", "calories": 500, "taste_profile": "savory", "popularity_score": 0.8},
    {"item_name": "Chole Bhature", "category": "main", "calories": 650, "taste_profile": "spicy", "popularity_score": 0.85},
    {"item_name": "Masala Dosa", "category": "main", "calories": 480, "taste_profile": "savory", "popularity_score": 0.88},
    {"item_name": "Grilled Sandwich", "category": "main", "calories": 370, "taste_profile": "savory", "popularity_score": 0.6},
    {"item_name": "Garlic Naan", "category": "side", "calories": 200, "taste_profile": "savory", "popularity_score": 0.9},
    {"item_name": "Mixed Veg Salad", "category": "side", "calories": 150, "taste_profile": "sweet", "popularity_score": 0.75},
    {"item_name": "French Fries", "category": "side", "calories": 350, "taste_profile": "savory", "popularity_score": 0.8},
    {"item_name": "Curd Rice", "category": "side", "calories": 250, "taste_profile": "savory", "popularity_score": 0.7},
    {"item_name": "Papad", "category": "side", "calories": 100, "taste_profile": "savory", "popularity_score": 0.65},
    {"item_name": "Paneer Tikka", "category": "side", "calories": 300, "taste_profile": "spicy", "popularity_score": 0.85},
    {"item_name": "Masala Chaas", "category": "drink", "calories": 100, "taste_profile": "spicy", "popularity_score": 0.8},
    {"item_name": "Sweet Lassi", "category": "drink", "calories": 220, "taste_profile": "sweet", "popularity_score": 0.9},
    {"item_name": "Lemon Soda", "category": "drink", "calories": 90, "taste_profile": "savory", "popularity_score": 0.7},
    {"item_name": "Cold Coffee", "category": "drink", "calories": 180, "taste_profile": "sweet", "popularity_score": 0.75},
    {"item_name": "Coconut Water", "category": "drink", "calories": 60, "taste_profile": "sweet", "popularity_score": 0.6},
    {"item_name": "Iced Tea", "category": "drink", "calories": 120, "taste_profile": "sweet", "popularity_score": 0.78},
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def round_popularity(score):
    return round(score * 20) / 20

def generate_combos(menu, start_day):
    combos = []
    used_combos = set()
    days_idx = DAYS.index(start_day)
    days_order = DAYS[days_idx:] + DAYS[:days_idx]

    all_combos = []
    for drink in menu:
        if drink['category'] != 'drink':
            continue
        for savory in menu:
            if savory['category'] not in ['main', 'side'] or savory['taste_profile'] != 'savory':
                continue
            for sweet in menu:
                if sweet['taste_profile'] != 'sweet' or sweet['category'] not in ['side', 'drink']:
                    continue
                names = {drink['item_name'], savory['item_name'], sweet['item_name']}
                if len(names) < 3:
                    continue
                total_cal = drink['calories'] + savory['calories'] + sweet['calories']
                if not (500 <= total_cal <= 800):
                    continue
                pop_drink = round_popularity(drink['popularity_score'])
                pop_savory = round_popularity(savory['popularity_score'])
                pop_sweet = round_popularity(sweet['popularity_score'])
                if not (abs(pop_drink - pop_savory) <= 0.05 and abs(pop_drink - pop_sweet) <= 0.05):
                    continue
                combo = (drink['item_name'], savory['item_name'], sweet['item_name'])
                all_combos.append({
                    'combo': combo,
                    'popularity': round((pop_drink + pop_savory + pop_sweet) / 3, 2),
                    'calories': total_cal
                })

    random.shuffle(all_combos)
    print(f"Total possible combos: {len(all_combos)}")

    for i in range(7):  # 7 days
        found = False
        for combo in all_combos:
            combo_key = combo['combo']
            if combo_key in used_combos:
                continue
            if i >= 2 and combos[i-1]['combo'] == combo_key and combos[i-2]['combo'] == combo_key:
                continue
            combos.append({'day': days_order[i], **combo})
            used_combos.add(combo_key)
            found = True
            break
        if not found:
            combos.append({'day': days_order[i], 'combo': ('N/A', 'N/A', 'N/A'), 'popularity': 'N/A', 'calories': 'N/A'})
    return combos

@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/menu')
def get_menu():
    return jsonify(MENU)

@app.route('/generate_combos')
def get_combos():
    start_day = request.args.get('start_day', 'Monday')
    combos = generate_combos(MENU, start_day)
    return jsonify(combos)

if __name__ == '__main__':
    app.run(debug=True)