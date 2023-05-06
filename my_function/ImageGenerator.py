import configparser
import openai

class ImageGenerator:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        api_key = config['OpenAI']['api_key']
        openai.api_key = api_key

    def generate_image(self, prompt):
        response = openai.Completion.create(
            engine="image-alpha-001",
            prompt=prompt,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if len(response.choices) > 0:
            return response.choices[0].text
        else:
            return None
