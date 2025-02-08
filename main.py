import marimo
import requests

__generated_with = "0.11.0"  # Adjust this as needed

app = marimo.App(width="medium")


# Cell 1: Import marimo as mo.
@app.cell
def cell1():
    import marimo as mo

    return mo


# Cell 2: Display instructions.
@app.cell
def cell2(mo):
    mo.md(
        """
        # MACHINA Spaceplan LLM

        Enter a prompt below and click **Submit** to call the `/generate_full_objective` endpoint.
        """
    )
    # No explicit return is needed here


# Cell 3: Create a text-area form for user input.
@app.cell
def cell3(mo):
    return mo.ui.text_area(
        placeholder="Enter your prompt here...", label="Prompt", rows=5, full_width=True
    ).form(submit_button_label="Submit")


# Cell 4: Process the input and call the API.
@app.cell
def cell4(input_text, mo):
    if not input_text:
        return mo.md("**Please enter a prompt and click Submit.**")

    payload = {"text": input_text}
    try:
        response = requests.post(
            "http://localhost:8888/generate_full_objective", json=payload
        )
        response.raise_for_status()  # Raise an error for HTTP error codes.
        result = response.json()
        formatted_result = "```json\n" + str(result) + "\n```"
        return mo.md("### API Response\n" + formatted_result)
    except Exception as e:
        return mo.md("**Error calling API:** " + str(e))


if __name__ == "__main__":
    app.run()
