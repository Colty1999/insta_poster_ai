import os
import requests
from dotenv import load_dotenv
import openai


class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.client = openai.OpenAI()

    def generate_text(self, prompt, model="gpt-4o-mini", temperature=0.8, max_tokens=400):
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def generate_image(self, prompt, output_path, size="1024x1024", model="dall-e-3"):
        response = self.client.images.generate(
            prompt=prompt,
            n=1,
            size=size,
            model=model
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
        print("Image saved to:", output_path)
        return output_path
