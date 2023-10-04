import pygame
import tkinter as tk
from tkinter import ttk
import time as t
from mutagen.mp3 import MP3
from tkinter import messagebox
from tkinter import filedialog as f
import keyboard as k
import os
import sqlite3 as sq
import random as r
import subprocess
# set base values_____________________________________________________________________
p = pygame.mixer
paused = False
stopped = False
changed = False
next_click = False
clicked = False
enter1 = False
played = False
end_list = False
choicing = False
muted = False
change_song = False
song1 = ""
font_choosing = ""
rand = False
sec_run = 0
bdata = []
di_list = []
pygame.init()
p.init()

# set functions_______________________________________________________________________


def current_di():
    global cur_di
    cur_di = os.path.dirname(os.path.abspath(__file__))


current_di()


def shortcut():
    exist = os.path.exists(
        "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/M.K Player.lnk")

    def run():
        subprocess.call([f"{cur_di}/shortcut.exe", '-c',
                         '"DSN=demo2suite;UID=dba;PWD=sql"', '-y', '"D://Databases//AMOS2//LIVE//LIVE_BCK"'])
        root2.destroy()
    if exist == False:
        shortcut_btn = tk.Button(
            root2, text="Add shortcut to start menu", font=(font_choosing, 8), command=lambda: run())
        shortcut_btn.grid(row=9, column=0, padx=(0, 345))
    else:
        save_note.grid_configure(padx=0)


