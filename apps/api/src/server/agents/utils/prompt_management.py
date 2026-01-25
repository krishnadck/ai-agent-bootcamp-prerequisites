import yaml
from jinja2 import Template
from langsmith import Client

ls_client = Client()

def get_prompt_from_config(yaml_file_path, prompt_key):
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return Template(config['prompts'][prompt_key])

def read_from_langsmith_registry(prompt_key):
    prompt_obj = ls_client.pull_prompt(prompt_key)
    return Template(prompt_obj.messages[0].prompt.template)


