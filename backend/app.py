from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

CORS(app)

assert torch.cuda.is_available()

model_id = "runwayml/stable-diffusion-v1-5"
pipeline = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

pipeline.load_lora_weights("../models/checkpoints", weight_name="howls_moving_castle.safetensors")

def run_inference(positive_prompt, negative_prompt):
    image = pipeline(
    prompt=positive_prompt,
    negative_prompt=negative_prompt,
    width=512,
    height=512,
    num_inference_steps=25,
    num_images_per_prompt=1,
    generator=torch.manual_seed(0),
    ).images[0]

    # with autocast("cuda"):
    #     image = pipel(prompt)["sample"][0]  
    img_data = io.BytesIO()
    image.save(img_data, "PNG")
    img_data.seek(0)
    return img_data

# def image_grid(imgs, rows=1, cols=2):
#     w, h = imgs[0].size
#     grid = Image.new("RGB", size=(cols * w, rows * h))

#     for i, img in enumerate(imgs):
#         grid.paste(img, box=(i % cols * w, i // cols * h))
#     return grid


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.form['positivePrompts']
        prompt = request.args["prompt"]
        img_data = run_inference(prompt)
        return send_file(img_data, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)