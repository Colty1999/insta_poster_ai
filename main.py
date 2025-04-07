import os
from datetime import datetime
import re
import requests
from dotenv import load_dotenv
import openai
from instagrapi import Client
from helpers import create_story_image
from instagram_login_challanger import challenge_code_handler
from instagrapi.types import StoryLink

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
        temperature=1.0,
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


def post_to_instagram(client: Client, image_path, caption):
    client.photo_upload(image_path, caption)
    print("Posted:", caption)


def post_story_with_newest_post(client: Client):
    feed = client.user_medias(client.user_id, 1)  # Get the most recent post
    if not feed:
        print("No posts found in your feed.")
        return
    newest_post = feed[0]
    media_url = newest_post.image_versions2['candidates'][0]['url']

    post_url = f"https://www.instagram.com/p/{newest_post.code}/"
    caption = "Sprawdźcie nowy post! 😍🎉"

    media_path = create_story_image(client.photo_download_by_url(media_url, "newest_post"))

    client.photo_upload_to_story(
        media_path,
        caption=caption,
        links=[StoryLink(webUri=post_url)],
    )

    print("Newest post shared as story with caption and emojis!")


if __name__ == "__main__":
    topic = generate_text('''
        Wygeneruj konkretny, specjalistycznie brzmiący temat posta na Instagramie (maks. 5 słów) dotyczący zdrowego odżywiania. Temat ma być unikalny, oparty na faktach, interesujący dla świadomego odbiorcy i brzmieć jak od eksperta. Unikaj ogólników typu ‘zdrowa dieta’ czy ‘zdrowe śniadanie’. Przykłady: ‘Wpływ omega-3 na mózg’, ‘Rola błonnika w mikrobiomie’, ‘Czy gluten szkodzi każdemu?’, ‘Mit detoksów sokowych obalony’.
    ''')
    post_promt = f"""
        Jesteś doświadczonym copywriterem tworzącym angażujące posty na Instagram dla marek z branży zdrowia i lifestyle.

        Napisz krótki post na temat: „{topic}”, który:

            od razu przyciąga uwagę nietypowym, ale naturalnym pierwszym zdaniem,

            wnosi konkretną, mniej oczywistą wartość lub ciekawostkę,

            unika utartych fraz i ogólników (np. „warto dbać o zdrowie”),

            jest profesjonalny, ale ludzki i przystępny,

            zawiera wyważoną listę (np. 2–4 punktów) z konkretnymi informacjami,

            korzysta z emoji tylko tam, gdzie naturalnie wspierają przekaz (nie dekoracyjnie),

            ma maksymalnie 600 znaków (bez hasztagów),

            nie zaczyna się od słów „Oto” ani „Poznaj”.

        Dodaj na końcu 2–3 trafne, ale niebanalne hasztagi (osobno).
    """
    caption = generate_text(post_promt)
    print("Generated caption:", topic, "/n", caption)
    image_prompt = f"A minimalist digital illustration of a {topic}. The background is a soft pale yellow color (#fefae0), with subtle gradients that give the effect of light falling from the left side. The illustration includes soft, natural shadows to add depth and dimension, with varying tones to give a sense of perspective. Smooth, textured surfaces create a sense of realism and richness. The design is clean and modern with a balanced color palette, incorporating light reflections and soft highlights to add volume and depth to the shapes."
    sanitized_topic = re.sub(r'[<>:"/\\|?*\r\n]', '', topic)
    image_path = f"images/{sanitized_topic}_{datetime.today().strftime('%Y-%m-%d')}.jpg"
    generate_image(image_prompt, image_path)

    client = Client()
    client.challenge_code_handler = challenge_code_handler
    client.login(insta_username, insta_password)
    # client.dump_settings("session.json")
    post_to_instagram(client, image_path, f"{caption} #InteligentnaDieta")
    post_story_with_newest_post(client)
    client.logout()