def query_setting():
    global font_choosing
    conn = sq.connect(
        (f"{cur_di}/settingdb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM settingdb")
    fetch = c.fetchall()
    for setting in fetch:
        if setting[0] == "":
            font_choosing = "Arial"
        else:
            font_choosing = setting[0]
    if len(fetch) == 0:
        font_choosing = "Arial"
    conn.commit()
    conn.close()


query_setting()


def add_song_box():
    global address1, directory1
    try:
        directory1 = [f.askdirectory(title="Select Music Directory")]
        for address1 in directory1:
            location = os.listdir(address1)
        for song in location:
            if song.endswith(".mp3"):
                song = song.replace(directory1[0], "")
                song = song.replace(".mp3", "")
                song_box.insert(tk.END, song)
        di_save()
    except:
        messagebox.showinfo(
            message="You didn't choose any directory", title="Directory error")


def change_music():
    global change_song
    if stopped == False:
        if song_box.get(tk.ACTIVE) == song1:
            change_song = False
            music_lenth.after(100, change_music)
        else:
            change_song = True
            my_slider.config(value=0)
            music_lenth.config(text=f"00:00 of {song_clock_time}")
            play()
            music_lenth.after(100, change_music)
            choice2()


def play():
    global enter1, played, stopped, end_list, choicing, paused, song1
    try:
        song = song_box.get(tk.ACTIVE)
        if fetch1 == []:
            song = f"{directory1[0]}/{song}.mp3"
        else:
            song = f"{di[0]}/{song}.mp3"
        p.music.load(song)
        p.music.play(loops=1)
        p.music.get_busy()
        pygame.time.Clock().tick(10)
        song_box.select_set(tk.ACTIVE)
        played = True
        stopped = False
        end_list = False
        choicing = True
        paused = False
        if fetch1 == []:
            song1 = song.replace(directory1[0], "")
        else:
            song1 = song.replace(di[0], "")
        song1 = song1.replace("/", "")
        song1 = song1.replace(".mp3", "")
        volume()
        if enter1 == False:
            enter1 = True
            enter()
    except:
        messagebox.showinfo(
            message="You didn't choose any music!", title="Music play error")


def stop():
    global played, choicing, stopped
    p.music.stop()
    stopped = True
    played = False
    choicing = False
    my_slider.config(value=0)
    song_box.selection_clear(tk.ACTIVE)
    music_lenth.config(text=f"00:00 of 00:00")
    choice2()


def pause():
    global paused, next_click, played, choicing, stopped
    if played:
        if next_click:
            play()
        else:
            if change_song == False:
                if paused:
                    p.music.unpause()
                    paused = False
                    choicing = True
                else:
                    p.music.pause()
                    paused = True
                    choicing = False
    else:
        play()
    choice2()


def next_song():
    global next_click, paused, stopped, end_list, choicing, i
    try:
        next_click = True
        paused = False
        stopped = False
        choicing = True
        next_one = song_box.curselection()
        if rand:
            all = song_box.get(0, tk.END)
            next_one = r.choice(all)
            song = next_one
            for i in range(len(all)):
                if all[i] == song:
                    song_box.selection_clear(0, tk.END)
                    song_box.activate(str(i))
                    song_box.selection_set(i, last=None)
                    song_box.yview(i)
        else:
            next_one = next_one[0]+1
            song = song_box.get(next_one)
            song_box.selection_clear(0, tk.END)
            song_box.activate(next_one)
            song_box.selection_set(next_one, last=None)
        if fetch1 == []:
            song = f"{directory1[0]}/{song}.mp3"
        else:
            song = f"{di[0]}/{song}.mp3"
        p.music.load(song)
        p.music.play(loops=1)
        p.music.get_busy()
        pygame.time.Clock().tick(10)
        choice2()
    except:
        stop()
        messagebox.showinfo(
            message="You got to end of the list", title="End of the list")
        end_list = True


def back_song():
    global next_click, paused, stopped, end_list, choicing
    try:
        next_click = True
        paused = False
        stopped = False
        end_list = False
        choicing = True
        next_one = song_box.curselection()
        if rand:
            all = song_box.get(0, tk.END)
            next_one = r.choice(all)
            song = next_one
            for i in range(len(all)):
                if all[i] == song:
                    song_box.selection_clear(0, tk.END)
                    song_box.activate(str(i))
                    song_box.selection_set(i, last=None)
                    song_box.yview(i)
        else:
            next_one = next_one[0]-1
            song = song_box.get(next_one)
            song_box.selection_clear(0, tk.END)
            song_box.activate(next_one)
            song_box.selection_set(next_one, last=None)
        if fetch1 == []:
            song = f"{directory1[0]}/{song}.mp3"
        else:
            song = f"{di[0]}/{song}.mp3"
        p.music.load(song)
        p.music.play(loops=1)
        p.music.get_busy()
        pygame.time.Clock().tick(10)
        choice2()
    except:
        stop()
        messagebox.showinfo(
            message="You got to top of the list", title="End of the list")
        end_list = True


def delete_song():
    song_box.delete(tk.ANCHOR)
    p.music.stop()


def delet_all_songs():
    song_box.delete(0, tk.END)
    p.music.stop()


def change():
    song_box.itemconfig(tk.ACTIVE, {"bg": change_color_combo.get()})
    database()


def remove_color():
    song_box.itemconfig(tk.ACTIVE, {"bg": ""})
    delete()


def slide_click():
    global clicked
    clicked = True


def finish():
    music_lenth.config(text=f"00:00 of {song_clock_time}")
    my_slider.configure(value=0, to=song_total_time)
    if end_list == False:
        next_song()
        music_lenth.after(1000, enter)
    else:
        music_lenth.after(10, finish)


def enter():
    global clicked, next_click, song_total_time, song_clock_time, played
    if end_list == False:
        if paused == False:
            if stopped == False:
                if clicked:
                    p.music.set_pos(int(my_slider.get()))
                    clicked = False
                    current_time = int(my_slider.get())
                else:
                    current_time = int(my_slider.get())
                    if next_click:
                        current_time = 0
                        next_click = False
                current_time += 1
                clock_time = t.strftime("%M:%S", t.gmtime(current_time))
                song = song_box.get(tk.ACTIVE)
                if fetch1 == []:
                    song = f"{directory1[0]}/{song}.mp3"
                else:
                    song = f"{di[0]}/{song}.mp3"
                song_total_time = MP3(song).info.length
                song_clock_time = t.strftime(
                    "%M:%S", t.gmtime(song_total_time))
                if clock_time == song_clock_time:
                    finish()
                elif change_song == False:
                    music_lenth.config(
                        text=f"{clock_time} of {song_clock_time}")
                    my_slider.configure(value=current_time, to=song_total_time)
                    change_music()
                    music_lenth.after(1000, enter)
            else:
                my_slider.configure(value=0, to=song_total_time)
                music_lenth.config(text=f"00:00 of 00:00")
                music_lenth.after(1000, enter)
        else:
            music_lenth.after(1000, enter)
    else:
        music_lenth.after(10, finish)


def volume():
    if muted:
        p.music.set_volume(0)
        volume_img.config(image=mute_img)
        volume_label.config(text="Mute")
    else:
        p.music.set_volume(volume_slider.get())
        volume_label.config(text=f"Volume: {int(volume_slider.get()*100)}%")
        choice()
        volume_label.after(10, volume)


def choice():
    if p.music.get_volume() >= 0.7:
        volume_img.config(image=volume_max_img)
    elif 0.7 > p.music.get_volume() >= 0.4:
        volume_img.config(image=volume_mid_img)
    elif 0.4 > p.music.get_volume() > 0:
        volume_img.config(image=volume_min_img)
    elif p.music.get_volume() == 0:
        volume_img.config(image=mute_img)
        volume_label.config(text="Mute")


def choice2():
    if choicing:
        pause_btn.config(image=pause_btn_img)
    else:
        pause_btn.config(image=play_btn_img)


def mute():
    global muted
    if muted:
        muted = False
    else:
        muted = True
    volume()


def di_save():
    delete2()
    conn = sq.connect(
        (f"{cur_di}/directorydb.db"))
    c = conn.cursor()
    c.execute("INSERT INTO directorydb VALUES(:di_address)",
              {
                  "di_address": address1
              })
    conn.commit()
    conn.close()


def delete2():
    conn = sq.connect(
        (f"{cur_di}/directorydb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM directorydb")
    fetch = c.fetchall()
    for i in fetch:
        if i[0] == address1:
            index = i[1]
            c.execute(
                "DELETE from directorydb WHERE oid = " + str(index))
    conn.commit()
    conn.close()


def query_di():
    global di, fetch1
    conn = sq.connect(
        (f"{cur_di}/directorydb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM directorydb")
    fetch1 = c.fetchall()
    for di in fetch1:
        di_list.append(di[0])
        loc = os.listdir(di[0])
        for song in loc:
            if song.endswith(".mp3"):
                song = song.replace(di[0], "")
                song = song.replace(".mp3", "")
                song_box.insert(tk.END, song)
                bdata.append(song)
    conn.commit()
    conn.close()


def album():
    global fetch2
    conn = sq.connect(
        (f"{cur_di}/music_colordb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM music_colordb")
    fetch2 = c.fetchall()
    for name in fetch2:
        def get_index(value):
            items = song_box.get(0, tk.END)
            for m in range(len(items)):
                if items[m] == value:
                    color1 = song_box.itemcget(m, "bg")
        get_index(name[0])
    conn.commit()
    conn.close()


def album_show():
    global show_color
    color = ["red", "yellow", "pink", "gray",
             "lightblue", "lightgreen", "All"]
    change_color_lable.config(text="Choose the color of album")
    change_color_btn.pack_forget()
    change_color_remove.pack_forget()
    change_color_combo.config(value=color)

    def part():
        if change_color_combo.get() == "All":
            song_box.delete(0, tk.END)
            query_di()
            query()
        else:
            album()
            song_box.delete(0, tk.END)
            for n in fetch2:
                if n[1] == change_color_combo.get():
                    song_box.insert(tk.END, n[0])
                    song_box.itemconfig(tk.END, {"bg": n[1]})
    show_color = tk.Button(
        change_color, text="Show musics", command=lambda: part())
    change_combo_lable.pack(side="left", ipadx=23)
    change_color_combo.pack(side="left", padx=30)
    show_color.pack(side="left", padx=35)


def choose_color():
    song_box.delete(0, tk.END)
    query_di()
    query()
    colors = ["red", "yellow", "pink", "gray",
              "lightblue", "lightgreen"]
    show_color.pack_forget()
    change_color_lable.config(text="Change the color of selected music")
    change_combo_lable.pack(side="left", padx=15, ipadx=0)
    change_color_combo.pack(side="left", padx=15)
    change_color_btn.pack(side="left", padx=15)
    change_color_remove.pack(side="left", padx=15)
    change_color_combo.config(value=colors)


def update(data):
    song_box.delete(0, tk.END)
    for item in data:
        song_box.insert(tk.END, item)
    query()


def check(e):
    song_box.config(state="normal")
    try:
        typed = search_bar.get()
        if typed == "":
            data = bdata
        else:
            for item in bdata:
                if typed.lower() in item.lower():
                    data = []
                    data.append(item)
        update(data=data)
    except:
        song_box.delete(0, tk.END)
        song_box.insert(tk.END, "No result!")
        song_box.config(state="disabled")


def temp_text(e):
    stop()
    if search_bar.get() == "Type here...":
        song_box.selection_clear(tk.ACTIVE)
        search_bar.config(fg="black")
        search_bar.delete(0, tk.END)


def back_text(e):
    if search_bar.get() == "":
        search_bar.config(fg="gray")
        search_bar.insert(0, "Type here...")


def rename_song():
    song_name = song_box.get(tk.ACTIVE)
    song_color = song_box.itemcget(tk.ACTIVE, "bg")
    delete()
    conn = sq.connect(
        (f"{cur_di}/music_colordb.db"))
    c = conn.cursor()
    c.execute("INSERT INTO music_colordb VALUES(:music_name,:color)",
              {
                  "music_name": right_entry.get(),
                  "color": song_color
              })
    conn.commit()
    conn.close()

    loc = os.listdir(di[0])
    for song in loc:
        if song.endswith(".mp3"):
            song = song.replace(di[0], "")
            song = song.replace(".mp3", "")
            if song == song_name:
                os.rename(f"{di[0]}/{song_name}.mp3",
                          f"{di[0]}/{right_entry.get()}.mp3")
                song_box.delete(0, tk.END)
                query_di()
                query()
                root5.destroy()


def rename():
    global right_entry, root5
    stop()

    def text(e):
        if right_entry.get() == "Type new name here...":
            right_entry.delete(0, tk.END)
            right_entry.config(fg="black")

    def textout(e):
        if right_entry.get() == "":
            right_entry.insert(0, "Type new name here...")
            right_entry.config(fg="gray")
    song = song_box.get(tk.ACTIVE)
    root5 = tk.Tk()
    right_entry = tk.Entry(root5, font=(
        font_choosing, 13), fg="gray", borderwidth=1)
    rename_btn = tk.Button(root5, text="Rename the active song", font=(
        font_choosing, 10), command=lambda: rename_song())
    if song == "":
        song = "No music actived"
    right_lable = tk.Label(root5, font=(font_choosing, 10),
                           text=f"Current song: {song}")

    if 60 > len(song) > 30:
        length = 500
        right_entry.config(width=50)
    elif len(song) > 60:
        length = 800
        right_entry.config(width=80)
    else:
        length = 300
        right_entry.config(width=25)
    root5.geometry(f"{length}x150")
    right_lable.pack(pady=10)
    right_entry.pack(pady=10)
    rename_btn.pack(pady=10)
    right_entry.insert(0, "Type new name here...")
    right_entry.bind("<FocusIn>", text)
    right_entry.bind("<FocusOut>", textout)
    root5.mainloop()


def popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)


def close():
    try:
        root.destroy()
    except:
        pass
    try:
        root2.destroy()
    except:
        pass
    try:
        root3.destroy()
    except:
        pass
    try:
        root4.destroy()
    except:
        pass
    try:
        root5.destroy()
    except:
        pass


def setting_menu():
    global font_choosing, root2, save_note
    # set functions+++++++++++++++

    def save2():
        global font_choosing
        delete_setting()
        conn = sq.connect(
            (f"{cur_di}/settingdb.db"))
        c = conn.cursor()
        c.execute("INSERT INTO settingdb VALUES(:font_name)",
                  {
                      "font_name": fonts_combo.get()
                  })
        conn.commit()
        conn.close()
        messagebox.showinfo(message="Saved!")

    def delete_setting():
        conn = sq.connect(
            (f"{cur_di}/settingdb.db"))
        c = conn.cursor()
        c.execute("SELECT *,oid FROM settingdb")
        fetch = c.fetchall()
        for setting in fetch:
            index = setting[1]
            c.execute(
                "DELETE from settingdb WHERE oid = " + str(index))
        conn.commit()
        conn.close()

    def delete_directory():
        stop()
        conn = sq.connect(
            (f"{cur_di}/directorydb.db"))
        c = conn.cursor()
        c.execute("SELECT *,oid FROM directorydb")
        fetch = c.fetchall()
        for di in fetch:
            pass

        def get_index(value):
            items = directory_box.get(0, tk.END)
            for i in range(len(items)):
                if items[i] == value:
                    index = di[1]
                    c.execute(
                        "DELETE from directorydb WHERE oid = " + str(index))
                    directory_box.delete(tk.ACTIVE)
        get_index(directory_box.get(tk.ANCHOR))
        conn.commit()
        conn.close()
        song_box.delete(0, tk.END)
        query_di()

    def insert():
        conn = sq.connect(
            (f"{cur_di}/directorydb.db"))
        c = conn.cursor()
        c.execute("SELECT *,oid FROM directorydb")
        fetch = c.fetchall()
        for di in fetch:
            loc = di[0]
            directory_box.insert(tk.END, loc)
        conn.commit()
        conn.close()
        conn2 = sq.connect(
            (f"{cur_di}/settingdb.db"))
        c2 = conn2.cursor()
        c2.execute("SELECT *,oid FROM settingdb")
        fetch2 = c2.fetchall()
        for font in fetch2:
            font_choosing = font[0]
            fonts_current.config(text=f"Current font is {font_choosing}")
        conn2.commit()
        conn2.close()

    # root2 base++++++++++
    root2 = tk.Tk()
    root2.title("Settings")
    root2.resizable(False, False)
    root2.geometry("500x350")
    # change font+++++++++++++++++
    Fonts = ["System",
             "Modern", "Roman", "Courier", "Arial"]
    fonts_frame = tk.Frame(root2)
    fonts_header = tk.Label(
        root2, text=f"Font changing menu", font=(font_choosing, 12))
    fonts_current = tk.Label(
        fonts_frame, text=f"Current font is {font_choosing}", font=(font_choosing, 10))
    fonts_lable = tk.Label(fonts_frame, text="Fonts", font=(font_choosing, 10))
    fonts_combo = ttk.Combobox(fonts_frame, textvariable=Fonts,
                               font=("", 10), values=Fonts)
    fonts_header.grid(row=0, column=0, pady=5, padx=25)
    fonts_current.grid(row=0, column=2, pady=10)
    fonts_frame.grid(row=1, column=0, pady=10)
    fonts_lable.grid(row=0, column=0, padx=10)
    fonts_combo.grid(row=0, column=1, padx=10)

    def combo_font():
        try:
            fonts_combo.config(font=(fonts_combo.get(), 10))
            music_lenth.after(10, combo_font)
        except:
            pass
    combo_font()
    # directory menu+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    directory_menu = tk.Label(
        root2, text=f"Directory menu", font=(font_choosing, 12))
    directory_frame = tk.Frame(root2)
    directory_box = tk.Listbox(directory_frame, bg="white", fg="black",
                               bd=3, selectbackground="gray", selectforeground="white", height=5, width=40, font=(font_choosing, 13))
    directory_delete_btn = tk.Button(
        directory_frame, text="Delete directory", font=(font_choosing, 10), command=lambda: delete_directory())
    end_label = tk.Label(root2, text="-"*99)
    directory_menu.grid(row=4, column=0)
    directory_frame.grid(row=5, column=0)
    directory_box.grid(row=0, column=0)
    directory_delete_btn.grid(row=1, column=0, pady=5)
    end_label.grid(row=7, column=0)
    # save chagnes++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    save_btn = tk.Button(root2, text="Save Changes", font=(
        font_choosing, 10), command=lambda: save2())
    save_note = tk.Label(
        root2, text="Note: Evrything will change after you restart the app!", font=(font_choosing, 8))
    save_btn.grid(row=8, column=0)
    save_note.grid(row=9, column=0, pady=(5, 0), padx=(70, 0))
    insert()
    shortcut()
    root2.mainloop()


