from rxconfig import config
from typing import List
import re
import reflex as rx
from ml import filter_data, conversion2
from ml import llama_finetune

gender: List[str] = ["Male", "Female", "Other"]
fitness: List[str] = ["Fat Loss", "Maintenance", "Muscle Gain"]
diet: List[str] = ["Low-Fat", "Low-Carb", "Ketogenic (High Fat)"]
activity: List[str] = ["None: Desk Job etc.", "Light: sitting, standing, etc.", "Moderate: Lifting, continuous activity, etc.", "Cardio/Sports: couple hours a day", "Heavy: very strenuous exercise daily"]

breakfast_path = "/Users/krish/Downloads/filtered_data_breakfast.csv"
lunch_path = "/Users/krish/Downloads/filtered_data_lunch.csv"
dinner_path = "/Users/krish/Downloads/filtered_data_dinner.csv"

filename = f"{config.app_name}/{config.app_name}.py"
style = {
    "color": "black",
    ".some-css-class": {
        "text_decoration": "underline",
    },
    rx.Input: {
        "color": "black", 
        "border": "1px solid black"
    },
    rx.Select: {
        "color": "black", 
        "border": "1px solid black"
    },
    rx.Text: {
        "font_family": "Comic Sans MS",
        "color": "black", 
    },
    rx.Divider: {
        "margin_bottom": "3em", 
        "margin_top": "0.5em",  
    },
    rx.Heading: {
        "font_weight": "500",  
        "color": "black",  
    },
}

class State(rx.State):
    gender: str = "No selection yet"
    fitness: str = "No selection yet"
    diet: str = "No selection yet"
    activity: str = "No selection yet"
    
    form_data: dict = {}
    
    show: bool = False

    ai_output: List[float]

    
    breakfast_list: List[filter_data.Recommendation]
    lunch_list: List[filter_data.Recommendation]
    dinner_list: List[filter_data.Recommendation]

    breakfast_names: List[str]
    lunch_names: List[str]
    dinner_names: List[str]
    #macro_recs = List[filter_data.Recommendation]

    def change(self):
        self.show = not (self.show)

    def handle_submit(self, form_data: dict):
        self.change()
        self.form_data = form_data
        cal_intake, protein, fat, carbs = conversion2.convert(form_data["weight"], form_data["height"], form_data["age"], form_data["sex"], form_data["fitness"], form_data["diet"], form_data["activity"])
        #self.macro_recs = [filter_data.Recommendation(calories=cal_intake, protein=protein, fat=fat, carbs=carbs)]
        cal_intake /= 3.0
        protein /= 3.0
        fat /= 3
        carbs /= 3

        self.breakfast_list = filter_data.load_data(breakfast_path, cal_intake, protein, fat, carbs)
        self.lunch_list = filter_data.load_data(lunch_path, cal_intake, protein, fat, carbs)
        self.dinner_list = filter_data.load_data(dinner_path, cal_intake, protein, fat, carbs)

        # shortens the names
        for i in range(len(self.breakfast_list)):
            self.breakfast_names.append(self.breakfast_list[i].name)
            # i.name = llama_finetune.get_shortened_name(i.name)

        for i in range(len(self.lunch_list)):
            self.lunch_names.append(self.lunch_list[i].name)
            # i.name = llama_finetune.get_shortened_name(i.name)

        for i in range(len(self.dinner_list)):
            self.dinner_names.append(self.dinner_list[i].name)
            # i.name = llama_finetune.get_shortened_name(i.name)
    
    def generate_breakfast(self):
        input = ""
        for i in range(len(self.breakfast_names)):
            input += f"{i+1}. {self.breakfast_names[i]}, "
        output = llama_finetune.get_additional_recs(input)
        pattern = r'\d+\.\s+([^\d,]+)'
        matches = re.findall(pattern, output)

        for match in matches:
            match.strip()

        element_list = [match.strip() for match in matches]
        self.breakfast_names.append(i for i in element_list)
    
    def generate_lunch(self):
        input = ""
        for i in range(len(self.lunch_names)):
            input += f"{i+1}. {self.lunch_names[i]}, "
        output = llama_finetune.get_additional_recs(input)
        pattern = r'\d+\.\s+([^\d,]+)'
        matches = re.findall(pattern, output)

        for match in matches:
            match.strip()

        element_list = [match.strip() for match in matches]
        self.lunch_names.append(i for i in element_list)
    
    def generate_dinner(self):
        input = ""
        for i in range(len(self.dinner_names)):
            input += f"{i+1}. {self.dinner_names[i]}, "
        output = llama_finetune.get_additional_recs(input)
        pattern = r'\d+\.\s+([^\d,]+)'
        matches = re.findall(pattern, output)

        for match in matches:
            match.strip()

        element_list = [match.strip() for match in matches]
        self.dinner_names.append(i for i in element_list)


