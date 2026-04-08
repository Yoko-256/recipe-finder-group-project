import streamlit as st
from typing import List, Dict

st.set_page_config(page_title="Recipe Finder", page_icon="🍳", layout="wide")

RECIPES: List[Dict] = [
    {
        "id": 1,
        "title": "Vegetable Fried Rice",
        "ingredients": ["rice", "egg", "carrot", "peas", "soy sauce", "garlic", "green onion", "oil"],
        "diet_tags": ["vegetarian"],
        "allergen_tags": ["egg", "soy"],
        "meal_type": "Dinner",
        "cook_time": 20,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Heat oil in a pan and cook garlic briefly.",
            "Add carrot and peas, then stir-fry until slightly softened.",
            "Add rice and soy sauce, and mix well.",
            "Push rice aside, scramble egg, then mix everything together.",
            "Top with green onion and serve."
        ]
    },
    {
        "id": 2,
        "title": "Chicken Broccoli Stir-Fry",
        "ingredients": ["chicken", "broccoli", "garlic", "soy sauce", "cornstarch", "oil", "ginger"],
        "diet_tags": ["high-protein"],
        "allergen_tags": ["soy"],
        "meal_type": "Dinner",
        "cook_time": 25,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Cook chicken in a hot pan until lightly browned.",
            "Add garlic, ginger, and broccoli.",
            "Pour in soy sauce mixture and cook until glossy.",
            "Serve hot with rice if desired."
        ]
    },
    {
        "id": 3,
        "title": "Vegan Tomato Pasta",
        "ingredients": ["pasta", "tomato", "garlic", "olive oil", "basil", "onion"],
        "diet_tags": ["vegan"],
        "allergen_tags": ["gluten"],
        "meal_type": "Dinner",
        "cook_time": 18,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Cook pasta according to package directions.",
            "Saute onion and garlic in olive oil.",
            "Add tomato and simmer into a quick sauce.",
            "Toss with pasta and basil, then serve."
        ]
    },
    {
        "id": 4,
        "title": "Gluten-Free Chicken Lettuce Wraps",
        "ingredients": ["chicken", "lettuce", "carrot", "garlic", "ginger", "tamari", "green onion"],
        "diet_tags": ["gluten-free", "dairy-free"],
        "allergen_tags": ["soy"],
        "meal_type": "Lunch",
        "cook_time": 20,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Cook chicken with garlic and ginger.",
            "Add carrot and tamari, then stir until combined.",
            "Spoon mixture into lettuce leaves.",
            "Top with green onion and serve."
        ]
    },
    {
        "id": 5,
        "title": "Oat Banana Pancakes",
        "ingredients": ["oats", "banana", "egg", "milk", "baking powder", "cinnamon"],
        "diet_tags": ["vegetarian"],
        "allergen_tags": ["egg", "dairy"],
        "meal_type": "Breakfast",
        "cook_time": 15,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Blend oats, banana, egg, milk, and baking powder.",
            "Pour batter onto a hot pan.",
            "Cook both sides until golden.",
            "Serve with fruit or syrup."
        ]
    },
    {
        "id": 6,
        "title": "Chickpea Salad Bowl",
        "ingredients": ["chickpeas", "cucumber", "tomato", "olive oil", "lemon", "lettuce", "onion"],
        "diet_tags": ["vegan", "gluten-free", "dairy-free"],
        "allergen_tags": [],
        "meal_type": "Lunch",
        "cook_time": 10,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Combine chickpeas and chopped vegetables in a bowl.",
            "Dress with olive oil and lemon.",
            "Toss gently and serve chilled or at room temperature."
        ]
    },
    {
        "id": 7,
        "title": "Tofu Vegetable Curry",
        "ingredients": ["tofu", "coconut milk", "curry paste", "broccoli", "carrot", "onion", "garlic"],
        "diet_tags": ["vegan", "dairy-free"],
        "allergen_tags": ["soy"],
        "meal_type": "Dinner",
        "cook_time": 30,
        "difficulty": "Medium",
        "image": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Cook onion and garlic until fragrant.",
            "Add curry paste and stir briefly.",
            "Add tofu, vegetables, and coconut milk.",
            "Simmer until vegetables are tender and serve."
        ]
    },
    {
        "id": 8,
        "title": "Turkey Avocado Wrap",
        "ingredients": ["tortilla", "turkey", "avocado", "lettuce", "tomato", "mustard"],
        "diet_tags": ["high-protein"],
        "allergen_tags": ["gluten"],
        "meal_type": "Lunch",
        "cook_time": 8,
        "difficulty": "Easy",
        "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=1200&q=80",
        "instructions": [
            "Lay out tortilla and spread mustard.",
            "Add turkey, avocado, lettuce, and tomato.",
            "Roll tightly, slice, and serve."
        ]
    }
]

