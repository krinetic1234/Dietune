"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"
rx.toggle_color_mode


class FormState(rx.State):

    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        self.form_data = form_data


def index():
    return rx.vstack(
        rx.toggle_color_mode,
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
        rx.text(FormState.form_data["weight"])
    )

app = rx.App()
app.add_page(index)
app.compile()
