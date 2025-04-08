from datetime import datetime
import re
from helpers.openai_client import OpenAIClient
from helpers.instagram_client import InstagramClient


if __name__ == "__main__":
    openai_client = OpenAIClient()
    topic_prompt = '''
        Wygeneruj konkretny, specjalistycznie brzmiący temat posta na Instagramie (maks. 5 słów) dotyczący zdrowego odżywiania. Temat ma być unikalny, oparty na faktach, interesujący dla świadomego odbiorcy i brzmieć jak od eksperta. Unikaj ogólników typu ‘zdrowa dieta’ czy ‘zdrowe śniadanie’. Przykłady: ‘Wpływ omega-3 na mózg’, ‘Rola błonnika w mikrobiomie’, ‘Czy gluten szkodzi każdemu?’, ‘Mit detoksów sokowych obalony’.
    '''
    topic = openai_client.generate_text(topic_prompt, temperature=1.0)
    print("Generated topic:", topic)
    caption_promt = f"""
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
    caption = openai_client.generate_text(caption_promt)
    print("Generated caption:", caption)
    image_prompt = f'''
    A minimalist digital illustration of a {topic}. The background is a soft pale yellow color (#fefae0), with subtle gradients that give the effect of light falling from the left side. The illustration includes soft, natural shadows to add depth and dimension, with varying tones to give a sense of perspective. Smooth, textured surfaces create a sense of realism and richness. The design is clean and modern with a balanced color palette, incorporating light reflections and soft highlights to add volume and depth to the shapes.
    '''
    sanitized_topic = re.sub(r'[<>:"/\\|?*\r\n]', '', topic)
    image_path = f"images/{sanitized_topic}_{datetime.today().strftime('%Y-%m-%d')}.jpg"
    openai_client.generate_image(image_prompt, image_path)

    # client.dump_settings("session.json")
    instagram_client = InstagramClient()
    instagram_client.post_to_feed(image_path, f"{caption} #InteligentnaDieta")
    instagram_client.post_story_with_newest_post()