# databases(music_colordb)_______________________________________________________________________________________


def query():
    conn = sq.connect(
        (f"{cur_di}/music_colordb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM music_colordb")
    fetch = c.fetchall()
    for insert_colors in fetch:
        def get_index(value):
            items = song_box.get(0, tk.END)
            try:
                for i in range(len(items)):
                    if items[i] == value:
                        song_box.itemconfig(i, {"bg": insert_colors[1]})
            except:
                messagebox.showinfo(
                    message="Coloring error: Music not found for coloring!", title="Coloring error")
        get_index(insert_colors[0])
    conn.commit()
    conn.close()


def delete():
    conn = sq.connect(
        (f"{cur_di}/music_colordb.db"))
    c = conn.cursor()
    c.execute("SELECT *,oid FROM music_colordb")
    fetch = c.fetchall()
    for insert_colors in fetch:
        if insert_colors[0] == song_box.get(tk.ACTIVE):
            index = insert_colors[2]
            c.execute(
                "DELETE from music_colordb WHERE oid = " + str(index))
    conn.commit()
    conn.close()


def database():
    delete()
    if song_box.itemcget(tk.ACTIVE, "bg") == "":
        color = "white"
    else:
        color = song_box.itemcget(tk.ACTIVE, "bg")
    conn = sq.connect(
        (f"{cur_di}/music_colordb.db"))
    c = conn.cursor()
    c.execute("INSERT INTO music_colordb VALUES(:music_name,:color)",
              {
                  "music_name": song_box.get(tk.ACTIVE),
                  "color": color
              })
    conn.commit()
    conn.close()


def about_app():
    global root3
    root3 = tk.Tk()
    root3.title("About App")
    root3.resizable(False, False)
    tk.Label(root3, text="""This app developed by Matin R. Keshavarz
Telegram ID: @MatinK84""", font=(font_choosing, 11)).pack(pady=(0, 10))
    tk.Label(root3, text="policies and privacy:", font=(
        font_choosing, 13)).pack()
    tk.Label(root3, text="""1- All rights of this program are reserved and exclusive to Matin R. Keshavarz,
2- Copyright of this program is prohibited and prosecuted""", font=(font_choosing, 11)).pack()
    root3.mainloop()


def randome_p():
    global rand
    if rand == False:
        rand = True
    else:
        rand = False
    choice3()


def choice3():
    if rand:
        rand_btn.config(image=rand_img)
    else:
        rand_btn.config(image=con_img)


def guide():
    global root4
    root4 = tk.Tk()
    root4.title("Guide Notes")
    tk.Label(root4, text="""1-This app can only play MP3 files.
2-App works corroctly after playing music. 
3-There are some keys that helps you using app:
Play/Pause => Control+Alt+Space key,
Stop => Control+Alt+S key,
Next Track => Control+Alt+N key,
Previous Track => Control+Alt+B key,
Mute => Control+Alt+M key,
and Random/ListPLay => Control+Alt+R key""", font=(font_choosing, 11)).pack()
    root4.mainloop()


# hot keys_______________________________________________________________________________________
k.add_hotkey("Control+Alt+space", pause)
k.add_hotkey("Control+Alt+s", stop)
k.add_hotkey("Control+Alt+n", next_song)
k.add_hotkey("Control+Alt+b", back_song)
k.add_hotkey("Control+Alt+m", mute)
k.add_hotkey("Control+Alt+r", randome_p)
# base window____________________________________________________________________________________
root = tk.Tk()
root.title("M.K Mp3 Player")
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(
    file=(f"{cur_di}/M.png")))
