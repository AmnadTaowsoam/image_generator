from flask import Flask, render_template, request, send_file, make_response
import openai
import configparser
import base64
from io import BytesIO

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['OpenAI']['api_key']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    image_generator = ImageGenerator()
    image_data = image_generator.generate_image(prompt)
    if image_data is not None:
        image = image_data
    else:
        image = None
    return render_template('generate.html', image=image, prompt=prompt)

@app.route('/download/<prompt>')
def download_image(prompt):
    image_generator = ImageGenerator()
    image_data = image_generator.generate_image(prompt)
    response = make_response(base64.b64decode(image_data))
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename='generated-image.png')
    return response

class ImageGenerator:
    def __init__(self):
        self.engine = "davinci"
        self.max_tokens = 256
        self.n = 1
        self.temperature = 0.5

    def generate_image(self, prompt):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=self.max_tokens,
            n=self.n,
            stop=None,
            temperature=self.temperature,
        )

        if len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, "image") and choice.image is not None:
                image_data = base64.b64encode(choice.image).decode('utf-8')
                return image_data
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


