import base64, requests, json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama_with_image(image_path, prompt):
    # Encode image to base64
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": "llava",  # make sure you've run: ollama pull llava
        "prompt": prompt,
        "images": [img_base64]
    }

    # Send to Ollama
    resp = requests.post(OLLAMA_URL, json=payload, stream=True)
    resp.raise_for_status()

    # Ollama streams JSONL responses
    output = ""
    for line in resp.iter_lines():
        if line:
            obj = json.loads(line)
            output += obj.get("response", "")
    return output.strip()