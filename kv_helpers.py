screen_helper = """
MDScreen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Drey Youtube Video Downloader (DYVD) V0.0.2"
                        elevation: 4
                        pos_hint: {"top": 1}
                        specific_text_color: "#4a4939"

                    MDBottomNavigation:
                        #panel_color: "#eeeaea"
                        selected_color_background: "orange"
                        text_color_active: "lightgrey"
      
                        MDBottomNavigationItem:
                            name: 'screen 1'
                            text: 'Youtube Downloader'
                            icon: 'youtube'
    
                            BoxLayout:
                                orientation: "vertical"   
                                pos_hint: {'center_x': 0.5, 'center_y': 1} 
                                spacing: "20dp"
                                
                                BoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height
                            
                                    AsyncImage:
                                        source: 'https://github.com/niyimarc/Video-downloader-with-kivy/blob/master/icon.png?raw=true'
                                        size_hint: (.5, None)
                                        height: dp(100)
                                        pos_hint: {'center_x': 0.5}
                            
                                    Widget:
                                        size_hint_y: None
                                        height: "20dp"
      
                                BoxLayout:
                                    orientation: "horizontal" 
                                    size_hint: (.9,None)
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.95} 
                                    spacing: "10dp"
                                    
                                    MDTextField:
                                        id: link_input
                                        hint_text: "Paste Youtube Video Link"
                                        mode: "fill"
                                        helper_text: "Paste Youtube Video Link"
                                        pos_hint: {'center_y': 0.95}                                          
                                        multiline: False
                          
                                        
                                    MDRaisedButton:
                                        id: get_link
                                        text: "Get Link"
                                        pos_hint: {'center_x': 0.86, 'center_y': 0.95}
                                        on_release: 
                                            app.getLinkInfo(self)  # Call the function when the button is released
                                        disabled: not link_input.text or not link_input.text.startswith(("https://youtu.be/", "https://www.youtube.com/"))
                                
                            BoxLayout:
                                id: video_details
                                orientation: "horizontal"
                                size_hint: (.9,None)
                                pos_hint: {'center_x': 0.5, 'center_y': 20}
                                spacing: "10dp"
                                    
                                AsyncImage:
                                    id: async_image
                                    size_hint: (.2,None)
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                    source:''
                                    
                                BoxLayout:
                                    orientation: "vertical"
                                    size_hint: (.7, None)
                                    pos_hint: {'center_y': 0.5}
                                    spacing: "10dp"  # Set the desired spacing  
                                    
                                    MDLabel:
                                        id: video_title
                                        text: ''
                                        size: self.texture_size      
                                      
                                    BoxLayout:        
                                        orientation: "horizontal"   
                                        size_hint: (None, .7)
                                        spacing: "10dp"  # Set the desired spacing  
                                        
                                        MDRectangleFlatButton:
                                            text: "Download Location"
                                            size_hint: (None,0.9)
                                            on_release: app.open_file_manager() 
                                        
                                        MDLabel:
                                            id: download_location
                                            size_hint: (None,0.4) 
                                            text: "Choose Download Location"
                                            halign: "center"
                                        
                                        MDRaisedButton:
                                            text: "Download Video"
                                            pos_hint: {'center_y': 0.35}   
                                            on_release: app.downloadVideo(self)  # Call the function when the button is released   
                                            disabled: download_location.text == "Choose Download Location"
                                            
                                        MDRaisedButton:
                                            id: download_video_playlist
                                            text: "Download Playlist Instead"
                                            pos_hint: {'center_y': 0.35}
                                            on_release: app.downloadPlaylistVideo(self)  # Call the function when the button is released 
                                            disabled: download_location.text == "Choose Download Location"   
                                            halign: "center"  
                                           
                            BoxLayout:
                                orientation: "horizontal"
                                pos_hint: {'center_x': 0.5, 'center_y': 20} 
                                id: progress_bar_detail
                                size_hint: (.9,None)
                                height: "18dp"   
                            
                                MDLabel:
                                    id: progress_label
                                    text: "Download Status"
                                    halign: "center"
                                        
                                    
                        MDBottomNavigationItem:
                            name: 'screen 3'
                            text: 'Information'
                            icon: 'information'
                            
                            BoxLayout:
                                orientation: "vertical"   
                                pos_hint: {'center_x': 0.5, 'center_y': 0.6} 
                                size_hint_x: 0.8
                                size_hint_y: 0.7
                                height: self.minimum_height
                                spacing: "10dp"

                                MDLabel:
                                    text: 'How To Use DYVD?'
                                    font_style: 'H3'
                                    halign: 'center'
                                    
                                MDLabel:
                                    text: 'Step 1: Copy the link to the youtube video you will like to download, paste it in the text field and click on Get Link button to get the video'
                                    halign: 'center'
                                    
                                MDLabel:
                                    text: 'Step 2: Once the video details are fully loaded, you must choose your download path(download path is where you want your video to be downloaded to.'
                                    halign: 'center'
                                    
                                MDLabel:
                                    text: 'Step 3: Download your video and wait till the download is completed.'
                                    halign: 'center'
                                    
                                MDLabel:
                                    text: 'Step 4: Open the path you selected in your file explorer to view your downloaded video'
                                    halign: 'center'
                                    
                                MDLabel:
                                    text: 'Do You Want To Report a Bug?'
                                    font_style: 'H3'
                                    halign: 'center'

                                MDLabel:
                                    text: 'If you have any issue while using this app to download from youtube, kindly send me a message with the issue you encounter to info@dreytech.us'
                                    halign: 'center'

"""