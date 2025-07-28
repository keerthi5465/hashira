import random
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd

# Data
menu = [
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

# Group items by category
mains = [item for item in menu if item["category"] == "main"]
sides = [item for item in menu if item["category"] == "side"]
drinks = [item for item in menu if item["category"] == "drink"]

# Generate exactly 7 days starting from today
def get_seven_days():
    today = datetime.now()
    dates = []
    for i in range(7):
        current_date = today + timedelta(days=i)
        dates.append(current_date.strftime("%Y-%m-%d"))
    return dates

# Check if combo is valid
def is_valid_combo(combo):
    total_calories = sum(item["calories"] for item in combo)
    return 500 <= total_calories <= 800

# Check if three consecutive days have the same combo
def no_three_consecutive_same(schedule):
    for i in range(len(schedule) - 2):
        if schedule[i] == schedule[i + 1] == schedule[i + 2]:
            return False
    return True

# Calculate average popularity score for a combo
def avg_popularity(combo):
    return sum(item["popularity_score"] for item in combo) / len(combo)

# Generate meal schedule
def generate_schedule():
    dates = get_seven_days()
    schedule = []
    used_combos = set()
    
    for _ in dates:
        valid_combo = False
        attempts = 0
        max_attempts = 100
        
        while not valid_combo and attempts < max_attempts:
            combo = [
                random.choice(mains),
                random.choice(sides),
                random.choice(drinks)
            ]
            # Ensure unique dishes in combo
            if len(set(item["item_name"] for item in combo)) != 3:
                attempts += 1
                continue
            # Check calorie constraint
            if not is_valid_combo(combo):
                attempts += 1
                continue
            # Check if combo is unique
            combo_tuple = tuple(item["item_name"] for item in combo)
            if combo_tuple in used_combos:
                attempts += 1
                continue
            # Check popularity score (within 0.1 range of average)
            if schedule:
                avg_pop = avg_popularity(schedule[-1])
                if not (avg_pop - 0.1 <= avg_popularity(combo) <= avg_pop + 0.1):
                    attempts += 1
                    continue
            valid_combo = True
            used_combos.add(combo_tuple)
            schedule.append(combo)
        
        if not valid_combo:
            return None  # Failed to generate valid schedule
    
    # Check three consecutive days constraint
    if not no_three_consecutive_same([tuple(item["item_name"] for item in combo) for combo in schedule]):
        return None
    
    return list(zip(dates, schedule))

# Tkinter Frontend
class MealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Planner")
        
        # Generate schedule
        self.schedule = None
        while self.schedule is None:
            self.schedule = generate_schedule()
        
        # Create date picker for day selection
        self.day_label = tk.Label(root, text="Select Day:")
        self.day_label.pack(pady=5)
        
        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)
        self.date_entry.bind("<<DateEntrySelected>>", self.display_combo)
        
        # Create table for displaying combo
        self.tree = ttk.Treeview(root, columns=("Item", "Category", "Calories", "Taste", "Popularity"), show="headings")
        self.tree.heading("Item", text="Item Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Calories", text="Calories")
        self.tree.heading("Taste", text="Taste Profile")
        self.tree.heading("Popularity", text="Popularity Score")
        self.tree.pack(pady=20)
        
        # Display total calories
        self.total_calories_label = tk.Label(root, text="Total Calories: 0")
        self.total_calories_label.pack(pady=5)
        
        # Message for out-of-range dates
        self.message_label = tk.Label(root, text="")
        self.message_label.pack(pady=5)
        
        # Set default selection to today
        self.date_entry.set_date(datetime.now())
        self.display_combo(None)
    
    def display_combo(self, event):
        selected_day = self.date_entry.get_date().strftime("%Y-%m-%d")
        # Clear previous items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.message_label.config(text="")
        
        # Find combo for selected day
        for date, combo in self.schedule:
            if date == selected_day:
                total_calories = 0
                for item in combo:
                    self.tree.insert("", "end", values=(
                        item["item_name"],
                        item["category"],
                        item["calories"],
                        item["taste_profile"],
                        item["popularity_score"]
                    ))
                    total_calories += item["calories"]
                self.total_calories_label.config(text=f"Total Calories: {total_calories}")
                return
        
        # If no combo found for selected day
        self.total_calories_label.config(text="Total Calories: 0")
        self.message_label.config(text="No menu available for selected date")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()