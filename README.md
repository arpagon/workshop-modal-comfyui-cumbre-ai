# Workshop: Running FLUX with ComfyUI on Modal

This repository contains materials from a workshop presented at CumbreAI, demonstrating how to run the FLUX model using ComfyUI on Modal's cloud infrastructure.

## Prerequisites

- [Pixi](https://github.com/prefix-dev/pixi) for environment management
- [Modal](https://modal.com/) account and CLI

## Setup

1. Initialize the Pixi environment:
   ```
   pixi init . --pyproject
   ```

2. Install Modal:
   ```
   pixi add modal --pypi
   ```

## Running ComfyUI on Modal

Navigate to the ComfyUI directory and serve the application:
```
cd comfyui
modal serve comfyapp.py
```

## About the Project

This workshop demonstrates the integration of several cutting-edge AI technologies:

- [FLUX](https://huggingface.co/black-forest-labs/FLUX.1-dev): A powerful 12B parameter rectified flow transformer for text-to-image generation.
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI): An advanced, modular interface for creating complex Stable Diffusion workflows.
- [Modal](https://modal.com/): A serverless platform for running AI models and large-scale batch jobs.

## Workshop Context

This workshop was conducted as an independent side-event coinciding with [CumbreAI](https://www.mintic.gov.co/cumbre-ia/), a Latin American AI summit organized by the Colombian Ministry of Information Technologies and Communications (MinTIC). While taking place during the summit, it's important to note that this workshop was not officially affiliated with or organized by CumbreAI or MinTIC.

The timing and location were chosen to leverage the gathering of AI enthusiasts and professionals attending CumbreAI, but the content and organization of this workshop were entirely independent initiatives.

## Additional Resources

- [CumbreAI Official Website](https://www.mintic.gov.co/cumbre-ia/)
- [FLUX Model on Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-dev)
- [ComfyUI GitHub Repository](https://github.com/comfyanonymous/ComfyUI)
- [Modal Official Website](https://modal.com/)

## Acknowledgements

Special thanks to Tribu AI Colombia providing the platform to share this knowledge on running advanced AI image generation pipelines using cutting-edge tools and infrastructure.