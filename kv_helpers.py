screen_helper = """
MDScreen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Drey Tech Downloader"
                        elevation: 4
                        pos_hint: {"top": 1}
                        specific_text_color: "#4a4939"
                        

                    MDBottomNavigation:
                        #panel_color: "#eeeaea"
                        selected_color_background: "orange"
                        text_color_active: "lightgrey"
                        
                        
                        MDBottomNavigationItem:
                            name: 'screen 3'
                            text: 'Home'
                            icon: 'home'
                
                            MDLabel:
                                text: 'Home'
                                halign: 'center'
                                
                        MDBottomNavigationItem:
                            name: 'screen 1'
                            text: 'Youtube'
                            icon: 'youtube'
                
                            
                            BoxLayout:
                                orientation: "vertical"   
                                pos_hint: {'center_x': 0.5, 'center_y': 1} 
                                spacing: "20dp"
                                
                                Image:
                                    source: 'youtube.png'
                                    size_hint: (.5,None)
                                    pos_hint: {'center_x': 0.5} 
                                    
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
                                        on_release: app.getLinkInfo(self)  # Call the function when the button is released
                                        disabled: not link_input.text or not link_input.text.startswith(("https://youtu.be/", "https://www.youtube.com/"))
                                
                            BoxLayout:
                                id: video_details
                                orientation: "horizontal"
                                size_hint: (.9,None)
                                pos_hint: {'center_x': 0.5, 'center_y': 20}
                                spacing: "10dp"
                                    
                                AsyncImage:
                                    id: async_image
                                    size_hint: (.35,None)
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                    source:''
                                    
                                BoxLayout:
                                    orientation: "vertical"
                                    size_hint: (.4, None)
                                    pos_hint: {'center_y': 0.5}
                                    spacing: "10dp"  # Set the desired spacing  
                                    
                                    MDLabel:
                                        id: video_title
                                        text: ''
                                        size: self.texture_size      
                                    
                                    
                                        
                                    BoxLayout:        
                                        orientation: "horizontal"   
                                        size_hint: (None, .7)
                                        spacing: "5dp"  # Set the desired spacing  
   
                                        MDTextFieldRect:
                                            id: drop_down_btn
                                            text: "Resolution"
                                            readonly: True  # Set the text field as readonly
                                            size_hint: (None,0.9)  
                                            on_focus: if self.focus: app.show_resolution_menu(self)  # Show resolution menu on focus      
                                        
                                        DropDown:
                                            id: drop_down 
                                            
                                        
                                            
                            
                            
                            BoxLayout:
                                id: location_detail
                                orientation: "horizontal"
                                size_hint: (.9,None)
                                height: "48dp"
                                pos_hint: {'center_x': 0.5, 'center_y': 20}
                        
                                MDRectangleFlatButton:
                                    text: "Download Location"
                                    on_release: app.open_file_manager() if drop_down_btn.text != "Resolution" else None
                                                    
                                MDLabel:
                                    id: download_location
                                    text: "Choose Download Location"
                                    halign: "center" 
                                    
                            BoxLayout:
                                id: progress_bar_detail
                                orientation: "horizontal"
                                size_hint: (.9,None)
                                height: "18dp"
                                pos_hint: {'center_x': 0.5, 'center_y': 20}
                        
                                MDLabel:
                                    id: progress_label
                                    text: ""
                                    halign: "center" 
                        
                                                                            
                            BoxLayout:
                                id: video_playlist_detail
                                orientation: "horizontal"
                                pos_hint: {'center_x': 0.5, 'center_y': 20} 
                                size_hint: (.9,None)  
                                spacing: "10dp"   
                                
                                MDRaisedButton:
                                    text: "Download Video"
                                    pos_hint: {'center_y': 0.48}   
                                    on_release: app.downloadVideo(self)  # Call the function when the button is released   
                                    disabled: drop_down_btn.text == "Resolution" or not download_location.text or download_location.text == "Choose Download Location"
                                    
                                MDRaisedButton:
                                    text: "Download Playlist Instead"
                                    pos_hint: {'center_y': 0.48}
                                    on_release: app.downloadPlaylistVideo(self)  # Call the function when the button is released 
                                    disabled: drop_down_btn.text == "Resolution" or not download_location.text or download_location.text == "Choose Download Location"   
                                    halign: "center"  
                                    
                                
                                    
                                                    
 
"""