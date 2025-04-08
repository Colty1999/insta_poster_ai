import random
from helpers.openai_client import OpenAIClient
from helpers.instagram_client import InstagramClient


if __name__ == "__main__":
    instagram_client = InstagramClient()
    users = instagram_client.search_users_by_keyword(random.choice(["dietetyk", "zdrowie", "odchudzanie", "fitprzepisy"]))
    random_user = random.choice(users)
    while True:
        if random_user.is_private:
            print("User is private, selecting another one.")
            users.remove(random_user)
            random_user = random.choice(users)
        else:
            break
    user_id = instagram_client.get_user_id_by_username(random_user.username)
    user_posts = instagram_client.get_user_posts(user_id)
    while True:
        if not user_posts:
            print("No posts found, selecting another user.")
            users.remove(random_user)
            random_user = random.choice(users)
            user_id = instagram_client.get_user_id_by_username(random_user.username)
            user_posts = instagram_client.get_user_posts(user_id)
        else:
            break
    random_post = random.choice(user_posts)
    openai_client = OpenAIClient()
    comment_prompt = f"""
        Jesteś doświadczonym copywriterem tworzącym angażujące komentarze na Instagram dla marek z branży zdrowia i lifestyle.

        Napisz krótki komentarz do posta: „{random_post.caption_text}”, który:

            pochwali twórcę postu za jego pracę,

            odniesie do treści posta w sposób merytoryczny i przemyślany,

            poleci swój profil jako źródło wartościowych treści związanych z tematem posta,

            ma maksymalnie 100 znaków.
    """
    comment = openai_client.generate_text(comment_prompt, temperature=0.9)
    instagram_client.comment_under_random_post(random_post, comment)
    print("Selected user:", random_user)
    print("Selected post:", f"https://www.instagram.com/p/{random_post.code}/")
    print("Generated comment:", comment)
