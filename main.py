from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import spacy

nlp = spacy.load("en_core_web_md")

# Sample dataset of recipes
RECIPES = {
    "pasta": "Boil pasta, add sauce, mix well, and serve.",
    "chicken curry": "Marinate chicken, cook with spices, add tomato puree, and simmer.",
    "paneer butter masala": "Cook paneer with butter, tomato sauce, and cream."
}

class ActionGenerateRecipe(Action):
    def name(self):
        return "action_generate_recipe"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text")
        doc = nlp(user_message)
        
        food_item = None
        for ent in doc.ents:
            if ent.label_ == "FOOD":  # Ensure spaCy recognizes food items
                food_item = ent.text.lower()
                break

        if not food_item:
            for word in user_message.split():
                if word.lower() in RECIPES:
                    food_item = word.lower()
                    break

        if food_item in RECIPES:
            dispatcher.utter_message(text=f"Here’s the recipe for {food_item}: {RECIPES[food_item]}")
        else:
            dispatcher.utter_message(text="Sorry, I don't have a recipe for that.")

        return []
    


    
