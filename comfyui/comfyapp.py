# ---
# cmd: ["modal", "serve", "06_gpu_and_ml/comfyui/comfyapp.py"]
# deploy: true
# ---
#
# # Run ComfyUI interactively and as an API
#
# [ComfyUI](https://github.com/comfyanonymous/ComfyUI) is a no-code Stable Diffusion GUI that allows you to design and execute advanced image generation pipelines.
#
# ![example comfyui image](./comfyui.png)
#
# In this example, we show you how to
#
# 1. run ComfyUI interactively to develop workflows
#
# 2. serve a ComfyUI workflow as an API
#
# Combining the UI and the API in a single app makes it easy to iterate on your workflow even after deployment.
# Simply head to the interactive UI, make your changes, export the JSON, and redeploy the app.
#
# ## Quickstart
#
# This example serves the [ComfyUI inpainting example workflow](https://comfyanonymous.github.io/ComfyUI_examples/inpaint/),
# which "fills in" part of an input image based on a prompt.
# For the prompt `"Spider-Man visits Yosemite, rendered by Blender, trending on artstation"`
# on [this input image](https://raw.githubusercontent.com/comfyanonymous/ComfyUI_examples/master/inpaint/yosemite_inpaint_example.png),
# we got this output:
#
# ![example comfyui image](./comfyui_gen_image.jpg)
#
# 1. Stand up the ComfyUI server in development mode:
# ```bash
# modal serve 06_gpu_and_ml/comfyui/comfyapp.py
# ```
#
# 2. In another terminal, run inference:
# ```bash
# python 06_gpu_and_ml/comfyui/comfyclient.py --dev --modal-workspace your-modal-workspace --prompt "your prompt here"
# ```
# You can find your Modal workspace name by running `modal profile current`.
#
# The first inference will take a bit longer because the server will need to boot up (~20-30s).
# Successive inference calls while the server is up should take a few seconds or less.
#
# ## Setup
#
# First, we define the environment we need to run ComfyUI using [comfy-cli](https://github.com/Comfy-Org/comfy-cli). This handy tool manages the installation of ComfyUI, its dependencies, models, and custom nodes.


import json
import subprocess
import uuid
from pathlib import Path
from typing import Dict

import modal

image = (  # build up a Modal Image to run ComfyUI, step by step
    modal.Image.debian_slim(  # start from basic Linux with Python
        python_version="3.11"
    )
    .apt_install("git")  # install git to clone ComfyUI
    .pip_install("comfy-cli==1.0.35")  # install comfy-cli
    .run_commands(  # use comfy-cli to install the ComfyUI repo and its dependencies
        "comfy --skip-prompt install --nvidia",
    )
    .run_commands(  # download the inpainting model
        "comfy --skip-prompt model download --url https://huggingface.co/stabilityai/stable-diffusion-2-inpainting/resolve/main/512-inpainting-ema.safetensors --relative-path models/checkpoints/"
    )
    .run_commands(  # download the Flux model need login (https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors)
        "comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/hunyuan_dit_comfyui/resolve/main/hunyuan_dit_1.2.safetensors --relative-path models/checkpoints/"
    )
    .run_commands(  # download the Clip/T5 model
        "comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors --relative-path models/clip/"
    )
    .run_commands(  # download the VAE model
        "comfy --skip-prompt model download --url https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors --relative-path models/vae/"
    )
    .run_commands(  # download a custom node
        "comfy node install image-resize-comfyui"
    )
    # can layer additional models and custom node downloads as needed
)

app = modal.App(name="flux-comfyui", image=image)


# ## Running ComfyUI interactively and as an API on Modal
#
# To run ComfyUI interactively, simply wrap the `comfy launch` command in a Modal Function and serve it as a web server.
@app.function(
    allow_concurrent_inputs=10,
    concurrency_limit=1,
    container_idle_timeout=30,
    timeout=1800,
    gpu="A100",
)
@modal.web_server(8000, startup_timeout=60)
def ui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)