root.geometry("600x550")
root.protocol("WM_DELETE_WINDOW", close)
# search bar_______________________________________________________________________________________
search_bar = tk.Entry(root, fg="gray", font=(
    font_choosing, 13), width=64, borderwidth=1)
search_bar.pack(side="top", pady=5)
search_bar.insert(0, "Type here...")
search_bar.config()
search_bar.bind("<FocusIn>", temp_text)
search_bar.bind("<FocusOut>", back_text)
# song menu box___________________________________________________________________________________
song_box = tk.Listbox(root, bg="white", fg="black", bd=3, font=(
    font_choosing, 13), selectbackground="gray", selectforeground="white", width=80)
song_box.pack(pady=5, padx=5)
# importing images________________________________________________________________________________
pause_btn_img = tk.PhotoImage(
    file=(f"{cur_di}/puase.png"))
back_btn_img = tk.PhotoImage(
    file=(f"{cur_di}/back.png"))
next_btn_img = tk.PhotoImage(
    file=(f"{cur_di}/next.png"))
stop_btn_img = tk.PhotoImage(
    file=(f"{cur_di}/stop.png"))
play_btn_img = tk.PhotoImage(
    file=(f"{cur_di}/play.png"))
volume_max_img = tk.PhotoImage(
    file=(f"{cur_di}/volume-max.png"))
