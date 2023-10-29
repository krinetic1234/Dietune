from rxconfig import config
from typing import List
import reflex as rx
from ml import filter_data, conversion2

options: List[str] = "Male", "Female"
breakfast_path = "/Users/jaibhatia/Desktop/filtered_data_breakfast.csv"
lunch_path = "/Users/jaibhatia/Desktop/filtered_data_lunch.csv"
dinner_path = "/Users/jaibhatia/Desktop/filtered_data_dinner.csv"

filename = f"{config.app_name}/{config.app_name}.py"
style = {
    "background": "black",
    "color": "red",
    "::selection": {
        "background_color": "#4a90e2", 
    },
    ".some-css-class": {
        "text_decoration": "underline",
    },
    "#special-input": {"width": "20vw"}, 
    rx.Input: {
        "color": "red", 
    },
    rx.Text: {
        "font_family": "Comic Sans MS",
        "color": "red", 
    },
    rx.Divider: {
        "margin_bottom": "1em", 
        "margin_top": "0.5em",  
    },
    rx.Heading: {
        "font_weight": "500",  
        "color": "#ffffff",  
    },
    rx.Code: {
        "color": "#4a90e2",  
        "background_color": "#1e1e1e",
        "border_radius": "4px", 
        "padding": "0.5em",  
    },
}


class FormState(rx.State):
    form_data: dict = {}
    breakfast_list: List[filter_data.Recommendation]
    lunch_list: List[filter_data.Recommendation]
    dinner_list: List[filter_data.Recommendation]
    #macro_recs = List[filter_data.Recommendation]

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        cal_intake, protein, fat, carbs = conversion2.convert(form_data["weight"], form_data["height"], form_data["age"], form_data["sex"], form_data["fitness_goal"], form_data["diet_goal"], form_data["activity_goal"])
        #self.macro_recs = [filter_data.Recommendation(calories=cal_intake, protein=protein, fat=fat, carbs=carbs)]
        cal_intake /= 3.0
        protein /= 3.0
        fat /= 3
        carbs /= 3
        self.breakfast_list = filter_data.load_data(breakfast_path, cal_intake, protein, fat, carbs)
        self.lunch_list = filter_data.load_data(lunch_path, cal_intake, protein, fat, carbs)
        self.dinner_list = filter_data.load_data(dinner_path, cal_intake, protein, fat, carbs)

def navbar():
    return rx.hstack(
        rx.hstack(
            rx.image(src="favicon.ico"),
            rx.heading("Dietune"),
        ),
        rx.spacer(),
        rx.menu(
            rx.menu_button("Menu"),
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="5",
        border_bottom="1px solid white"
    )

def show_value(value):
    return rx.vstack(
        rx.text(value.name, font_size="2em"),
        rx.text(f"Protein (g): {value.protein}"),
        rx.text(f"Fat (g): {value.fat}"),
        rx.text(f"Carbs (g): {value.carbs}"),
        rx.text(f"Error %: {value.error}"),
        border = "1px solid white"
    )

def show_breakfast():
    return rx.vstack(
        rx.heading("Breakfast"),
        rx.foreach(
                FormState.breakfast_list, # list of objects
                show_value,
            ),
        width="100%"
    )


def show_lunch():
    return rx.vstack(
        rx.heading("Lunch"),
        rx.foreach(
                FormState.lunch_list, # list of objects
                show_value,
            ),
        width="100%"
    )

def show_dinner():
    return rx.vstack(
        rx.heading("Dinner"),
        rx.foreach(
                FormState.dinner_list, # list of objects
                show_value,
            ),
        width="100%"
    )


def form():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Weight",
                    id="weight",
                ),
                rx.input(
                    placeholder="Height",
                    id="height"
                ),
                rx.input(
                    placeholder="Age",
                    id="age"
                ),
                rx.input(
                    placeholder="Sex",
                    id="sex"
                ),
                rx.input(
                    placeholder="Fitness Goal",
                    id="fitness_goal"
                ),
                rx.input(
                    placeholder="Diet Goal",
                    id="diet_goal"
                ),
                rx.input(
                    placeholder="Activity Goal",
                    id="activity_goal"
                ),
                rx.button("Submit", type_="submit"),
            ),
            on_submit=FormState.handle_submit,
        ),
        rx.divider(),
        rx.heading("Macronutrient Recommendation"),
        # cal_intake, protein, fat, carbs
        #rx.text(f"Calorie intake: {FormState.macro_recs[0].calories}\nProtein intake: {FormState.macro_recs[0].protein}\nFat intake: {FormState.macro_recs[0].fat}\nCarbs intake: {FormState.macro_recs[0].carbs}"),
        color='white',
        size='3px',
        height="100%",
        align_items="top",
        bg = "gray",
        width = "25%"
    )


@rx.page(title='Dietune')
def index():
    return rx.vstack(
        navbar(),
        rx.hstack(
            form(),
            rx.hstack(
                show_breakfast(),
                show_lunch(),
                show_dinner(),
                overflow = 'hidden',
                width = "75%",
            ),
            width="100%",
            bg= "green"
        ),
        padding_top ="5em",
        width ="100%",
        
    )

app = rx.App(style=style)
app.add_page(index)
app.compile() 
