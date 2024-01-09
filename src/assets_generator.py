'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

import os

def shape_models_generator(opt, filepath, description):

    print("Generating " + str(filepath))
    # 3D model generation
    local_path = "./tmp_file/"+str(filepath)
    object_name = filepath.split("/")[-1].split('.')[0]

    cmd = "cd "+opt.shape_dir+"/space;"+opt.python_dir+" generate_model.py --prompt \""+str(description)+\
          "\""
    os.system(cmd)

    cmd2 = "cd "+opt.shape_dir+"/space; "+opt.blender_dir+" -b -P 2gltf2.py -- mesh.ply"
           #"/home/zyin/.nvm/versions/node/v16.20.0/bin/node /home/zyin/.nvm/versions/node/v16.20.0/bin/obj2gltf -i mesh_0.obj -o " + str(object_name) + ".gltf"
    os.system(cmd2)

    model_path = opt.shape_dir+"/space/mesh.gltf"
    cmd3 = "cp "+model_path+" "+local_path
    os.system(cmd3)

if __name__ == "__main__":
    import argparse
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

    prompt = "a woman with long curly hair wearing a light blue dress"
    filepath = "resource/models/Rose.gltf"
    shape_models_generator(opt, filepath, prompt)