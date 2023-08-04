from pytube import YouTube
import yt_dlp
import customtkinter
from CTkMessagebox import CTkMessagebox
from PIL import Image

import sys
import os

# default button color theme
# self.set_default_color_theme("blue")

dark_mode_color=('#8f75ff', '#5d8ade')
warning_icon = './assets/819890869792145418.webp' #resource_path("819890869792145418.webp")
light_mode_image = './assets/app_icon.png' #resource_path("app_icon.png")

# widgets placement
default_left_most_val = 0.03
default_right_most_val = 0.97
default_top_most_val = 0.04
default_bottom_most_val = 0.9

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        def progress_hook(d):
            if d['status'] == 'downloading':
                progressbar.set(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))
                # print (dl_status)
            # if d['status'] == 'finished':
            #     filename=d['filename']
            #     print(filename)

        def url_failed(e):
            CTkMessagebox(title="ERROR!", message="WRONG LINK OR\nDOWNLOAD TYPE!", icon=warning_icon)
            url_entry.delete(0, customtkinter.END)
            print(f"An error occurred: {e}")

        def url_success():
            CTkMessagebox(title="DONE!", icon="check",width=75, height=30, message="Download Complete 👻")
            progressbar.set(0)
            url_entry.delete(0, customtkinter.END)

        def selected():
            if segemented_button_var.get() == "YOUTUBE MP4":
                # YOUTUBE URL
                download("youtubeMP4")
            elif segemented_button_var.get() == "FB | IG | TWITTER | TIKTOK":
                # FACEBOOK URL
                download("fb_ig_reels")
            elif segemented_button_var.get() == "YOUTUBE MP3":
                # YOUTUBE MP3
                download("youtubeMP3")
                
        def download(downloadType):
                    url = url_entry.get()
                    if downloadType == "youtubeMP4":
                        try:
                            ydl_opts = {
                                'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                                'outtmpl': os.path.join("./videoYT", '%(title)s.%(ext)s')
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
                            url_success()
                        except Exception as e:
                            url_failed(e)

                    if downloadType == "fb_ig_reels":
                        # FACEBOOK VIDS AND IG REELS
                        try:
                            ydl_opts = {
                                'format': 'bestvideo+bestaudio/best',
                                'merge_output_format': 'mp4',
                                'outtmpl': os.path.join("./FB_IG_TK", '%(title)s.%(ext)s'),
                                'progress_hooks': [progress_hook]
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
                            url_success()
                        except Exception as e:
                            url_failed(e)

                    if downloadType == "youtubeMP3":
                        # YOUTUBE MP3
                        try:
                            ydl_opts = {
                            'format': 'wav/bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'wav',
                            }],
                            'outtmpl': os.path.join("./YTMP3", '%(title)s.%(ext)s'),
                            'progress_hooks': [progress_hook]
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
                            url_success()
                        except Exception as e:
                            url_failed(e)

        def open_folder():
            os.startfile(r'')

        def close_window():
            self.quit()
            
        def change_appearance_mode_event(values):
            if values == "System":
                customtkinter.set_appearance_mode("System")
            elif values == "Light":
                customtkinter.set_appearance_mode("Light")
            elif values == "Dark":
                customtkinter.set_appearance_mode("Dark")

        self.title("Kuro Downloader")   
        self.minsize(600, 300)
        self.maxsize(600, 300)

        # progress bar
        progressbar_label = customtkinter.CTkLabel(self, text="Download Progress")
        # progressbar_label.place(relx=.05, rely=.4, anchor=customtkinter.W)
        progressbar = customtkinter.CTkProgressBar(self, progress_color=dark_mode_color, width=250, orientation="horizontal")
        progressbar.set(0)
        progressbar.place(relx=default_left_most_val, rely=default_top_most_val+.4, anchor=customtkinter.W)

        # Info
        info_label = customtkinter.CTkLabel(self, text="HEY!\nNot responding = processing, chill ;3\n\nCHOOSE DOWNLOAD TYPE ABOVE!\n\nIf you want to stop downloading, just close the program")
        ver_label = customtkinter.CTkLabel(self, text="Ver 0.1")

        # Segmented Button
        segmented_button_label = customtkinter.CTkLabel(self, text="CHOOSE DOWNLOAD TYPE")
        segemented_button_var = customtkinter.StringVar(value="YOUTUBE MP4")  # set initial value
        segemented_button = customtkinter.CTkSegmentedButton(self, height=40, selected_color=dark_mode_color, values=["YOUTUBE MP4", "FB | IG | TWITTER | TIKTOK", "YOUTUBE MP3"],variable=segemented_button_var)
        segmented_button_label.place(relx=default_left_most_val, rely=default_top_most_val, anchor=customtkinter.NW)
        segemented_button.place(relx=default_right_most_val, rely=default_top_most_val, anchor=customtkinter.NE)

        # url label and entry box
        url_label = customtkinter.CTkLabel(self, text="Enter URL:")
        url_entry = customtkinter.CTkEntry(self, width=250, placeholder_text="Enter URL")
        url_label.place(relx=default_left_most_val, rely=default_top_most_val+.2 , anchor=customtkinter.W)
        url_entry.place(relx=default_left_most_val, rely=default_top_most_val+.3 , anchor=customtkinter.W)

        # appearance combo box
        appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance:")
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, fg_color=dark_mode_color, button_color=dark_mode_color, width=24, values=["System", "Dark", "Light"],command=change_appearance_mode_event)
 
        # download button
        download_btn = customtkinter.CTkButton(self, fg_color=dark_mode_color, width=14, hover_color="medium purple", text="Download", command=selected)
        download_btn.place(relx=default_left_most_val, rely=default_bottom_most_val, anchor=customtkinter.SW)
        # download_btn.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="sw")

        # quit button
        quit_btn = customtkinter.CTkButton(self, fg_color=dark_mode_color, width=24, hover_color="orange red", text="Quit", command=close_window)
        quit_btn.place(relx=default_right_most_val, rely=default_bottom_most_val, anchor=customtkinter.SE)

app = App()
app.mainloop()