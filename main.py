import os
import random
import requests
from dotenv import load_dotenv
import openai
from instagrapi import Client
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
insta_username = os.getenv("INSTAGRAM_USERNAME")
insta_password = os.getenv("INSTAGRAM_PASSWORD")

client = openai.OpenAI()


def generate_text(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.8,
    )
    return response.choices[0].message.content


def generate_image(prompt, output_path):
    response = client.images.generate(
        prompt=prompt,
        n=1,
        size="1024x1024",
        model="dall-e-3"
    )
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as handler:
        handler.write(img_data)
    return output_path


def post_to_instagram(image_path, caption):
    cl = Client()
    cl.login(insta_username, insta_password)
    cl.photo_upload(image_path, caption)


if __name__ == "__main__":
    topic = generate_text("Wygeneruj losowy temat z zakresu zdrowego odzywiania ktory mozna przedstawic w formie postu na instagarmie. Max 5 słów.")
    post_promts = [
        f"""
            Jesteś doświadczonym copywriterem tworzącym posty na Instagram dla marek lifestyle i zdrowia.

            Napisz krótki, angażujący post na temat: "{topic}", który przyciągnie uwagę od pierwszego zdania i zainteresuje szeroką grupę odbiorców. 

            Post powinien być:
            - profesjonalny, naturalny i ekspercki,
            - przyjazny i ludzki w tonie,
            - zawierać konkretną wartość (np. listę z myślnikami),
            - z wyważonym użyciem emoji,
            - maksymalnie 600 znaków (bez liczenia hasztagów).

            Dodaj też 2–3 trafne hasztagi na końcu (oddzielnie). Nie zaczynaj posta od „Oto” ani „Poznaj”. Zadbaj o lekkość języka i unikanie powtórzeń.
        """,
        f"""
            Jesteś doświadczonym copywriterem specjalizującym się w tworzeniu inspirujących treści na Instagram dla marek zajmujących się zdrowiem, wellness i stylem życia.

            Napisz krótki, interesujący post na temat: "{topic}", który zainteresuje szeroką grupę odbiorców. Post ma być:
            - profesjonalny, ale jednocześnie pełen pasji,
            - pełen wartościowych wskazówek,
            - użyj kilku emoji, aby podkreślić kluczowe informacje, ale nie przesadzaj,
            - maksymalnie 400 znaków,
            - zakończ post prostym, angażującym wezwaniem do działania (np. zapraszając do komentowania).

            Dodaj 3 trafne hasztagi.
        """,
        f"""
            Jako kreatywny copywriter, którego celem jest angażowanie i bawić odbiorców, napisz energiczny i lekki post na temat: "{topic}".
            Post ma być:
            - pełen entuzjazmu i pozytywnej energii,
            - zawierać przyjazny ton i delikatny humor,
            - być angażujący, zachęcający do interakcji,
            - wpleciony w wartościową treść z użyciem kilku dobrze dobranych emoji,
            - maksymalnie 400 znaków.
            Zakończ post pytaniem do odbiorców, które pobudzi rozmowę.
            Dodaj 3 odpowiednie hasztagi.
        """,
        f"""
            Jesteś specjalistą od tworzenia wartościowych treści edukacyjnych na Instagramie. Napisz post na temat: "{topic}", który:
            - ma na celu edukować odbiorców w przystępny sposób,
            - zawiera konkretne porady lub ciekawostki,
            - używa zwięzłego języka, ale jest rzetelny,
            - nie zapomnij o kilku emoji, które podkreślą kluczowe punkty,
            - zmieści się w 400 znakach.
            Podsumuj post krótką, inspirującą myśl, która zachęci do refleksji.
            Dodaj 3 odpowiednie hasztagi.
        """,
        f"""
            Tworzysz treści na Instagramie, które mają na celu budowanie relacji z odbiorcami. Napisz post na temat: "{topic}", który:
            - będzie ciepły i osobisty, jak rozmowa z przyjacielem,
            - wykorzysta ludzki ton i autentyczność,
            - zaprezentuje temat w sposób, który porusza emocje i angażuje,
            - zawiera wartościową informację z odpowiednią liczbą emoji,
            - nie przekroczy 400 znaków.
            Zakończ post pytaniem do odbiorców, które skłoni ich do dyskusji.
            Dodaj 3 trafne hasztagi.
        """,
        f"""
            Jesteś copywriterem, który tworzy eleganckie, estetyczne treści na Instagramie. Napisz post na temat: "{topic}", który:
            - zachwyci odbiorców zarówno treścią, jak i estetycznym stylem,
            - będzie elegancki, ale przystępny,
            - użyje subtelnych emoji w sposób, który wzbogaci przekaz,
            - zmieści się w 400 znakach,
            - zakończy inspirującym stwierdzeniem.
            Dodaj 3 eleganckie hasztagi.
        """
    ]
    caption = generate_text(random.choice(post_promts))
    image_prompt = f"A minimalist digital illustration of a {topic}. The background is a soft pale yellow color (#fefae0), flat and uniform. The dominant color of the fruit and bowl should be a muted sage green tone (#ccd5ae), used prominently throughout the composition. No text, no writing, just the image. Clean, modern design with a balanced color palette."
    image_path = f"images/{topic}_{datetime.today().strftime('%Y-%m-%d')}.jpg"

    generate_image(image_prompt, image_path)
    post_to_instagram(image_path, caption)
    print("Posted:", caption)
