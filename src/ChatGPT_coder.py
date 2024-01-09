'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

import os
import json
import time
import openai
from json_parser import *
from overload import *
import token_counter
from assets_generator import  shape_models_generator
from skybox_generator import skybox_generator

def attempt_to_fix_json_by_finding_outermost_brackets(json_string):

    try:
        # Use regex to search for JSON objects
        import regex
        json_pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")
        json_match = json_pattern.search(json_string)

        if json_match:
            # Extract the valid JSON object from the string
            json_string = json_match.group(0)
        else:
            raise ValueError("No valid JSON object found")

    except (json.JSONDecodeError, ValueError) as e:
        json_string = {}

    return json_string

def parse_response_json(gpt_response):
    try:
        # Parse and print Assistant json_response
        json_response = fix_and_parse_json(gpt_response)

    except json.JSONDecodeError as e:
        json_response = attempt_to_fix_json_by_finding_outermost_brackets(gpt_response)
        json_response = fix_and_parse_json(json_response)

    # Check if json_response is a string and attempt to parse it into a JSON object
    if isinstance(json_response, str):
        try:
            json_response = json.loads(json_response)
        except json.JSONDecodeError as e:
            json_response = attempt_to_fix_json_by_finding_outermost_brackets(json_response)

    return json_response

def Response_parser(Response):
    '''
    Take '<' and '>' as divider to capture the html source code.
    Might wrongly capture some explanations about the codes.
    :param Response: response content
    :return: html source code
    '''
    print("Parsing Response")
    try:
        json_res = parse_response_json(Response)

        parsed_json = json_res  # just check the validity
        return parsed_json
    except:
        return None

