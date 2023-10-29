from rxconfig import config
from typing import List
import reflex as rx
from ml import test
from ml import filter_data

filename = f"{config.app_name}/{config.app_name}.py"
test_data: dict = test
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
    recommendation_list: List[filter_data.Recommendation]

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        # self.recommendation_list = give_recommendations(form_data['diet goal'], ...) --> list of Recommendation object
        self.recommendation_list = test.test(1,1,1)

def navbar():
    return rx.hstack(
        rx.hstack(
            rx.image(src="favicon.ico"),
            rx.heading("My App"),
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
        rx.text(value.protein),
        rx.text(value.fat),
        rx.text(value.carbs),
        border  = "1px solid white"
    )

def show_data_breakfast():
    return rx.vstack(
        rx.heading("Breakfast"),
        rx.foreach(
                FormState.recommendation_list, # list of objects
                show_value,
            ),
        width="100%"
    )

def show_data_lunch():
    return rx.vstack(
        rx.heading("Lunch"),
        rx.foreach(
                FormState.recommendation_list, # list of objects
                show_value,
            ),
        width="100%"
    )


def show_data_dinner():
    return rx.vstack(
        rx.heading("Dinner"),
        rx.foreach(
                FormState.recommendation_list, # list of objects
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
                    placeholder="Activity",
                    id="activity"
                ),
                rx.button("Submit", type_="submit"),
                
            ),
            on_submit=FormState.handle_submit,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.form_data.to_string()),
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
                show_data_breakfast(),
                show_data_lunch(),
                show_data_dinner(),
                overflow = 'hidden',
                width = "75%",
                bg="red"
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