volume_mid_img = tk.PhotoImage(
    file=(f"{cur_di}/volume-mid.png"))
volume_min_img = tk.PhotoImage(
    file=(f"{cur_di}/volume-min.png"))
mute_img = tk.PhotoImage(
    file=(f"{cur_di}/mute.png"))
con_img = tk.PhotoImage(
    file=(f"{cur_di}/continue.png"))
rand_img = tk.PhotoImage(
    file=(f"{cur_di}/random.png"))
# right click menu_________________________________________________________________________________
my_menu = tk.Menu(song_box, tearoff=False)
my_menu.add_command(label="Rename the song", command=lambda: rename())
song_box.bind("<Button-3>", popup)
# set control frame________________________________________________________________________________
control_frame = tk.Frame(root)
control_frame.pack()
back_btn = tk.Button(control_frame, image=back_btn_img,
                     borderwidth=0, command=lambda: back_song())
pause_btn = tk.Button(control_frame, image=play_btn_img,
                      borderwidth=0, command=lambda: pause())
next_btn = tk.Button(control_frame, image=next_btn_img,
                     borderwidth=0, command=lambda: next_song())
stop_btn = tk.Button(control_frame, image=stop_btn_img,
                     borderwidth=0, command=lambda: stop())
rand_btn = tk.Button(control_frame, bd=0, image=con_img,
                     command=lambda: randome_p())
