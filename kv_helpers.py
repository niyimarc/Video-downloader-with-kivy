screen_helper = """
MDScreen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Demo App"
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
                
                            Image:
                                source: 'img/youtube.png'
                                size_hint: (.5,None)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                                
                                
                            MDTextField:
                                id: link_input
                                hint_text: "Paste Youtube Video Link"
                                mode: "round"
                                helper_text: "Paste Youtube Video Link"
                                pos_hint: {'center_x': 0.4, 'center_y': 0.75}
                                size_hint: (.7,None)
                                
                            MDIconButton:
                                icon: "close-circle-outline"
                                pos_hint: {"center_y": .75}
                                pos: link_input.width - self.width + dp(8), 0
                                on_release: app.clear_link_field(link_input)
                                
                            MDRoundFlatButton:
                                text: "Get Link"
                                pos_hint: {'center_x': 0.86, 'center_y': 0.75}
                                size_hint: (None,None)
                                on_release: app.getLinkInfo(self)  # Call the function when the button is released
                                
                            
                            
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
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                                    MDLabel:
                                        id: video_title
                                        text: ''
                                        size: self.texture_size
                                        
                                        
                                    
                                    BoxLayout:        
                                        orientation: "horizontal"   
                                        spacing: "10dp"  # Set the desired spacing              
                                        MDRoundFlatButton:
                                            text: "Download"
                                            size_hint: (None,None)    
                                            on_release: app.downloadVideo(self)  # Call the function when the button is released    
                                        
                                        MDTextFieldRect:
                                            id: drop_down_btn
                                            text: "Resolution"
                                            size_hint: (None,0.7)  
                                            on_focus: if self.focus: app.show_resolution_menu(self)  # Show resolution menu on focus      
                                        
                                        DropDown:
                                            id: drop_down              
                                            
        
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
                    title: "Header title"
                    title_color: "#4a4939"
                    text: "Header text"
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