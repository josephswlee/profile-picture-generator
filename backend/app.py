from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import torch
from torch import autocast
from diffusers import DiffusionPipeline, UniPCMultistepScheduler
from PIL import Image
import logging

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

CORS(app)

# Configure the logging system to print to the terminal
logging.basicConfig(level=logging.DEBUG)

assert torch.cuda.is_available()



model_id = "runwayml/stable-diffusion-v1-5"
pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
# pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)

# pipeline.load_lora_weights(".", weight_name="majicmixRealistic_v6.safetensors")

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
    # image.save('test.png')
    
    return image


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # data = request.form['positivePrompts']

        positive_prompt = request.form["positivePrompts"]
        negative_prompt = request.form["negativePrompts"]
        app.logger.info("Image generation started.")
        image = run_inference(positive_prompt, negative_prompt)
        app.logger.info("Image generation done.")

        img_data = io.BytesIO()
        image.save(img_data, "PNG")
        img_data.seek(0)
        return send_file(img_data, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.logger.info("server starts")
    app.run(host='0.0.0.0', port=5000, debug=True)