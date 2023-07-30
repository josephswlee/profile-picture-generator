# Readme.md

# Profile Picture Generator

## ****Overview****

This ongoing project aims to provide students and young professionals with a free and accessible tool to generate or enhance their professional profile pictures without any cost or the need to visit a store.

## ****Getting Started****

### **Prerequisites**

Virtual environment (conda or venv) with python version 3.10.6

[requirements.txt](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/15b1af18-6aa9-4233-9fa5-3e2cc0726177/requirements.txt)

### **Installation**

1. Clone the repository to your local machine.
    
    ```bash
    git clone https://github.com/your_username/your_project.git
    ```
    
2. 
npm install

## Background

### What is Stable Diffusion?

![Stable Diffusion Model Architecture](/screenshot/stable-diffusion.png)

Stable Diffusion Model Architecture

### What is LoRA?

![Merge LoRA weights into the base model](/screenshot/lora.png)

Merge LoRA weights into the base model

LoRA stands for Low-Rank Adaptation for Large Language Models. It is originally created to solve the issue of fine-tuning large language models with too many parameters. 

LoRA’s approach is to represent the weight updates with two smaller matrices (called update matrices) through low-rank decomposition. 

Under the LoRA strategy, we add a “side branch” on the right of the pretrained weights. Within this side branch, a linear layer A is used first to reduce the dimension from $d\times d$ to $d\times r$. The $r$ here is the rank of LoRA which is usually  $<< d$.  

Then in the second linear layer B, we map from $r$ back to $d$. To produce the final results, both the original and the adapted weights are combined to generate the hidden state. During the training or inferencing, the original weight matrix remains frozen and doesn’t receive any further adjustments. 

**With LoRA, we can efficiently train our own models and fine-tuning on a large general base model like Stable Diffusion v1-5.**

## Pipeline

### Machine Learning - LoRA Training

To train your LoRA, it is recommended to upload at least 10 to 15 pictures of yours.

### Frontend
![Image 1](/screenshot/frontend-1.png) ![Image 2](/screenshot/frontend-2.png)

We used React.JS and tailwind.css to create the frontend of our app.

```bash
npm run start
```

### Backend

Replace the line below to your trained LoRA:

```bash
# define lora path
lora_path = '../models/lora/'
# change the path here for your own trained LoRA
pipeline = load_lora(pipeline, lora_path + '<Your Own LoRA>.safetensors', 1, 'cuda', torch.float32)
```

Run backend app.

```bash
python app.py
```

## Results
<div style="display: flex; justify-content: center;">

![Image 1](/screenshot/result-1.png)

![Image 2](/screenshot/result-2.jpg)

</div>
<p float="middle">
  <img src="/screenshot/result-1.png" width="50%" />
  <img src="/screenshot/result-2.jpg" width="50%" /> 
</p>