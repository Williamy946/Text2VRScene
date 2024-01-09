'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

from ChatGPT_coder import ChatGPT_coder
from experience_generator import experience_generator
import argparse

def Text2VR(opt, hist_messages, is_test):

    # Input text as ChatGPT prompt, return the filtered aframe html code

    hist_messages, code, literature = ChatGPT_coder(hist_messages, opt, is_test)

    if code != None:
        # generate VR experience
        experience_generator(code, literature, is_test)

    return hist_messages, code

if __name__ == "__main__":

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
        default="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",
        help="openai api key"
    )
    parser.add_argument(
        "--skybox_key",
        type=str,
        nargs="?",
        default="1QIF7ouzzbkRGcnXe1XAtABVy6b5c28brOLsOgY3UgUJV4hmYJy0rSkJn9ZR",
        help="skybox api key"
    )
    parser.add_argument(
        "--shape_dir",
        type=str,
        nargs="?",
        default="/home/zyin/shap-e",
        help="path of shap-e folder in remote machine"
    )
    parser.add_argument(
        "--python_dir",
        type=str,
        nargs="?",
        default="/home/zyin/anaconda3/envs/shap-e/bin/python",
        help="path of configured python environment in remote machine"
    )
    parser.add_argument(
        "--blender_dir",
        type=str,
        nargs="?",
        default="~/blender/blender",
        help="path of blender in remote machine"
    )
    opt = parser.parse_args()

    hist_messages = []
    is_test = False
    Text2VR(opt, hist_messages, is_test)