def navbar():
    return rx.vstack(
        rx.markdown("## DieTune!"),
        # rx.text("Based on basic biometric information, fitness/diet goals, and daily excercise, our app provides a detailed dietary plan for you.", as_="i", margin="auto"),
        bg="#d3d3d3",
        color="black",
        margin="auto",
        position="fixed",
        top="0px",
        z_index="5",
        width="100%",
        border_bottom="1px solid black"
    )

# TODO: SHOW ERROR FOODS
def show_value(value):
    return rx.vstack(
        rx.text(value.name, font_size="10px"),
        rx.text(f"Protein (g): {value.protein}", font_size="8px"),
        rx.text(f"Fat (g): {value.fat}", font_size="8px"),
        rx.text(f"Carbs (g): {value.carbs}", font_size="8px"),
        rx.text(f"Error %: {value.error}", font_size="8px"),
        width = "200px",
        height = "100px",
        color = "black",
        border = "1px solid black",
        border_radius = "md"
    )

def show_breakfast():
    return rx.vstack(
        rx.heading(
            "Breakfast",
        ),
        rx.foreach(
                State.breakfast_list, # list of objects
                show_value,
        ),
        rx.button(
            "Generate More",
            bg="#fef2f2",
            color="#b91c1c",
            border_radius="lg",
            on_click=State.generate_breakfast,
        ),
        width="100%"
    )

def show_lunch():
    return rx.vstack(
        rx.heading("Lunch"),
        rx.foreach(
                State.lunch_list, # list of objects
                show_value,
        ),
        rx.button(
            "Generate More",
            bg="#fef2f2",
            color="#b91c1c",
            border_radius="lg",
            on_click=State.generate_lunch,
        ),
        width="100%"
    )

def show_dinner():
    return rx.vstack(
        rx.heading("Dinner"),
        rx.foreach(
                State.dinner_list, # list of objects
                show_value,
            ),
        rx.button(
            "Generate More",
            bg="#fef2f2",
            color="#b91c1c",
            border_radius="lg",
            on_click=State.generate_dinner,
        ),
        width="100%"
    )

def form():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.heading("Biometric Information", size="lg", margin="10px"),
                rx.input(
                    placeholder="Weight",
                    id="weight"
                ),
                rx.input(
                    placeholder="Height",
                    id="height"
                ),
                rx.input(
                    placeholder="Age",
                    id="age"
                ),
                rx.select(
                    gender,
                    placeholder="Gender",
                    id="sex",
                    color_schemes="twitter",
                ),
                rx.select(
                    fitness,
                    placeholder="Fitness Goal",
                    id="fitness",
                    color_schemes="twitter",
                ),
                rx.select(
                    diet,
                    placeholder="Diet Goal",
                    id="diet",
                    color_schemes="twitter",
                ),
                rx.select(
                    activity,
                    placeholder="Activity Goal",
                    id="activity",
                    color_schemes="twitter",
                ),
                rx.button("Submit", type_="submit"),
            ),
            on_submit=State.handle_submit,
        ),
        rx.divider(),
        # TODO: DISPLAY MACRONUTRIENTS

        rx.heading("Macronutrient Recommendation", size="sm"),
        # rx.text(f"Calorie intake: {State.macro_recs[0].calories}\nProtein intake: {FormState.macro_recs[0].protein}\nFat intake: {FormState.macro_recs[0].fat}\nCarbs intake: {FormState.macro_recs[0].carbs}"),
        color = 'black',
        bg = '#eeeee4',
        size = '30px',
        height = "100%",
        margin = "20px",
        padding = "30px",
        align_items="top",
        width = "30%",
        radius = "10px",
        border = "3px solid black",
        border_radius= "lg",
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
                width = "70%",
            ),
            width="100%"
        ),
        padding_top ="5em",
        width ="100%",
        color="black"
    )

# TODO: DISPLAY LOADING SIGN OR SOME SORT OF MODAL
rx.box(
    rx.button("Confirm", on_click=State.change),
    rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Loading..."),
                rx.modal_body(
                    "This may take a few seconds..."
                ),
                rx.modal_footer(
                    rx.button(
                        "Close", on_click=State.change
                    )
                ),
            )
        ),
        is_open=State.show,
    ),
)

# app = rx.App(style=style)
app = rx.App(style=style)
app.add_page(index)
app.compile() 