back_btn.grid(row=0, column=0)
rand_btn.grid(row=0, column=1)
pause_btn.grid(row=0, column=2, padx=3)
stop_btn.grid(row=0, column=3, padx=3)
next_btn.grid(row=0, column=4)
# set menu_________________________________________________________________________________________
my_list = tk.Menu(root)
root.config(menu=my_list)
song_list = tk.Menu(my_list, tearoff=False)
my_list.add_cascade(label="Songs", menu=song_list)
song_list.add_command(label="Add song",
                      command=lambda: add_song_box())
remove_song_menu = tk.Menu(song_list, tearoff=False)
song_list.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(
    label="Delete a song from playlist", command=lambda: delete_song())
remove_song_menu.add_command(
    label="Delete all songs from playlist", command=lambda: delet_all_songs())
# set slider________________________________________________________________________________________
slider_frame = tk.Frame(root)
slider_frame.pack()
music_lenth = tk.Label(
    slider_frame, text="00:00 of 00:00", font=(font_choosing, 10))
my_slider = ttk.Scale(slider_frame, from_=0, to=100,
                      orient=tk.HORIZONTAL, value=0, length=450, command=lambda x: slide_click())
my_slider.grid(row=0)
music_lenth.grid(row=1)
# set volume frame__________________________________________________________________________________
volume_frame = tk.Frame(root)
volume_frame.pack(side="bottom")
volume_slider = ttk.Scale(volume_frame, from_=0,
                          orient=tk.HORIZONTAL, to=1, value=1, length=200)
