from flask import Flask, request, jsonify
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = Flask(__name__)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)
model.eval()


@app.route("/generate", methods=["POST"])
async def generate():
    content = request.get_json()
    prompt = content["prompt"]
    length = content["length"]
    temperature = content["temperature"]

    prompt_tokens = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate text
    output = model.generate(prompt_tokens, max_length=length, temperature=temperature)

    # Decode output and return as response
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return jsonify({"output": output_text})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
