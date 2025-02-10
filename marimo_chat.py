import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import httpx
    import json
    import traceback
    return httpx, json, mo, traceback


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # MACHINA Objective ChatBot

        This chatbot will assist you in submitting a MACHINA objective.
        """
    )
    return


@app.cell
def _(mo):
    MODE_PROMPT = "prompt"
    MODE_DECISION = "decision"
    MODE_DONE = "done"

    get_mode, set_mode = mo.state(MODE_PROMPT)
    return MODE_DECISION, MODE_DONE, MODE_PROMPT, get_mode, set_mode


@app.cell
def _(
    MODE_DECISION,
    MODE_DONE,
    MODE_PROMPT,
    get_mode,
    httpx,
    json,
    mo,
    set_mode,
    traceback,
):
    def _submit_objective(messages):
        set_mode(MODE_DONE)
        return f"Objective submitted! Please refresh page to start a new objective."


    def _query_llm(messages, config):
        # Combine the content of all messages where role == 'user'
        user_messages = [message.content for message in messages if message.role == "user"]
        combined_message = "\n".join(user_messages)
        print("_query_llm combined_message():", combined_message)

        try:
            response = httpx.post(
                "https://llm.openmachina.net/generate_full_objective",
                json={"text": combined_message},
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            print(traceback.format_exc())
            return mo.md(
                f"Sorry, I'm experimental and error {str(e)} occurred. Please try again."
            )

        # show llm json
        editor = mo.ui.code_editor(value=json.dumps(result, indent=2), language="python")

        # set mode to decision and ask user to submit
        set_mode(MODE_DECISION)
        return mo.vstack(
            [editor, mo.md("I've configured this objective. Do you want to submit it?")]
        )


    def _parse_decision(messages, config):
        message = messages[-1].content.lower()

        if message == "yes" or message == "y":
            return _submit_objective(messages)
        elif message == "no" or message == "n":
            set_mode(MODE_PROMPT)
            return f"Please continue to refine your objective. Refresh the page to start over."
        else:
            return f"Please response yes or no. Thank you."


    def _chat_model(messages, config):
        if get_mode() == MODE_PROMPT:
            return _query_llm(messages, config)
        elif get_mode() == MODE_DECISION:
            return _parse_decision(messages, config)
        elif get_mode() == MODE_DONE:
            return f"Please refresh page to start a new objective."
        else:
            return f"I've encountered an internal error. Please refresh the page. Sorry!"


    chatbot = mo.ui.chat(
        _chat_model,
        prompts=[
            "Make a new catalog maintenance for sensor RME01 with U markings and TEST mode",
            "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours",
            "Search for target 28884 using sensor RME04",
        ],
        show_configuration_controls=False,
    )
    chatbot
    return (chatbot,)


@app.cell
def _(MODE_DONE, chatbot, get_mode):
    # chatbot.value is the list of chat messages
    if get_mode() == MODE_DONE:
        # this doesn't work, so we need to tell the user to refresh the page
        # chatbot._chat_history.clear()
        # set_mode(MODE_PROMPT)
        chatbot.value
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