volume_label = tk.Label(
    volume_frame, text=f"Volume: {int(volume_slider.get()*100)}%", font=(font_choosing, 10))
volume_img = tk.Button(volume_frame, image=volume_max_img,
                       borderwidth=0, command=lambda: mute())
volume_label.grid(row=0, column=0)
volume_img.grid(row=0, column=1, padx=5)
volume_slider.grid(row=0, column=2)
# set change color frame___________________________________________________________________________
change_color = tk.Frame(root).pack(pady=5)
change_color_line = tk.Label(change_color, text="_"*101).pack()
change_color_lable = tk.Label(
    change_color, text="Change the color of selected music", font=(font_choosing, 12))
change_color_lable.pack()
colors = ["red", "yellow", "pink", "gray",
          "lightblue", "lightgreen"]
change_combo_lable = tk.Label(
    change_color, text="Choose The Color:", font=(font_choosing, 10))
change_combo_lable.pack(side="left", padx=15)
change_color_combo = ttk.Combobox(
    change_color, textvariable=colors, font=(font_choosing, 10), values=colors)
change_color_combo.pack(side="left", padx=15)
change_color_btn = tk.Button(change_color, text="Change Color", font=(
    font_choosing, 10), command=lambda: change())
change_color_btn.pack(side="left", padx=15)
change_color_remove = tk.Button(change_color, text="Remove Color", font=(
    font_choosing, 10), command=lambda: remove_color())
change_color_remove.pack(side="left", padx=15)
# help menu____________________________________________________________________________________________
setting = tk.Menu(root, tearoff=False)
albums = tk.Menu(root, tearoff=False)
my_list.add_cascade(label="Albums", menu=albums)
my_list.add_cascade(label="Help", menu=setting)
albums.add_command(label="By Colors", command=lambda: album_show())
albums.add_command(label="Add Song", command=lambda: choose_color())
setting.add_command(label="Settings", command=lambda: setting_menu())
setting.add_command(label="Guide", command=lambda: guide())
setting.add_command(label="About", command=lambda: about_app())
# mainloop and function calling__________________________________________________________________________________________
query_di()
query()
search_bar.bind("<KeyRelease>", check)
root.mainloop()