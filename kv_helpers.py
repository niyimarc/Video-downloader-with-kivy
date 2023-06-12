screen_helper = """
MDScreen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Drey Tech"
                        elevation: 4
                        pos_hint: {"top": 1}
                        specific_text_color: "#4a4939"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]

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
                                    source: 'img/youtube.png'
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
                                        on_focus:
                                            if self.focus: self.select_all()
                          
                                        
                                    MDRaisedButton:
                                        id: get_link
                                        text: "Get Link"
                                        pos_hint: {'center_x': 0.86, 'center_y': 0.95}
                                        on_release: app.getLinkInfo(self)  # Call the function when the button is released
                                        disabled: not link_input.text or not link_input.text.startswith(("https://youtu.be/", "https://www.youtube.com/"))
                                
                            BoxLayout:
                                id: video_details
                                orientation: "horizontal"
                                pos_hint: {'center_x': 0.5, 'center_y': 20}
                                    
                                AsyncImage:
                                    id: async_image
                                    size_hint: (.5,None)
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                    source:''
                                    
                                BoxLayout:
                                    orientation: "vertical"
                                    size_hint: (.5, None)
                                    pos_hint: {'center_y': 0.5}
                                    spacing: "10dp"  # Set the desired spacing  
                                    
                                    MDLabel:
                                        id: video_title
                                        text: ''
                                        size: self.texture_size      
                                    
                                    
                                        
                                    BoxLayout:        
                                        orientation: "horizontal"   
                                        spacing: "5dp"  # Set the desired spacing  
   
                                        MDTextFieldRect:
                                            id: drop_down_btn
                                            text: "Resolution"
                                            size_hint: (None,0.8)  
                                            on_focus: if self.focus: app.show_resolution_menu(self)  # Show resolution menu on focus      
                                        
                                        DropDown:
                                            id: drop_down 
                                            
                                        MDRaisedButton:
                                            text: "Download"
                                            size_hint: (None,0.8)    
                                            on_release: app.downloadVideo(self)  # Call the function when the button is released   
                            BoxLayout:
                                id: video_playlist_detail
                                orientation: "horizontal"
                                pos_hint: {'center_x': 0.16, 'center_y': 20} 
                                size_hint: (None,None)     
                                
                                MDRaisedButton:
                                    text: "Download Playlist Instead"
                                    pos_hint: {'center_y': 0.48}
                                    on_release: app.downloadPlaylistVideo(self)  # Call the function when the button is released                          
                                                   
                        MDBottomNavigationItem:
                            name: 'screen 2'
                            text: 'Facebok'
                            icon: 'facebook'
                
                            MDLabel:
                                text: 'Facebook'
                                halign: 'center'
                
                                    
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            MDNavigationDrawerMenu:
    
                MDNavigationDrawerHeader:
                    title: "Drey Tech"
                    title_color: "#4a4939"
                    text: "app"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"
    
                MDNavigationDrawerLabel:
                    text: "Video Downloader"
                    
                MDNavigationDrawerItem
                    icon: "youtube"
                    text: "Youtube Downloader"
                
                MDNavigationDrawerItem
                    icon: "facebook"
                    text: "Facebok Downloader"                
 
"""