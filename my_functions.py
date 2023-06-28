
from kivy.clock import mainthread
import os
from kivymd.uix.filemanager import MDFileManager

def open_file_manager(app):
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if app.file_manager is None:
        app.file_manager = MDFileManager(
            exit_manager=app.exit_file_manager,  # Set the exit_manager method
            select_path=app.select_path,  # Set the select_path method
        )
    app.file_manager.show(download_path)  # Show the file manager

def exit_file_manager(app, *args):
    app.file_manager.close()  # Close the file manager

def select_path(app, path):
    app.root.ids.download_location.text = path  # Update the text of the download_location label
    app.download_path = path
    app.exit_file_manager()  # Close the file manager
@mainthread
def update_async_image(root, source):
    async_image = root.ids.async_image
    async_image.source = source

@mainthread
def update_video_title(root, vtitle):
    video_title = root.ids.video_title
    video_title.text = vtitle

@mainthread
def update_video_details(root):
    video_details = root.ids.video_details
    video_details.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
