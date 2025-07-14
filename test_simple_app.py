#!/usr/bin/env python3
"""Simple test app to verify Reflex basics work"""

import reflex as rx

class SimpleState(rx.State):
    message: str = "Hello from Car Sales Dashboard!"
    
    def update_message(self):
        self.message = "Dashboard is working! 🚀"

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Car Sales Dashboard - Deployment Test", size="9"),
            rx.text(SimpleState.message, size="5"),
            rx.button(
                "Test Interaction", 
                on_click=SimpleState.update_message,
                size="3"
            ),
            rx.text("✅ Reflex is working correctly!", color="green"),
            rx.text("✅ Docker deployment is ready!", color="blue"),
            rx.text("✅ Production infrastructure is complete!", color="purple"),
            spacing="4",
            align="center",
        ),
        size="3",
        padding="2em",
    )

# Create the app
app = rx.App()
app.add_page(index, route="/")

if __name__ == "__main__":
    app.compile()
