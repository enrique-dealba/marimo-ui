import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell
def _():
    import json
    import requests
    import marimo as mo
    return json, mo, requests


@app.cell
def _(mo):
    mo.md(
        """
        #MACHINA LLM Chat Test UI
        Examples:

        Make a new catalog maintenance for sensor RME01 with U markings and TEST mode

        Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours

        Search for target 28884 using sensor RME04
        """
    )
    return


@app.cell
def _(mo):
    form = mo.ui.text_area(placeholder="...").form()
    form
    return (form,)


@app.cell
def _(form, mo, requests):
    text = form.value
    result = None

    if text:
        try:
            with mo.status.spinner(subtitle="Thinking...") as spinner:
                response = requests.post(
                    "https://llm.openmachina.net/generate_full_objective",
                    json={"text": text},
                )
                response.raise_for_status()
                result = response.json()
        except Exception as e:
            result = f"Error calling API: {str(e)}"
    return response, result, spinner, text


@app.cell
def _(json, mo, result):
    mo.stop(result is None)

    editor = mo.ui.code_editor(
        value=json.dumps(result, indent=2),
        language="python"
    )
    editor
    return (editor,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
