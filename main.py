from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.snackbar import Snackbar

from kv_helpers import screen_helper
from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import MaxRetriesExceeded
import socket
from kivymd.uix.dialog import MDDialog
from urllib.parse import urlparse, parse_qs
import re

Window.size = (450,700)

class DreyApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(screen_helper)
        return screen

    def getLinkInfo(self, event):
        # Check for internet connection
        if not self.check_internet_connection():
            # Show dialog if there is no internet connection
            self.show_no_internet_dialog()
            return

        self.link = self.root.ids.link_input.text  # Access MDTextField using ids
        self.yt = YouTube(self.link)
        self.source = self.yt.thumbnail_url
        self.vtitle = self.yt.title

        video_details = self.root.ids.video_details  # Access the BoxLayout of video details
        video_details.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Parse the link URL
        parsed = urlparse(self.link)
        # Extract the query parameters from the parsed URL
        query = parse_qs(parsed.query)
        # Access the video_playlist_detail BoxLayout using ids
        video_playlist_detail = self.root.ids.video_playlist_detail
        # Check if the 'list' parameter exists in the query parameters
        if 'list' in query:
            # If the 'list' parameter exists, it means the link is a playlist
            # Create a Playlist object using the link
            self.playlist = Playlist(self.link)
            # Set the position hint for the video_playlist_detail BoxLayout
            video_playlist_detail.pos_hint = {'center_y': 0.38}
        else:
            # If the 'list' parameter does not exist, it means the link is not a playlist
            # Set the position hint to hide the video_playlist_detail BoxLayout
            video_playlist_detail.pos_hint = {'center_y': 20}

        async_image = self.root.ids.async_image  # Access AsyncImage using ids
        async_image.source = self.source

        video_title = self.root.ids.video_title
        video_title.text = self.vtitle

        self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
        drop_down = self.root.ids.drop_down
        drop_down.clear_widgets()  # Clear existing resolution buttons

    def show_resolution_menu(self, instance):
        drop_down = self.root.ids.drop_down
        drop_down.clear_widgets()  # Clear existing resolution buttons

        for video in self.video:
            btn = MDRectangleFlatButton(
                text=video.resolution,
                size_hint=(None, None),
                on_release=lambda btn: self.select_resolution(btn.text),
            )
            drop_down.add_widget(btn)

        drop_down.open(instance)

    def select_resolution(self, resolution):
        self.root.ids.drop_down_btn.text = resolution

    def downloadVideo(self, event):
        resolution = self.root.ids.drop_down_btn.text  # Get the selected resolution

        if not self.check_internet_connection():
            # Show dialog if there is no internet connection
            self.show_no_internet_dialog()
            return

        if resolution != 'Resolution':
            selected_video = self.video.filter(res=resolution).first()
            if selected_video:
                selected_video.download("YoutubeDownloader")
                print('Downloading')
                Snackbar(
                    text="[color=#ddbb34]Downloading video![/color]",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=.7,
                ).open()

            else:
                Snackbar(
                    text="[color=#ddbb34]Selected resolution is not available for download![/color]",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=.7,
                ).open()
        else:
            Snackbar(
                text="[color=#ddbb34]please select a resolution before download![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7,
            ).open()

    def sanitize_filename(self, filename):
        """
        Remove characters that are not allowed in filenames on Windows.
        """
        restricted_chars = r'[<>:"/\\|?*]'
        sanitized_filename = re.sub(restricted_chars, "", filename)
        return sanitized_filename
    def downloadPlaylistVideo(self, event):
        try:
            Snackbar(
                text="[color=#ddbb34]Downloading playlist videos...[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7,
            ).open()
            sanitized_title = self.sanitize_filename(self.vtitle)
            for video in self.playlist.videos:
                highest_resolution = video.streams.get_highest_resolution()
                if highest_resolution:
                    highest_resolution.download("YoutubeDownloader/" + sanitized_title)
            Snackbar(
                text="[color=#ddbb34]Playlist fully downloaded[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7,
            ).open()
        except MaxRetriesExceeded:
            # Handle the MaxRetriesExceeded exception
            Snackbar(
                text="[color=#ddbb34]Failed to download playlist videos. Please check your internet connection and try again.[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7,
            ).open()

    def video_download_complete(self, stream, file_path):
        Snackbar(
            text="[color=#ddbb34]Download completed![/color]",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.7,
        ).open()

    def check_internet_connection(self):
        try:
            # Create a socket connection to a well-known host
            # Create a socket connection to Google's DNS server (8.8.8.8 on port 53).
            # If the connection is successful, it means there is an internet connection.
            # If an error occurs, it means there is no internet connection.
            socket.create_connection(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    def show_no_internet_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="No internet connection",
                type="simple",
                text="Oops! Check your internet connection and try again!",
                radius=[20, 7, 20, 7],
            )
        if not self.dialog._is_open:
            self.dialog.open()

    def on_stop(self):
        if self.dialog:
            self.dialog.dismiss()

if __name__ == "__main__":
    DreyApp().run()