def construct_prompt(literature, hist_code, description, skybox, models, scale, position, hist_messages, prompt, cur_step, parse_error):
    task_start = "The user prompt is: "
    task_end = ". You should determine the literature or name of songs that user mentioned, and generate the description follows the constraints. "
    res_cons = " You should only output the JSON formatted response as described in Constraints and do not add extra explanations excluding the JSON response"
    res_chk = " You should check the correctness of the JSON response again, it can not be parsed by json.loads()."
    count_chk = " And You should check token count of your response, make sure your response do not exceed the limitation."
    if cur_step == 0:
        prompt_task = open("prompts/prompt_task.txt",'r').read()
        cur_prompt = [{"role":"system", "content":f"You are a helpful assistant."},
                      {"role":"system", "content":f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task": "Generate the main topic of User Prompt, and generate the description follows the constraints."+res_cons,
                                                  "User Prompt":prompt,
                                                  "Constraints":prompt_task,
                                                  })}]
    elif cur_step == 1:
        prompt_skybox = open("prompts/prompt_skybox.txt",'r').read()
        cur_prompt = [{"role":"system", "content":f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task":"Respond the short description of the skybox based on the Scene Description based on the content in Literature, following the Constraints."+res_cons,
                                                  "Scene Description":description,
                                                  "Literature":literature,
                                                  "Constraints":prompt_skybox
                                                  })}]

    elif cur_step == 2:
        prompt_3d_models = open("prompts/prompt_3d_models.txt", 'r').read()
        cur_prompt = [{"role": "system", "content": f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task":"Based on THE DESCRIBED SCENE and the description of the skybox, YOU SHOULD DETERMINE THE MENTIONED AND POSSIBLE IMPORTANT CHARACTERS AND OBJECTS in the scene STRICTLY Following the Constraints based on the literature",
                                                  "Scene Description":description,
                                                  "Skybox Description":skybox,
                                                  "Constraints":prompt_3d_models,
                                                  "Literature":literature
                                                })}]
    elif cur_step == 3:
        prompt_scale = open("prompts/prompt_scale.txt", 'r').read()
        cur_prompt = [{"role": "system", "content": f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task":"Based on the given scene description, you should generate the SIZE of all characters and objects in the given Model List STRICTLY following the Constraint."+
                                                 ". Explain the reasons."+res_cons,
                                                  "Scene Description":description,
                                                  "Model List":models,
                                                  "Constraints":prompt_scale,
                                                  })}]
    elif cur_step == 4:
        prompt_position = open("prompts/prompt_position.txt", 'r').read()
        cur_prompt = [{"role": "system", "content": f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task":"Considering the scale of all characters and objects in the given Scales and considering the given Scene Descriptions, generate the position of all characters and objects listed in given Models STRICTLY following the Constraints below"+
                                                " and explain the reasons."+res_cons,
                                                  "Scales":scale,
                                                  "Models":models,
                                                  "Scene Descriptions":description,
                                                  "Constraints":prompt_position
                                                  })}]

    elif cur_step == 5:
        prompt_codes = open("prompts/prompt_codes.txt", 'r').read()
        cur_prompt = [{"role": "system", "content": f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content": json.dumps({
                                                "Task": "Based on the given Constraints, generating the source code USING the 3D objects in given Models, skybox image file in given Skybox."
                                                 " Do not use any extra model not listed in the Models. Set the scale and position of the above models with the given scale and start position "
                                                 " Then output the AFrame code based on the given AFrame template in the given constraints."
                                                 " Do not modify the given part of AFrame code. ",
                                                   "Models":models,
                                                   "Skybox":skybox,
                                                   "Scene Description": description,
                                                   "Scale": scale,
                                                   "Start Position": position,
                                                   "Constraints": prompt_codes})}]

    elif cur_step == 6:
        prompt_animations = open("prompts/prompt_animations.txt", 'r').read()
        cur_prompt = [{"role": "system", "content": f"You are a helpful assistant."},
                      {"role": "system", "content": f"The historical Conversation is:\n{hist_messages}\n\n"},
                      {"role": "user", "content":json.dumps({
                                                "Task":"Based on the Constraints and the Start Position, add the animation attribute of 3D models in the Generated Code to realise the described movements in the Scene Description"+
                                                 "\n to express the logic in the description."+res_cons,
                                                    "Literature": literature,
                                                    "Scene Description": description,
                                                    "Start Position": position,
                                                    "Generated Code": hist_code,
                                                    "Constraints": prompt_animations
                                                })}]
    else:
        cur_prompt = []
    if len(cur_prompt) > 1 and cur_step < 5 and parse_error == 1:
        cur_prompt.append({"role": "system", "content": res_chk})
    elif len(cur_prompt) > 1 and cur_step >= 5 and parse_error == 1:
        cur_prompt.append({"role": "system", "content": res_chk+count_chk})
    current_tokens_used = token_counter.count_message_tokens(cur_prompt)
    return cur_prompt, current_tokens_used

