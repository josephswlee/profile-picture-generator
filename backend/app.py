from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, UniPCMultistepScheduler
from diffusers import (
    DDPMScheduler,
    DDIMScheduler,
    PNDMScheduler,
    LMSDiscreteScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
    DPMSolverSDEScheduler,
)
from PIL import Image
import random
import logging
import os

# Get the current directory of the 'app.py' script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up to reach the parent folder ('project_root')
parent_dir = os.path.dirname(current_dir)

# Combine the path to the 'models/checkpoints' folder
checkpoint_folder = os.path.join(parent_dir, "majicmixRealistic_v6.safetensors")

# pt_state_dict = safetensors.torch.load_file(checkpoint_folder, device="cpu")
# torch.save(pt_state_dict, "pt_state_dict.bin")


app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

CORS(app)

# Configure the logging system to print to the terminal
logging.basicConfig(level=logging.DEBUG)

assert torch.cuda.is_available()


model_id = "runwayml/stable-diffusion-v1-5"
# pipeline = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

pipeline = StableDiffusionPipeline.from_single_file(
    checkpoint_folder,
    torch_dtype=torch.float16,
    scheduler_type = "dpm",
    load_safety_checker = False,
    use_safetensors=True
)
pipeline.to("cuda")

# pipeline.unet.load_attn_procs("pt_state_dict.bin")
# pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)

# load lora weights
lora_path = '../models/lora'
pipeline.load_lora_weights(lora_path, weight_name="mix4.safetensors", local_files_only=True)
pipeline.load_lora_weights(lora_path, weight_name="AI_hh-ka.safetensors", local_files_only=True)
pipeline.load_lora_weights(lora_path, weight_name="Droste_Effect.safetensors", local_files_only=True)
pipeline.load_lora_weights(lora_path, weight_name="ClothingAdjuster2.safetensors", local_files_only=True)
pipeline.load_lora_weights(lora_path, weight_name="more_details.safetensors", local_files_only=True)
pipeline.load_lora_weights(lora_path, weight_name="add_detail.safetensors", local_files_only=True)

def get_pipeline_embeds(pipeline, prompt, negative_prompt, device):
    """ Get pipeline embeds for prompts bigger than the maxlength of the pipe
    :param pipeline:
    :param prompt:
    :param negative_prompt:
    :param device:
    :return:
    """
    max_length = pipeline.tokenizer.model_max_length

    # simple way to determine length of tokens
    # count_prompt = len(prompt.split(" "))
    # count_negative_prompt = len(negative_prompt.split(" "))
    # app.logger.info("count_p: %d", count_prompt)
    # app.logger.info("count_np: %d", count_negative_prompt)

    input_ids = pipeline.tokenizer(prompt, return_tensors="pt", truncation=False).input_ids.to(device)
    app.logger.info("input shape: %d", input_ids.shape[-1])

    negative_ids = pipeline.tokenizer(negative_prompt, return_tensors="pt", truncation=False).input_ids.to(device)
    app.logger.info("negative shape: %d", negative_ids.shape[-1])


    # create the tensor based on which prompt is longer
    if input_ids.shape[-1] >= negative_ids.shape[-1]:
        input_ids = pipeline.tokenizer(prompt, return_tensors="pt", truncation=False).input_ids.to(device)
        shape_max_length = input_ids.shape[-1]
        negative_ids = pipeline.tokenizer(negative_prompt, truncation=False, padding="max_length",
                                          max_length=shape_max_length, return_tensors="pt").input_ids.to(device)

    else:
        negative_ids = pipeline.tokenizer(negative_prompt, return_tensors="pt", truncation=False).input_ids.to(device)
        shape_max_length = negative_ids.shape[-1]
        input_ids = pipeline.tokenizer(prompt, return_tensors="pt", truncation=False, padding="max_length",
                                       max_length=shape_max_length).input_ids.to(device)

    concat_embeds = []
    neg_embeds = []
    for i in range(0, shape_max_length, max_length):
        concat_embeds.append(pipeline.text_encoder(input_ids[:, i: i + max_length])[0])
        neg_embeds.append(pipeline.text_encoder(negative_ids[:, i: i + max_length])[0])
    app.logger.info("shape_max_length: %d", shape_max_length)
    app.logger.info("max_length: %d", max_length)
    return torch.cat(concat_embeds, dim=1), torch.cat(neg_embeds, dim=1)

def run_inference(positive_prompt, negative_prompt):
    try:
        image = pipeline(
        prompt_embeds=positive_prompt,
        negative_prompt_embeds=negative_prompt,
        # prompt=positive_prompt,
        # negative_prompt=negative_prompt,
        width=512,
        height=512,
        num_inference_steps=25,
        num_images_per_prompt=1,
        generator=torch.manual_seed(random.randint(1, 10000)),
        ).images[0]
        # image.save('test.png')
        
        return image
    except Exception as e:
        app.logger.info(e)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # data = request.form['positivePrompts']

        positive_prompt = request.form["positivePrompts"]
        negative_prompt = request.form["negativePrompts"]
        # app.logger.info("Image generation started.")
        # image = run_inference(positive_prompt, negative_prompt)
        # app.logger.info("Image generation done.")

        app.logger.info("Image embedding started.")
        positive_embeds, negative_embeds = get_pipeline_embeds(pipeline, 
                                                               positive_prompt,
                                                               negative_prompt,
                                                               "cuda")
        app.logger.info(positive_embeds.shape)
        app.logger.info(negative_embeds.shape)
        app.logger.info("Image embedding done.")

        app.logger.info("Image generation started.")
        image = run_inference(positive_embeds, negative_embeds)
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