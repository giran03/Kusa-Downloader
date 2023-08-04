import yt_dlp
import customtkinter
from CTkMessagebox import CTkMessagebox
import subprocess

import sys
import os

def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

app_ver = '@Girandayoo | Ver 1.0'
dark_mode_color=('#8f75ff', '#5d8ade')
window_icon = resource_path("favico.ico") #resource_path("favico.ico") | './assets/favico.ico'
warning_icon = './assets/819890869792145418.webp' #resource_path("819890869792145418.webp") | './assets/819890869792145418.webp'

# widgets placement
default_left_most_val = 0.03
default_right_most_val = 0.97
default_top_most_val = 0.04
default_bottom_most_val = 0.9

class DownloadSuccessWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        def close_window():
            self.destroy()
            self.update()
        
        self.minsize(250,80)
        self.maxsize(250,80)
        self.title("DOWNLOAD DONE!")

        self.success_text = customtkinter.CTkLabel(self, text="Download Complete! ;)")
        self.success_text.pack(padx=25, pady=25, anchor=customtkinter.CENTER)
        self.after(1500, close_window)

class DownloadFailedWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        def close_window():
            self.destroy()
            self.update()
        
        self.minsize(450,80)
        self.maxsize(450,80)
        self.title("DOWNLOAD FAILED!")
        
        failed_text = "Must be wrong link, download type, or file already exists!"
        self.success_text = customtkinter.CTkLabel(self, text=failed_text)
        self.success_text.pack(padx=25, pady=25, anchor=customtkinter.CENTER)    
        self.after(2500, close_window)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.download_success_window = None
        self.download_failed_window = None

        def progress_hook(d):
            if d['status'] == 'downloading':
                info_label.insert("0.0","downloading...\n"+ "Time Elapsed " + str(int(d['elapsed'])) +"\n\n")
                info_label.insert("1.0","megabytes downloaded: "+ str(int(d['downloaded_bytes'])/100000) +"\n\n")
                info_label.update()
            if d['status'] == 'finished':
                info_label.insert("0.0", "Filename: " + d['filename'] +"\n\n")
                info_label.insert("1.0", "Done Downloading! Finalization\nplease wait...\n\n")
                url_success()

        def url_failed(e):
            if e == "'int' object is not subscriptable":
                print("")
            info_label.delete("0.0", "end")
            info_label.insert("0.0", "Must be wrong link or download type!")
            info_label.update()
            if self.download_failed_window is None or not self.download_failed_window.winfo_exists():
                self.download_failed_window = DownloadFailedWindow(self)  # create window if its None or destroyed
            else:
                self.download_failed_window.focus()  # if window exists focus it
            url_entry.delete(0, customtkinter.END)
            print(f"An error occurred: {e}")

        def url_success():
            if self.download_success_window is None or not self.download_success_window.winfo_exists():
                self.download_success_window = DownloadSuccessWindow(self)  # create window if its None or destroyed
            else:
                self.download_success_window.focus()  # if window exists focus it
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
                    info_label.delete("0.0", "end")
                    info_label.insert("0.0", "URL Received, Please wait...\n\nIf download doesn't start,\nThe file already exists.")
                    info_label.update()                 
                    if downloadType == "youtubeMP4":
                        try:
                            ydl_opts = {
                                'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                                'outtmpl': os.path.join("./downloads/Youtube_MP4", '%(title)s.mp4'),
                                'progress_hooks': [progress_hook],
                                'noplaylist': True
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
                        except Exception as e:
                            url_failed(e)

                    if downloadType == "fb_ig_reels":
                        # FACEBOOK VIDS AND IG REELS
                        try:
                            ydl_opts = {
                                'format': 'bestvideo+bestaudio/best',
                                'merge_output_format': 'mp4',
                                'outtmpl': os.path.join("./downloads/FB_IG_TWI_TK", '%(title)s.mp4'),
                                'progress_hooks': [progress_hook],
                                'noplaylist': True
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
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
                            'outtmpl': os.path.join("./downloads/Youtube_MP3", '%(title)s.%(ext)s'),
                            'progress_hooks': [progress_hook],
                            'noplaylist': True
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as u:
                                u.download([url])
                        except Exception as e:
                            url_failed(e)

        def open_folder():
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            subprocess.Popen(r'explorer /open, downloads')

        def close_window():
            self.quit()
    
        self.title("Kusa Downloader")
        self.iconbitmap(window_icon)
        self.minsize(600, 400)
        self.maxsize(600, 400)

        # load download type info     
        download_info_label = customtkinter.CTkTextbox(self, wrap='word', width=250, height=250)
        download_info_label.insert("0.0", "\tDOWNLOADING TIPS\n\t            (>‿◠)✌\n\nCopy paste the YT link from the search bar or use 'copy link address'\n\n")
        download_info_label.insert("5.0", "Use links from 'Share button > Copy Link' in FB Vid, IG Reels, Twitter Vid, Tiktok Vid\n")
        download_info_label.insert("11.0", "Check all of the supported sites here: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md\n\n")
        download_info_label.insert("14.0", "Not responding = processing,\nchill (ɔ◔‿◔)ɔ ♥\n\nto stop from downloading, just force close me (╥﹏╥)\n\n")
        # download_info_label.insert("19.0", "After clicking  download button...\n\nlet me cook bruh dont rush\n\n")
        download_info_label.configure(state="disabled")
        download_info_label.place(relx=default_right_most_val, rely=default_top_most_val+.45, anchor=customtkinter.E)

        # Info
        info_label = customtkinter.CTkTextbox(self, wrap='word', width=250, height=160)
        info_label.place(relx=default_left_most_val, rely=default_bottom_most_val, anchor=customtkinter.SW)
        ver_label = customtkinter.CTkLabel(self, text=app_ver)
        ver_label.place(relx=default_right_most_val, rely=default_bottom_most_val+.1, anchor=customtkinter.SE)

        # Segmented Button
        segmented_button_label = customtkinter.CTkLabel(self, text="CHOOSE DOWNLOAD TYPE")
        segemented_button_var = customtkinter.StringVar(value="YOUTUBE MP4")  # set initial value
        segemented_button = customtkinter.CTkSegmentedButton(self, height=40, selected_color=dark_mode_color, 
                                                             values=["YOUTUBE MP4", "FB | IG | TWITTER | TIKTOK", "YOUTUBE MP3"],
                                                             variable=segemented_button_var)
        segmented_button_label.place(relx=default_left_most_val, rely=default_top_most_val, anchor=customtkinter.NW)
        segemented_button.place(relx=default_right_most_val, rely=default_top_most_val, anchor=customtkinter.NE)

        # url label and entry box
        url_label = customtkinter.CTkLabel(self, text="Enter URL:")
        url_entry = customtkinter.CTkEntry(self, width=250, placeholder_text="Enter URL")
        url_label.place(relx=default_left_most_val, rely=default_top_most_val+.2 , anchor=customtkinter.W)
        url_entry.place(relx=default_left_most_val, rely=default_top_most_val+.3 , anchor=customtkinter.W)

        # open downloads folder button
        open_folder_btn = customtkinter.CTkButton(self, fg_color=dark_mode_color, width=14, hover_color="medium purple", text="Downloads Folder", command=open_folder)
        open_folder_btn.place(relx=default_left_most_val+.13, rely=default_top_most_val+.4, anchor=customtkinter.W)
 
        # download button
        download_btn = customtkinter.CTkButton(self, fg_color=dark_mode_color, width=14, hover_color="medium purple", text="Download", command=selected)
        download_btn.place(relx=default_left_most_val, rely=default_top_most_val+.4, anchor=customtkinter.W)

        # quit button
        quit_btn = customtkinter.CTkButton(self, fg_color=dark_mode_color, width=24, hover_color="orange red", text="Quit", command=close_window)
        quit_btn.place(relx=default_right_most_val, rely=default_bottom_most_val, anchor=customtkinter.SE)

app = App()
app.mainloop()