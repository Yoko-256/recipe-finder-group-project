import json
from pathlib import Path
from typing import Dict, List

import streamlit as st

st.set_page_config(page_title="Recipe Finder", page_icon="🍳", layout="wide")

DATA_FILE = Path(__file__).with_name("recipes.json")

RESTRICTION_RULES = {
    "Vegetarian": {"exclude": ["chicken", "turkey", "beef", "pork", "fish", "shrimp", "salmon", "tuna"]},
    "Vegan": {"exclude": ["chicken", "turkey", "beef", "pork", "fish", "shrimp", "salmon", "tuna", "egg", "milk", "cheese", "butter", "yogurt", "honey"]},
    "Gluten-Free": {"exclude": ["pasta", "tortilla", "bread", "flour", "soy sauce", "gluten", "breadcrumbs", "ramen", "bagel"]},
    "Dairy-Free": {"exclude": ["milk", "cheese", "butter", "cream", "yogurt", "dairy", "mozzarella", "parmesan", "feta"]},
    "Egg-Free": {"exclude": ["egg", "mayonnaise"]},
    "Nut-Free": {"exclude": ["peanut", "almond", "walnut", "cashew", "pecan", "nut", "pesto"]},
}

ALL_MEAL_TYPES = ["All", "Breakfast", "Lunch", "Dinner", "Snack"]


@st.cache_data
def load_recipes() -> List[Dict]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE.name} was not found.")
    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = {
        "id",
        "title",
        "ingredients",
        "diet_tags",
        "allergen_tags",
        "meal_type",
        "cook_time",
        "difficulty",
        "image",
        "instructions",
    }

    for idx, recipe in enumerate(data, start=1):
        missing = required_keys - set(recipe.keys())
        if missing:
            raise ValueError(f"Recipe #{idx} is missing keys: {', '.join(sorted(missing))}")
    return data


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
    recipe_diet_tags = {item.lower() for item in recipe.get("diet_tags", [])}

    for restriction in restrictions:
        excluded = set(RESTRICTION_RULES[restriction]["exclude"])
        if recipe_ingredients & excluded:
            return True

        if restriction == "Vegetarian" and "vegetarian" not in recipe_diet_tags and recipe_ingredients & excluded:
            return True
        if restriction == "Vegan" and "vegan" not in recipe_diet_tags and recipe_ingredients & excluded:
            return True
        if restriction == "Gluten-Free" and ("gluten" in recipe_allergens or recipe_ingredients & excluded):
            return True
        if restriction == "Dairy-Free" and ("dairy" in recipe_allergens or recipe_ingredients & excluded):
            return True
        if restriction == "Egg-Free" and ("egg" in recipe_allergens or recipe_ingredients & excluded):
            return True
        if restriction == "Nut-Free" and ("nuts" in recipe_allergens or recipe_ingredients & excluded):
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


def find_recipes(
    recipes: List[Dict],
    available: List[str],
    restrictions: List[str],
    meal_type: str,
    keyword: str,
) -> List[Dict]:
    filtered = []
    keyword = keyword.strip().lower()

    for recipe in recipes:
        if meal_type != "All" and recipe["meal_type"] != meal_type:
            continue
        if keyword and keyword not in recipe["title"].lower():
            continue
        if violates_restrictions(recipe, restrictions):
            continue
        filtered.append(score_recipe(recipe, available))

    filtered.sort(key=lambda x: (x["score"], x["coverage"], -x["cook_time"]), reverse=True)
    return filtered


try:
    RECIPES = load_recipes()
except Exception as exc:
    st.error(f"Unable to load recipes.json: {exc}")
    st.stop()

st.title("Recipe Finder Demo App")
st.caption(
    "Enter ingredients you already have, choose food restrictions, and get recipe suggestions from a local dataset."
)

with st.sidebar:
    st.header("Search Settings")
    ingredient_text = st.text_area(
        "Available ingredients",
        placeholder="Example: rice, egg, garlic, broccoli, tomato",
        height=130,
    )
    keyword = st.text_input("Search recipe title", placeholder="Example: curry, pasta, tacos")
    selected_restrictions = st.multiselect(
        "Food restrictions",
        options=list(RESTRICTION_RULES.keys()),
    )
    selected_meal_type = st.selectbox(
        "Meal type",
        options=ALL_MEAL_TYPES,
    )
    show_only_good_matches = st.checkbox(
        "Show only recipes with at least 2 matching ingredients",
        value=False,
    )

available_ingredients = parse_ingredients(ingredient_text)
results = find_recipes(RECIPES, available_ingredients, selected_restrictions, selected_meal_type, keyword)

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
    st.warning("No matching recipes found. Try fewer restrictions, a different meal type, or a broader ingredient list.")
else:
    for recipe in results:
        with st.container(border=True):
            left, right = st.columns([1.05, 1.95])

            with left:
                st.image(recipe["image"], use_container_width=True)

            with right:
                st.subheader(recipe["title"])
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                meta_col1.write(f"**Meal type:** {recipe['meal_type']}")
                meta_col2.write(f"**Cook time:** {recipe['cook_time']} min")
                meta_col3.write(f"**Difficulty:** {recipe['difficulty']}")
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
