import os
from dotenv import load_dotenv
from helpers.story_image_generator import create_story_image
from helpers.instagram_login_challanger import challenge_code_handler
from instagrapi.types import StoryLink, Media
from instagrapi import Client


class InstagramClient:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")

        self.client = Client()
        self.client.challenge_code_handler = challenge_code_handler
        self.client.login(self.username, self.password)
        print(f"Logged in as {self.username}")

    def dump_settings(self, filename: str):
        self.client.dump_settings(filename)

    def load_settings(self, filename: str):
        self.client.load_settings(filename)

    def post_to_feed(self, image_path: str, caption: str):
        self.client.photo_upload(image_path, caption)

    def post_story_with_newest_post(self):
        feed = self.client.user_medias(self.client.user_id, 1)
        if not feed:
            print("No posts found in your feed.")
            return

        newest_post = feed[0]
        media_url = newest_post.image_versions2['candidates'][0]['url']
        post_url = f"https://www.instagram.com/p/{newest_post.code}/"

        media_path = create_story_image(self.client.photo_download_by_url(media_url, "newest_post"))
        self.client.photo_upload_to_story(
            media_path,
            links=[StoryLink(webUri=post_url)],
        )

    def get_user_id_by_username(self, username: str):
        user_id = self.client.user_id_from_username(username)
        if not user_id:
            print("User not found.")
            return
        return user_id

    def get_user_posts(self, user_id: str):
        medias = self.client.user_medias(user_id, 10)
        if not medias:
            print("No posts found for user.")
            return None
        return medias

    def comment_under_random_post(self, media: Media, comment: str):
        post_id = media.pk
        self.client.media_comment(post_id, comment)

    def search_users_by_keyword(self, keyword: str):
        users = self.client.search_users(keyword)
        if not users:
            print("No users found.")
            return
        return users

    def __del__(self):
        self.client.logout()
        print(f"Logged out from {self.username}")
