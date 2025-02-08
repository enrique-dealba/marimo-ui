import marimo
import requests

__generated_with = "0.11.0"  # Adjust this as needed

app = marimo.App(width="medium")


# Cell 1: Import marimo as mo.
@app.cell
def __():
    import marimo as mo

    return (mo,)


# Cell 2: Display a title and brief instructions.
@app.cell
def __(mo):
    mo.md(
        r"""
        # MACHINA Spaceplan LLM

        Enter spaceplan objective:
        """
    )
    return


# Cell 3: Create a text-area form for user input.
@app.cell
def __(mo):
    # Create a text area (with placeholder text, label, and 5 rows) and wrap it in a form.
    return mo.ui.text_area(
        placeholder="Enter spaceplan objective...",
        label="Prompt",
        rows=5,
        full_width=True,
    ).form(submit_button_label="Submit")


# Cell 4: When the form is submitted, call the API and display its JSON response.
@app.cell
def __(input_text, mo):
    if not input_text:
        return mo.md("**Enter spaceplan objective.**")

    payload = {"text": input_text}
    try:
        response = requests.post(
            "http://localhost:8888/generate_full_objective", json=payload
        )
        response.raise_for_status()  # Raise an error for non-2xx responses.
        result = response.json()
        # Format the JSON result inside a code block.
        formatted_result = "```json\n" + str(result) + "\n```"
        return mo.md("### API Response\n" + formatted_result)
    except Exception as e:
        return mo.md("**Error calling API:** " + str(e))


if __name__ == "__main__":
    app.run()