RESTRICTION_RULES = {
    "Vegetarian": {"exclude": ["chicken", "turkey", "beef", "pork", "fish", "shrimp"]},
    "Vegan": {"exclude": ["chicken", "turkey", "beef", "pork", "fish", "shrimp", "egg", "milk", "cheese", "butter", "yogurt", "honey"]},
    "Gluten-Free": {"exclude": ["pasta", "tortilla", "bread", "flour", "soy sauce", "gluten"]},
    "Dairy-Free": {"exclude": ["milk", "cheese", "butter", "cream", "yogurt", "dairy"]},
    "Egg-Free": {"exclude": ["egg"]},
    "Nut-Free": {"exclude": ["peanut", "almond", "walnut", "cashew", "pecan", "nut"]}
}


def parse_ingredients(text: str) -> List[str]:
    raw = text.replace("\n", ",").split(",")
    cleaned = []
    for item in raw:
        value = item.strip().lower()
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned


def violates_restrictions(recipe: Dict, restrictions: List[str]) -> bool:
    recipe_ingredients = {item.lower() for item in recipe["ingredients"]}
    recipe_allergens = {item.lower() for item in recipe.get("allergen_tags", [])}

    for restriction in restrictions:
        excluded = set(RESTRICTION_RULES[restriction]["exclude"])
        if recipe_ingredients & excluded:
            return True
        if restriction == "Gluten-Free" and "gluten" in recipe_allergens:
            return True
        if restriction == "Dairy-Free" and "dairy" in recipe_allergens:
            return True
        if restriction == "Egg-Free" and "egg" in recipe_allergens:
            return True
    return False


def score_recipe(recipe: Dict, available: List[str]) -> Dict:
    recipe_ingredients = [item.lower() for item in recipe["ingredients"]]
    available_set = set(available)

    matched = [item for item in recipe_ingredients if item in available_set]
    missing = [item for item in recipe_ingredients if item not in available_set]
    score = len(matched)
    coverage = len(matched) / len(recipe_ingredients) if recipe_ingredients else 0

    result = dict(recipe)
    result["matched"] = matched
    result["missing"] = missing
    result["score"] = score
    result["coverage"] = coverage
    return result


def find_recipes(available: List[str], restrictions: List[str], meal_type: str) -> List[Dict]:
    filtered = []
    for recipe in RECIPES:
        if meal_type != "All" and recipe["meal_type"] != meal_type:
            continue
        if violates_restrictions(recipe, restrictions):
            continue
        filtered.append(score_recipe(recipe, available))

    filtered.sort(key=lambda x: (x["score"], x["coverage"], -x["cook_time"]), reverse=True)
    return filtered


st.title("Recipe Finder Demo App")
st.caption("Enter available ingredients, choose food restrictions, and get recipe suggestions from a local demo dataset.")

with st.sidebar:
    st.header("Search Settings")
    ingredient_text = st.text_area(
        "Available ingredients",
        placeholder="Example: rice, egg, garlic, broccoli, tomato"
    )
    selected_restrictions = st.multiselect(
        "Food restrictions",
        options=list(RESTRICTION_RULES.keys())
    )
    selected_meal_type = st.selectbox(
        "Meal type",
        options=["All", "Breakfast", "Lunch", "Dinner"]
    )
    show_only_good_matches = st.checkbox("Show only recipes with at least 2 matching ingredients", value=False)

available_ingredients = parse_ingredients(ingredient_text)
results = find_recipes(available_ingredients, selected_restrictions, selected_meal_type)

if show_only_good_matches:
    results = [recipe for recipe in results if recipe["score"] >= 2]

col1, col2, col3 = st.columns(3)
col1.metric("Recipes in dataset", len(RECIPES))
col2.metric("Ingredients entered", len(available_ingredients))
col3.metric("Matching recipes", len(results))

if available_ingredients:
    st.write("**Your ingredients:**", ", ".join(available_ingredients))
else:
    st.info("Add some ingredients in the sidebar to get more personalized matches.")

if not results:
    st.warning("No matching recipes found. Try fewer restrictions or a broader ingredient list.")
else:
    for recipe in results:
        with st.container(border=True):
            left, right = st.columns([1.1, 1.9])

            with left:
                st.image(recipe["image"], use_container_width=True)

            with right:
                st.subheader(recipe["title"])
                st.write(f"**Meal type:** {recipe['meal_type']}  ")
                st.write(f"**Cook time:** {recipe['cook_time']} min  ")
                st.write(f"**Difficulty:** {recipe['difficulty']}  ")
                st.write(f"**Match score:** {recipe['score']} / {len(recipe['ingredients'])}")

                if recipe["matched"]:
                    st.success("You already have: " + ", ".join(recipe["matched"]))
                if recipe["missing"]:
                    st.info("You still need: " + ", ".join(recipe["missing"]))

                tags = recipe.get("diet_tags", [])
                if tags:
                    st.write("**Tags:** " + ", ".join(tags))

                with st.expander("See full ingredients and steps"):
                    st.write("**Ingredients:**")
                    st.write(", ".join(recipe["ingredients"]))
                    st.write("**Instructions:**")
                    for idx, step in enumerate(recipe["instructions"], start=1):
                        st.write(f"{idx}. {step}")

st.markdown("---")
st.markdown(
    "This demo uses a curated local dataset instead of a live recipe API, which makes the final presentation more stable and avoids personal API ownership issues."
)
