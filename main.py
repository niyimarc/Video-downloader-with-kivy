from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kv_helpers import screen_helper
from pytube import YouTube
import socket
from kivymd.uix.dialog import MDDialog

Window.size = (450,700)

class DreyApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(screen_helper)
        return screen

    def clear_link_field(self, text_field):
        text_field.text = ""

    def getLinkInfo(self, event):
        # Check for internet connection
        if not self.check_internet_connection():
            # Show dialog if there is no internet connection
            if not self.dialog:
                self.dialog = MDDialog(
                    title="No internet connection",
                    type="simple",
                    text="Oops! Check your internet connection and try again!",
                    radius=[20, 7, 20, 7],
                )
            self.dialog.open()
            return

        self.link = self.root.ids.link_input.text  # Access MDTextField using ids
        self.yt = YouTube(self.link)
        self.source = self.yt.thumbnail_url
        self.vtitle = self.yt.title

        video_details = self.root.ids.video_details  # Access the BoxLayout of video details
        video_details.pos_hint = {'center_x': 0.5, 'center_y': 0.6}

        spinner = self.root.ids.spinner
        spinner.active = False  # Stop spinning

        async_image = self.root.ids.async_image  # Access AsyncImage using ids
        async_image.source = self.source

        video_title = self.root.ids.video_title
        video_title.text = self.vtitle

        self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
        drop_down = self.root.ids.drop_down
        drop_down.clear_widgets()  # Clear existing resolution buttons

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
        if resolution != 'Resolution':
            selected_video = self.video.filter(res=resolution).first()
            if selected_video:
                selected_video.download("YoutubeDownloader")
                print('Download Completed')
            else:
                print('Selected resolution is not available for download')
        else:
            print('Please select a resolution')

if __name__ == "__main__":
    DreyApp().run()