@overload
def ChatGPT_coder(hist_messages, opt, is_test):

    '''
    Submit prompt and obtain response
    Add retry mechanism for increasing the robustness of generating executable codes.
    :param hist_messages: existing prompts for conversation
    :param prompt: recorded prompt
    :return: new hist_prompt, html codes
    '''

    openai.api_key = opt.openai_key
    prompt = opt.prompt
    total_steps = 7
    cur_step = 0
    max_retry = 5
    literature = ""
    name_liter = ""
    description = ""
    sky_cam_prop = ".."
    models = ""
    html_code = ""
    skybox = ""
    scale = ""
    position = ""
    while cur_step < total_steps:
        retry_num = 0
        parse_error = 0
        while retry_num < max_retry:
            print("Step {}:".format(cur_step))
            cur_prompt, current_tokens_used = construct_prompt(name_liter, html_code, description, skybox, models, scale, position, hist_messages, prompt, cur_step, parse_error)
            while current_tokens_used > 3000:
                hist_messages = hist_messages[1:]
                cur_prompt, current_tokens_used = construct_prompt(name_liter, html_code, description, skybox, models, scale, position, hist_messages, prompt, cur_step, parse_error)
            print("Submit prompt")
            try:
                response = openai.ChatCompletion.create(
                  model="gpt-4",
                  messages = cur_prompt,
                  temperature = 0,
                  timeout=10,
                )
            except Exception as ex:
                print(ex)
                retry_num += 1
                continue
            res_content = response['choices'][0]['message']['content']
            print(res_content)
            parsed_json = Response_parser(res_content)
            if parsed_json == None:
                retry_num += 1
                parse_error = 1
                continue

            if cur_step == 0: # generate task description

                literature = parsed_json["responses"]["topic"]
                name_liter = parsed_json["responses"]["topic"]
                literature = literature.replace(" ","").lower()
                description = parsed_json["responses"]["description"]

            elif cur_step == 1:
                key = parsed_json["responses"].keys()
                skybox_desc = parsed_json["responses"]["skyboxprompt"]
                skybox = skybox_desc
                if False:
                    if not os.path.exists("./tmp_file/" + str(literature)+ "/resource/images/"):
                        os.makedirs("./tmp_file/" + str(literature) + "/resource/images/")
                    print("generating skybox")
                    if not skybox_generator(apikey = opt.skybox_key, prompt=skybox_desc, literature=literature):
                        retry_num += 1
                        continue
            elif cur_step == 2:
                if "models" in parsed_json["responses"]:
                    models = str(parsed_json["responses"]["models"])
                    models3d = list(parsed_json["responses"]["models"].keys())
                    if len(models3d) != 0:
                        for path in models3d:
                            print(path)
                            if not is_test:
                                shape_models_generator(opt, path, parsed_json["responses"]["models"][path])
                                local_path = "./tmp_file/" + str(path)
                                indiv_path = "./tmp_file/" + str(literature) + "/" + str(path)
                                if not os.path.exists('/'.join(indiv_path.split('/')[:-1])):
                                    os.makedirs('/'.join(indiv_path.split('/')[:-1]))
                                os.system("cp " + local_path + " " + indiv_path)

            elif cur_step == 3:
                scale = str(parsed_json["responses"]["scale"])
            elif cur_step == 4:
                position = str(parsed_json["responses"]["position"])
            elif cur_step == 5:
                html_code = response['choices'][0]['message']['content']
            elif cur_step == 6:
                print(parsed_json.keys())
                if "responses" in parsed_json:
                    print(parsed_json["responses"].keys())
                    if "html code" in parsed_json["responses"]:
                        html_code = parsed_json["responses"]["html code"]
                    else:
                        print("Key not found")
                        retry_num += 1
                        continue
                else:
                    print("Key not found")
                    retry_num += 1
                    continue
            else:
                retry_num += 1
                continue

            if not os.path.exists('./tmp_file/resource/response/'+str(literature)):
                os.makedirs('./tmp_file/resource/response/'+str(literature))
            with open('./tmp_file/resource/response/'+str(literature)+'/'+str(cur_step)+'.json', 'w') as f:
                f.write(res_content)

            if not os.path.exists('./tmp_file/'+literature+'/resource/response/'):
                os.makedirs('./tmp_file/'+literature+'/resource/response/')
            with open('./tmp_file/'+literature+'/resource/response/'+str(cur_step)+'.json', 'w') as f:
                f.write(res_content)

            if cur_step == 0:
                f = open('./tmp_file/' + literature + '/discussion.txt', 'w')
            else:
                f = open('./tmp_file/'+literature+'/discussion.txt', 'a')
            ques = json.dumps(cur_prompt, indent=4)
            f.write("\n\n**** PROMPT "+str(cur_step)+" *****\n\n")
            f.write(ques)
            f.write("\n\n**** Response " + str(cur_step) + " *****\n\n")
            f.write(res_content)
            f.close()

            hist_messages.append({"user": cur_prompt[-1]['content']})
            hist_messages.append({"assistant": res_content})
            cur_step += 1
            break
        if retry_num >= max_retry:
            if cur_step == 0:
                f = open('./tmp_file/' + literature + '/discussion.txt', 'w')
            else:
                f = open('./tmp_file/'+literature+'/discussion.txt', 'a')
            ques = json.dumps(cur_prompt, indent=4)
            f.write("\n\n**** PROMPT "+str(cur_step)+" *****\n\n")
            f.write(ques)
            f.write("\n\n**** Response " + str(cur_step) + " *****\n\n")
            f.write(res_content)
            f.close()
            print("Generation Error, Please Retry.")
            break

    return hist_messages, html_code, literature

