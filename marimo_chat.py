import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell
def _():
    import json

    import requests

    return json, requests


@app.cell
def _():
    print("MACHINA Spaceplan LLM")
    print("\nEnter spaceplan objective:")
    text = input()
    return (text,)


@app.cell
def _(json, requests, text):
    if text:
        try:
            response = requests.post(
                "http://localhost:8888/generate_full_objective", json={"text": text}
            )
            response.raise_for_status()
            result = response.json()
            print("API Response:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error calling API: {str(e)}")
    else:
        print("Please enter a spaceplan objective.")
    return response, result


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
