from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kv_helpers import screen_helper
from pytube import YouTube
from pytube.exceptions import MaxRetriesExceeded
import socket
from kivymd.uix.dialog import MDDialog
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import Clock, mainthread
from pytube import Playlist
from urllib.parse import urlparse, parse_qs
from my_functions import update_async_image, update_video_title, update_video_details, open_file_manager, exit_file_manager, select_path
import os
Window.size = (1000,700)

class DreyApp(MDApp):
    dialog = None
    file_manager = None
    file_size = 0  # Define the 'file_size' attribute

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(screen_helper)

        return screen


    def get_android_screen_size(self):
        from jnius import autoclass

        # Get the current activity and display metrics
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        metrics = autoclass('android.util.DisplayMetrics')()

        # Get the default display
        display = activity.getWindowManager().getDefaultDisplay()
        display.getMetrics(metrics)

        # Return the screen width and height
        return (metrics.widthPixels, metrics.heightPixels)

    def open_file_manager(self):
        open_file_manager(self)

    def exit_file_manager(self, *args):
        exit_file_manager(self, *args)

    def select_path(self, path):
        select_path(self, path)

    def getLinkInfo(self, event):
        # Check for internet connection
        if not self.check_internet_connection():
            # Show dialog if there is no internet connection
            self.show_no_internet_dialog()
            return

        self.current_size = 0  # Initialize current_size to 0

        self.link = self.root.ids.link_input.text  # Access MDTextField using ids
        self.yt = YouTube(self.link)
        self.source = self.yt.thumbnail_url
        self.vtitle = self.yt.title

        # Parse the link URL
        parsed = urlparse(self.link)
        # Extract the query parameters from the parsed URL
        query = parse_qs(parsed.query)
        # Access the download_video_playlist BoxLayout using ids
        download_video_playlist_btn = self.root.ids.download_video_playlist
        # Check if the 'list' parameter exists in the query parameters
        if 'list' in query:
            # If the 'list' parameter exists, it means the link is a playlist
            # Create a Playlist object using the link
            self.playlist = Playlist(self.link)
            # Set the position hint for the download_video_playlist BoxLayout
            download_video_playlist_btn.pos_hint = {'center_y': 0.35}
        else:
            # If the 'list' parameter does not exist, it means the link is not a playlist
            # Set the position hint to hide the download_video_playlist BoxLayout
            download_video_playlist_btn.pos_hint = {'center_y': 20}


        update_async_image(self.root, self.source)
        update_video_title(self.root, self.vtitle)
        update_video_details(self.root)



        progress_bar_detail = self.root.ids.progress_bar_detail
        progress_bar_detail.pos_hint = {'center_x': 0.5, 'center_y': 0.26}
        self.progress_label = self.root.ids.progress_label

        self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()


    def downloadVideo(self, event):
        if not self.check_internet_connection():
            # Show dialog if there is no internet connection
            self.show_no_internet_dialog()
            return

        # Find the stream with the highest resolution
        highest_resolution = self.yt.streams.get_highest_resolution()
        if highest_resolution:
            # Start the download in a separate thread to avoid app slowing down or freezing
            download_thread = threading.Thread(target=self.start_downloadvideo, args=(highest_resolution,))
            download_thread.start()
        else:
            # If there is no stream with the highest resolution, show an error message
            Snackbar(
                text="No video available in the highest resolution",
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
            # Create a thread for each video in the playlist and start downloading
            download_threads = [] # Create an empty list to store the download threads
            download_status = {}  # Dictionary to track the download status for each video

            with ThreadPoolExecutor() as executor:
                for video in self.playlist.videos:
                    download_status[video.video_id] = False  # Initialize the download status for each video
                    thread = threading.Thread(target=self.start_downloadplaylistvideo, args=(video, self.file_size, download_status))
                    download_threads.append(thread)
                    thread.start()

            # Wait for all the threads to complete
            for thread in download_threads:
                thread.join()

            # Check if all videos have been downloaded
            if all(status for status in download_status.values()):
                # If all videos are downloaded, update the progress label
                self.update_progress_label("Download completed!")
            else:
                # If any video is still downloading, update the progress label
                self.update_progress_label("Download in progress...")

        except MaxRetriesExceeded:
            # Handle the MaxRetriesExceeded exception
            Snackbar(
                text="[color=#ddbb34]Failed to download playlist videos. Please check your internet connection and try again.[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7,
            ).open()


    def start_downloadvideo(self, video):
        try:
            self.total_size = video.filesize
            self.current_size = 0
            self.download_completed = False
            Clock.schedule_once(lambda dt: self.update_download_progress(self.total_size, self.current_size), 0)
            video.download(self.download_path + "/")
            self.download_completed = True  # Set the download_completed flag to True
        except Exception as e:
            # Handle any exceptions that occur during the download process
            print(f"Download error: {e}")


    @mainthread
    def show_downloading_snackbar(self, text):
        Snackbar(
            text=text,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.7,
        ).open()

    @mainthread
    def update_progress_label(self, text):
        self.progress_label.text = text
    def start_downloadplaylistvideo(self, video, file_size, download_status):
        try:
            sanitized_title = self.sanitize_filename(self.vtitle)
            def download_playlist():
                file_path = f"{self.download_path}/{sanitized_title}/{video.title}.mp4"
                if os.path.exists(file_path):
                    # Skip the video if it already exists
                    self.update_progress_label(f"Skipping video: {video.title}")
                    return
                # Download the playlist in the background
                highest_resolution = video.streams.get_highest_resolution()
                highest_resolution.download(output_path=self.download_path + "/" + sanitized_title)

            # Create and start a new thread for the download
            download_thread = threading.Thread(target=download_playlist)
            download_thread.start()


        except Exception as e:
            # Handle any exceptions that occur during the download process
            print(f"Download error: {e}")

    def update_download_progress(self, total_size, current_size):
        if self.download_completed:
            progress = "Download completed!"
        elif total_size == 0:
            self.progress_label.text = "Download completed!"
        elif current_size > 0 and total_size > 0:
            progress = f"Download in progress..."
        else:
            progress = "Download in progress..."
        self.progress_label.text = progress

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
