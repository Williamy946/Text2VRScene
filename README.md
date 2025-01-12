# Text2VRScene
Source Code Repository of IEEE VR 2024 Conference Paper "Text2VRScene: Exploring the Paradigm of Automated Generation System for VR Experience From the Ground Up"

# Introduction

This project utilizes LLMs to drive other kinds of text-based generation methods to construct an LLM-based VR Scene generator. In the source code, we utilize [Shap-E](https://github.com/openai/shap-e) to generate the 3D models from text, and utilize the API of [Skybox AI](https://skybox.blockadelabs.com/) to generate the Skybox Image. 

# Reproduction

## Step 1: Install Conda Development Environment and Create Virtual Env
Install the conda package manager from https://docs.conda.io/en/latest/miniconda.html.

```shell
cd src
conda create -n text2vr python=3.10
conda activate text2vr
pip install openai=0.28 tiktoken
```

## Step 2: Configuring 3D model generator in Virtual Env

### Shap-E
Following the instructions in [Shap-E](https://github.com/openai/shap-e) Github Page:

```shell
git clone https://github.com/openai/shap-e.git
cd shap-e
pip install -e .
```
### Download [Blender 3.5.1](https://drive.google.com/file/d/12q9-YoE9-ZcKWDLAP3UxsDrLt-rnA8Yl/view?usp=sharing)
### Download [Model Format Transforming Tool](https://drive.google.com/file/d/1PqHrqVOfdgkJhnBaTkDGN-9xlzGgPYYL/view?usp=sharing)

**Move the downloaded 2gltf2.py file into shap-e/space**

```shell
mv <path to 2gltf2>/2gltf2.py shap-e/space
```

**Move the generate_model.py file into shape-e/space**
```shell
mv <path to generate_model>/generate_model.py shap-e/space
```


## Step 3: Configuring OpenAI API

Following the [OpenAI Official API Webpage](https://platform.openai.com/api-keys)

## Step 4: Configuring Skybox API 

Following the [Blockad Lab Official API Webpage](https://skybox.blockadelabs.com/api-membership)

## Step 5: Set the parameters in main.py

```python
parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="generate the scene of the movie the Titanic",
        help="the prompt to render"
    )
    parser.add_argument(
        "--openai_key",
        type=str,
        nargs="?",
        default="<Fill your OpenAI API key>",
        help="openai api key"
    )
    parser.add_argument(
        "--skybox_key",
        type=str,
        nargs="?",
        default="<Fill your Skybox API key>",
        help="skybox api key"
    )
    parser.add_argument(
        "--shape_dir",
        type=str,
        nargs="?",
        default="<Path to shap-e>/shap-e",
        help="path of shap-e folder in remote machine"
    )
    parser.add_argument(
        "--python_dir",
        type=str,
        nargs="?",
        default="<Path to local anaconda>/envs/shap-e/bin/python",
        help="path of configured python environment"
    )
    parser.add_argument(
        "--blender_dir",
        type=str,
        nargs="?",
        default="<Path to downloaded blender>",
        help="path of blender in remote machine"
    )
```

# Expert Interview Scripts ([Link](https://drive.google.com/file/d/1bTMqTd4cUCoBRJpqxjV4Ha8Hx5Iw_o1C/view?usp=sharing))

# Citation

