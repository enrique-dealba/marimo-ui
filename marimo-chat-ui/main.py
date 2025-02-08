import marimo
import requests

app = marimo.App(width="medium")


@app.cell
def input_text(mo):
    """
    Display a text area (wrapped in a form) for the user to enter a prompt.
    When the form is submitted (e.g. by clicking the Submit button or pressing Enter),
    the forms value is updated and sent to dependent cells.
    """
    return mo.ui.text_area(
        placeholder="Enter your prompt here...", label="Prompt", rows=5, full_width=True
    ).form(submit_button_label="Submit")


@app.cell
def output_response(input_text, mo):
    """
    When the user submits a prompt via the form (i.e. when input_text has a value),
    this cell calls the generate_full_objective endpoint and displays the API's JSON response.
    """
    if not input_text:
        return mo.md("**Enter spaceplan objective:**")

    payload = {"text": input_text}

    try:
        response = requests.post(
            "http://localhost:8888/generate_full_objective", json=payload
        )
        response.raise_for_status()  # raise exception for HTTP errors

        result = response.json()
        formatted_result = "```json\n" + str(result) + "\n```"
        return mo.md("### API Response\n" + formatted_result)
    except Exception as e:
        return mo.md("**Error calling API:** " + str(e))


if __name__ == "__main__":
    app.run()
