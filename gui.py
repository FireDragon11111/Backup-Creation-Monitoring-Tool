import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import Calendar
from functions import (run_backup, start_monitoring, stop_monitoring, monitor_directories, monitoring_states, monitoring_threads, start_backup_for_profile)
from config import load_config, save_config, CONFIG_FILE
from utils import log_message, decode_base64_to_file
import base64
import datetime

icon_base64 = 'AAABAAEAAAAAAAEAIABMEQAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAEAAAABAAgGAAAAXHKoZgAAAAlwSFlzAAALEwAACxMBAJqcGAAAEP5JREFUeJztnWnMXVUVhpcCtmVoI1QotaBViwYpEZRI0Bj/owwi0Coa58gPNBCcYhBQgxEZokagLUiZZRCiosYfICTQMkgAIZgokQQQbCsO0EIHRPfKuTeUy/ed79x71tprn/O+T/L8IaTf2uusve/a55y7rwhBYW5yeXJV8p7k+uTWgesH/21lcllyt6AYCSHG7Je8JLkp+b+G6v97cXJJQLyEEAPmJM9JbpPmE39U7Q7OTs7OHDshpAX6yf2QTD7xR12bXJB1BISQiThIqj291eQf+kRyacZxEELGRD/5PSb/0MeFnQAhRaL79AfEb/IPXZOclWlMhJCG6A0/78k/9MxMYyKENEAf9bW52z+uzwm3AoQUgz7nzzX5h16QZWSEkFr0Db9xXvKxcqPwjUFCwtHXe3NP/qHHZxgfIaQGfbc/agFYkWF8hJAa9Es8UQvA2gzjI4TUsEHiFoB1GcZHCKlhi8QtAJszjI8QUkPU5B9KCAmECwAhwHABIAQYLgCEAMMFgBBguAAQAgwXAEKA4QJACDBcAAgBhgsAIcBwASAEGC4AhADDBYAQYLgAEAIMFwBCgOECQEgD3pj8dPLK5H1S/YTWS+I/QfTUnBuSZySXJQ9OLk6+PrmTwbi6vgBoDjQXmhPNjR5yqj88ojnz/JmzoS8N/o7WxBVS1chCg3GRQjg0eV3yRck3Ke5Nnpw8IPka5/F1fQGoQ3OnP0h6ilQTNNeYtFa0Zg51Hh9xZE+pLmKuonk2eW5y/xyD244+LwCjvDN5nlS/TJRrfNdKVUukQxySfFLyFMg/k6cnd88ysleDtAAM2UOqbcK/GsbYVv1p9PdkGRlpzful+jT2LgrdO/40+YY8w5oWxAVgyF7JyyTPvZz/JA/LMywyKUuSz4h/MTwq1UJTAsgLwJAPJP8q/mP9R/JtmcZExmTH5B/EvwhukuqudSlwAajQ30jU/br3eO9Pvi7TmMgYnCa+F17bzFOzjaY5XABeRp8afF38twTfzDUg0gzdh3vu+7clP5NtNOPBBeDVnJDcKn5j1qcQe2UbDZmRH4jfxdZC+nC+oYwNF4CpOUKqhdtr3N/PNxRSxxypbs54XGRtJT+VbSSTwQVgej4uftsBrbnZ+YZCpkNfHfUq7hL3/KNwAahH7wl4jf34jOMg0+B15/f6nINoAReAevTG4I3iM/ZrMo6DTIE+jvm32F9Yfc4/L+M42sAFYGb0se1jYj92rT0+EgzkcLG/qLpnLOUlnyZwAWjGB8XnfsDhGcdARlgt9hf0kpwDMIALQHP0677W41+dcwDkZbT1sv4yiH6xx+vd/h2k6iz08dFtyT8lNw78S/KO5EqpzgzYZYx/tysLwK5S3bBdNRjro9uNX3Nxm1S50RztMMa/Ow767N56y6g1yG1AAB7t/+kOce4m1VuK4xxuoS+a/FCqQ0xmovQFYFHyx1JN9Kb/5oZBznZr8O+Py3fHiKOp3AYEsFpsL6K+SWj5lV69+/wlqYp50ph0IThZ6g8VKXUB0Jj1II9xJv5UC8FJM4x/XOaL/XkCqw3jIw3waP/PNYxPnyDcZBjbzTL9p2GJC4B+Mec3hn/jJrF9KnO+YWwqtwGZ8Wj/rU7y2Sf5Z4f49JuO86f4e6UtAPPF51uZmtPFU/y9SVjqEB+3ARlZLbYX716juPR588PGsW3vg/LqRaCkBWD+IEavv/VYcu9pcj8u9xvHdplRXGQGPNr/k43iut04riaLQCkLgPfkH7pGbE5T/opxXNwGZEK/mWddVAcYxPVth7im85HkgsHfLWEB0EenOSb/0G/NeDVm5l0OcX3IIC4yA9pqWV40Pbe/7V3mNye3GMc1k8NOIHoByPXJv72bk/s2uTA1vFbaPaGZSm4DnJkl9u3/DQZxrTCOaZxFIHoBiIrhwkZXph7rLwlpbc4yiItMg0f7f0bLmPQNtxynENNXqs/y274o9B2HuLgNcORysb9gy1vGtMwhJtrMYxpcnzpOcIiJ2wAnPNp/9d0t41rpEBNt5kUNrk8dhzjEpN814DbAAY/2X31Ty7judoqLzuyaBtenjsVOcZV8hmRnsb77P3SPlnHl+AVbOrXrGlyfOryeolzeMi4ygrZUHif/qG1f3sj9+I++7OYG16eOWU5x6c+I8cBQQ/SIZ68i2rFlbDl/qZa+0i0Nrk8dOznGxm2AIR53/4fObRnbo46x0XrXN7g+dcxzjI3bACM82391Ycv47nCMjdZ7d4PrU8cix9j4NMAIr7v/Qw9pGd8q5/jo9K5ocH3qeK9zfNwGGODZ/qttXybx/GESWm/bH+Y41jm+K1rGB493+6+e1jJGfRW4zbFXdDI3DnLfhtOdY+Q2oCWed/+H3mgQ508yxElf6Y8aXZl6fpEhziMM4oTFu/1Xn5L2XwfWY8DYBeRTH702OTG5Dr3mT2eIlduACcnR/g9dahDvKZlipSJfbnhN6jgwU6x8KWhCcrT/Q79qEK9+olyVMWZUrxCbY8I9fzV4VG4DJuBKyXeB7jeKWVf6NRnjRlMPb53T+GrU88eMcXMbMCba/mvrlLO4DjSKPeKILASnOhF5UjzOA6yT24AxOVLyF9gqw/j1eHCPs/FRtZz8yqUBYzjSMP7e4/ErrjP5glQ/HmkFOwEbrSe//q7A5oBxXGk4hl6T8+7/qBbPlreHnUA7rSe/EvXOhp4baXX/otfkvPs/qn699K3G42EnMJkek39JcmvgmLgNaEDOu/9TeYvY/hqtwk5gPD0mv/K74HFxGzADeqc0993/qfyEw9hy/3pOV31wkCtrPlnA2Pg0YAaOkviLpH7RaXzsBOr1+uRXTixgfOpRTuPrBSW8Sfdick/HMXIRmFrPya9oV7GtgHFe5TjGTlNK+3+L90CFi8Co3pN/yK1B49tePg2Yhr63/6NwEajMNfkVbgMKBqH9HwV9Ecg5+RVuAwoFqf0fBXURyD35h5SwDdDzDLgN2A609n8UtEUgavIr3AYUCGL7PwrKewKPJBcY5WwSuA0oDOT2f5S+LwLRk38ItwEFcbTEXww1qv0fpa+LQCmTXyllG3C090C7wNUSfyGi2/9R+rYIlDT5lVK2AVd7D7R02P5PT18WgdIm/xBuAwqA7X89XV8ESp38CrcBBVBK+295EpA1XV0ESp78CrcBwbD9b07XFoHSJ/8QbgMCYfs/Hl1ZBLoy+ZVStgEf8R5oibD9Hx9dBHKeZ9/nya+Usg24xnugpcH2f3JKXQS6NvmHlLAN0N+V3MV7oCWhLU900tWutP+jlLYIdHXyK9wGBKAtT3TCu9b+j1LKItDlya9wG5AZtv92RC8CXZ/8Q0rYBmwSkG0A239bohaBvkx+pZRtwDHeAy0Btv/25F4E+jT5lVK2AT/zHmg02v7roYjRie5D+z9KrkWgb5N/CLcBGSil/T/Re6BBeC8CXj/aUQLcBmRAW5zoBPet/R9Fjxe7Q+zzdldyj4zjyA23Ac7o+8763nN0gm/1HmgBaBv5W7HL2c8F4331ErYBOkd29h5oBGz/87JD8gxp92u4Wownif2PpZYKtwGO8O5/DPtL9QmuY2+aJ70ZdUFyUUC8kWhtjJMnL3u3DWD7H88+Un3CaXHpzbxnkluSLyT/nrw3eXHyY8l5QTGWQAnbAP1uQK+2AdrSRCdV7cvLP8SPUrYBH/UeaE549590hVKeBlzrPdBcaCtTQvvfx5d/iA8lbAN681KQtjLRyVTZ/pOmcBtgiLYy0Ylk+0/GgdsAI9j+k67CbYABbP9JVyllG3Cs90A9YftPukop24DrvAfqBdt/0nW4DWgB23/SdbgNaAHbf9J1uA2YEG3/9X3m6MSx/Sdt4TZgArRliU6ayvaftKWUbcBx3gO1RFuW6ISx/ScWlLINuN57oFaw/Sd9o5RtwK7eA7WA7T/pG9wGjMENEp8oSvuonuxUNHOTz0t8oijto3qC0+5SMJ+T+CRR2mc/KwXze4lPEKV9tthzLRdKGSeqUtpn/yuFntZ8qsQnh1IEda4Vx1qJTwylCN4phaFv3GlrEp0YShHUuVbULzR/QeKTQimSn5eC+LXEJ4RSJG+WQpglfPmH0tzqnNO5F877JD4ZlCJ6mBTANyQ+EZQi+jUpgF9JfCIoRfSXUgCPSHwiKEX0YSmAZyU+EZQiqnMvnOgkUIpsONEJoBTZcKITQCmy4UQngFJkw4lOAKXIhhOdAEqRDSc6AZQiG050AihFNpzoBFCKbDjRCaAU2XCiE0ApsuFEJ4BSZMOJTgClyIYTnQBKkQ0nOgGUIhtOdAIoRTYc+AQQaODrHz4BBBr4+odPAIEGvv7hE0Cgga9/+AQQaODrHz4BBBr4+odPAIEGvv7hE0Cgga9/+AQQaODrHz4BBBr4+odPAIEGvv7hE0Cgga9/+AQQaODrHz4BBBr4+odPAIEGvv7hE0Cgga9/+ASQLMxNLk+uSt6TXJ/cOnD94L+tTC5L7pYxLvj6h08AcWW/5CXJTdK8JvT/vTi5JEN88PUPnwDiwpzkOcltMnltaHdwdnK2Y5zw9Q+fAGKOfnI/JHY1sja5wClW+PqHTwAx5SCp9vTWdfJEcqlDvPD1D58AYoZ+8ntM/qGPi30nAF//8AkgJug+/QHxr5c1yVmGccPXP3wCiAl6wy9XzZxpGDd8/cMngLRGH/W1uds/rs+J3VYAvv7hE0Bao8/5c9fNBUaxw9c/fAJIK/QNv3Fe8rFyo9i8MQhf//AJIK3Q13ujaud4g/jh6x8+AaQV+m5/VO2sMIgfvv7hE0BaoV/iiaqdtQbxw9c/fAJIKzZIXO2sM4gfvv7hE0BasUXiamezQfzw9Q+fANIKLgAdr3/4BJBWcAvQ8fqHTwBpBW8Cdrz+4RNAWqHHeEXVzkUG8cPXP3wCSCv0DL+o2jnWIH74+odPAGnFrlJ9OSd33Wwc/O22wNc/fAJIa/QAz9x1Y/EWoATEXVz9wyeAtEZPAtIDPHPVjD56fItR7PD1D58AYoKe3purZs4yjBu+/uETQEzQI8H0sZx3vdwpPBLMFPgEEDP0lB49uNOrVv6WXGgcM3z9wyeAmKJHd+sR3tZ1ogvLAQ7xwtc/fAKIOfOTt4tdjehJwPxhECfgE0Bc0H26nt6rz+snrQ2923+W2O75R4Gvf/gEEFf0k1sP8BxnIdD/V5/zL84QH3z9wyeAZEHf2tMz/PT9/buk+ibfloHrBv/twuRxYvOGX1Pg6x8+AQQa+PqHTwCBBr7+4RNAoIGvf/gEEGjg6x8+AQQa+PqHTwCBBr7+4RNAoIGvf/gEEGjg6x8+AQQa+PqHTwCBBr7+4RNAoIGvf/gEEGjg6x8+AQQa+PqHTwCBBr7+4RNAoIGvf/gEEGjg6z86AZQiG050AihFNpzoBFCKbDjRCaAU2XCiE0ApsuFEJ4BSZMOJTgClyIYTnQBKkQ0nOgGUIhtOdAIoRTac6ARQimw40QmgFNlwohNAKbLhRCeAUmTDiU4ApciGE50ASpENZ4vEJ4FSRHXuhbNB4hNBKaLrpQDukfhEUIroXVIAKyU+EZQiukIKYLnEJ4JSRJdJAcxNbpL4ZFCK5PPJeVIIF0l8QihFUudcMewt7AIozaV++i+SwviexCeGUgTPkgKZnbxb4pNDaZ+9L7mzFIpuBZ6U+CRR2keflgJb/1EOTj4l8cmitE/qnNK51QkWCt8QpNTKB5L7SsfQfcr5yW0Sn0BKu6jOnfOk4D1/E96RvFSqRxfRCaW0C+pcuTT5dukR+taSvjas3x3QpwX6TSZ+lZiiq3NA54LOCZ0bOkf07dos/B88K5K9iTNC4AAAAABJRU5ErkJggg=='

def settings_saved_before():
    return os.path.exists("settings_saved.flag")

def mark_settings_as_saved():
    with open("settings_saved.flag", "w") as f:
        f.write("Settings have been saved.")

def select_directory(var):
    directory = filedialog.askdirectory()
    if directory:
        var.set(directory)

def add_subdirectory(parent_dir, sub_dirs_listbox):
    directory = filedialog.askdirectory(initialdir=parent_dir.get())
    if directory:
        sub_dir_name = os.path.relpath(directory, parent_dir.get())
        sub_dirs_listbox.insert(tk.END, sub_dir_name)

def remove_subdirectory(sub_dirs_listbox):
    selected = sub_dirs_listbox.curselection()
    for index in reversed(selected):
        sub_dirs_listbox.delete(index)

def save_current_state(source_dir, dest_dir, sub_dirs_listbox, backup_frequency, backup_time, backup_day_of_week, calendar, zip_files_kept, interval_days, interval_hours, interval_minutes, interval_seconds, current_profile, tree):
    sub_dirs_list = [sub_dirs_listbox.get(i) for i in range(sub_dirs_listbox.size())]
    selected_date = calendar.get_date()
    
    if selected_date:
        day_of_month = int(selected_date.split('/')[0])
    else:
        day_of_month = 1
    
    config = {
        'backup_frequency': backup_frequency.get(),
        'backup_time': backup_time.get(),
        'backup_day_of_week': backup_day_of_week.get(),
        'backup_day_of_month': day_of_month,
        'zip_files_kept': zip_files_kept.get(),
        'interval_days': interval_days.get(),
        'interval_hours': interval_hours.get(),
        'interval_minutes': interval_minutes.get(),
        'interval_seconds': interval_seconds.get(),
        'source_dir': source_dir.get(),
        'dest_dir': dest_dir.get(),
        'sub_dirs': sub_dirs_list,
        'monitoring_state': monitoring_states.get(current_profile.get(), False)
    }
    save_config(config, current_profile.get())
    log_message(tree, "Current state saved")

def center_window(app, width=1000, height=900):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.geometry(f'{width}x{height}+{x}+{y-30}')

def cleanup():
    icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.ico') if getattr(sys, 'frozen', False) else 'icon.ico'
    if os.path.exists(icon_path):
        os.remove(icon_path)

def create_gui():
    app = tk.Tk()
    app.title("Backup Creation & Monitoring Tool")
    center_window(app, width=975, height=925)
    
    icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.ico') if getattr(sys, 'frozen', False) else 'icon.ico'
    decode_base64_to_file(icon_base64, icon_path)
    app.iconbitmap(icon_path)
    
    def update_entry(*args):
        backup_time.delete(0, tk.END)
        backup_time.insert(0, f"{hours.get()}")

    def save_settings():
        sub_dirs_list = [sub_dirs_listbox.get(i) for i in range(sub_dirs_listbox.size())]
        config = {
            'backup_frequency': backup_frequency.get(),
            'backup_time': backup_time.get(),
            'backup_day_of_week': backup_day_of_week.get(),
            'backup_day_of_month': calendar.get_date(),
            'zip_files_kept': zip_files_kept.get(),
            'interval_days': interval_days.get(),
            'interval_hours': interval_hours.get(),
            'interval_minutes': interval_minutes.get(),
            'interval_seconds': interval_seconds.get(),
            'source_dir': source_dir.get(),
            'dest_dir': dest_dir.get(),
            'sub_dirs': sub_dirs_list,
            'monitoring_state': monitoring_states.get(current_profile.get(), False)
        }
        save_config(config, current_profile.get())
        log_message(tree, "Settings saved")
        
        start_button.config(state=tk.NORMAL)
        
        mark_settings_as_saved()

    source_dir = tk.StringVar()
    dest_dir = tk.StringVar()
    sub_dirs = tk.StringVar()

    current_profile = tk.StringVar(value="Profile 1")
    config = load_config(current_profile.get())

    columns = ("Time", "Message", "FilePath")
    tree = ttk.Treeview(app, columns=columns, show='headings')
    tree.heading("Time", text="Time")
    tree.heading("Message", text="Message")
    tree.heading("FilePath", text="File Path")
    tree.column("Time", width=125)
    tree.column("Message", width=250)
    tree.column("FilePath", width=600)

    tree.place(x=10, y=10, width=950, height=425)

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_columnconfigure(3, weight=1)

    label = tk.Label(app, text="Parent Directory:")
    label.place(x=10, y=450)
    source_dir_entry = tk.Entry(app, textvariable=source_dir, width=75)
    source_dir_entry.place(x=225, y=450)
    button = tk.Button(app, text="Browse", command=lambda: select_directory(source_dir))
    button.place(x=700, y=450)

    tk.Label(app, text="Subdirectories:").place(x=10, y=530)
    sub_dirs_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, width=75, height=5)
    sub_dirs_listbox.place(x=225, y=500)
    tk.Button(app, text="Add", command=lambda: add_subdirectory(source_dir, sub_dirs_listbox)).place(x=700, y=500)
    tk.Button(app, text="Remove", command=lambda: remove_subdirectory(sub_dirs_listbox)).place(x=700, y=535)

    tk.Label(app, text="Destination Directory:").place(x=10, y=600)
    dest_dir_entry = tk.Entry(app, textvariable=dest_dir, width=75)
    dest_dir_entry.place(x=225, y=600)
    tk.Button(app, text="Browse", command=lambda: select_directory(dest_dir)).place(x=700, y=600)

    tk.Label(app, text="Backup Frequency:").place(x=10, y=650)
    backup_frequency = tk.StringVar(value=config.get('backup_frequency', 'Daily'))
    backup_frequency_radiobuttons = [
        tk.Radiobutton(app, text="Daily", variable=backup_frequency, value="Daily", command=lambda: update_frequency_options()),
        tk.Radiobutton(app, text="Weekly", variable=backup_frequency, value="Weekly", command=lambda: update_frequency_options()),
        tk.Radiobutton(app, text="Monthly", variable=backup_frequency, value="Monthly", command=lambda: update_frequency_options())
    ]
    backup_frequency_radiobuttons[0].place(x=225, y=650)
    backup_frequency_radiobuttons[1].place(x=300, y=650)
    backup_frequency_radiobuttons[2].place(x=375, y=650)

    tk.Label(app, text="Backup Time (HH:mm):").place(x=10, y=700)
    backup_time = tk.Entry(app, width=10)
    backup_time.place(x=225, y=700)
    backup_time.insert(0, config.get('backup_time', ''))

    hour_options = [f"{i:02d}:00" for i in range(24)]
    hours = ttk.Combobox(app, values=hour_options, width=7)
    hours.place(x=310, y=700)
    hours.bind("<<ComboboxSelected>>", update_entry)

    backup_day_of_week = tk.StringVar(value=config.get('backup_day_of_week', ''))
    day_options = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_menu = ttk.Combobox(app, textvariable=backup_day_of_week, values=day_options)
    day_menu.place(x=700, y=650)
    day_menu.place_forget()

    backup_day_of_month = tk.StringVar(value=config.get('backup_day_of_month', ''))
    calendar_frame = tk.Frame(app)
    current_date = datetime.datetime.now()
    calendar = Calendar(calendar_frame, selectmode='day', date_pattern='dd/mm/yyyy')
    calendar.pack()
    calendar.selection_set(current_date)
    calendar_frame.place(x=700, y=650)
    calendar_frame.place_forget()

    tk.Label(app, text="# ZIP files kept before deletion:").place(x=10, y=750)
    zip_files_kept = tk.Entry(app, width=10)
    zip_files_kept.place(x=225, y=750)
    zip_files_kept.insert(0, config.get('zip_files_kept', ''))

    tk.Label(app, text="Interval Between Next Deletion Check:").place(x=10, y=800)
    interval_frame = tk.Frame(app)
    interval_frame.place(x=225, y=800)

    interval_days = tk.Entry(interval_frame, width=5)
    interval_days.grid(row=0, column=0, padx=(0, 5))
    tk.Label(interval_frame, text="Days").grid(row=0, column=1, padx=(0, 30))

    interval_hours = tk.Entry(interval_frame, width=5)
    interval_hours.grid(row=0, column=2, padx=(0, 5))
    tk.Label(interval_frame, text="Hours").grid(row=0, column=3, padx=(0, 30))

    interval_minutes = tk.Entry(interval_frame, width=5)
    interval_minutes.grid(row=0, column=4, padx=(0, 5))
    tk.Label(interval_frame, text="Minutes").grid(row=0, column=5, padx=(0, 30))

    interval_seconds = tk.Entry(interval_frame, width=5)
    interval_seconds.grid(row=0, column=6, padx=(0, 5))
    tk.Label(interval_frame, text="Seconds").grid(row=0, column=7, padx=(0, 30))

    interval_days.insert(0, config.get('interval_days', ''))
    interval_hours.insert(0, config.get('interval_hours', ''))
    interval_minutes.insert(0, config.get('interval_minutes', ''))
    interval_seconds.insert(0, config.get('interval_seconds', ''))

    save_settings_button = tk.Button(app, text="Save Settings", command=save_settings, width=13)
    save_settings_button.place(x=25, y=885)

    def toggle_input_widgets(state):
        state = tk.DISABLED if state else tk.NORMAL
        save_settings_button.config(state=state)
        source_dir_entry.config(state=state)
        dest_dir_entry.config(state=state)
        sub_dirs_listbox.config(state=state)
        backup_time.config(state=state)
        zip_files_kept.config(state=state)
        interval_days.config(state=state)
        interval_hours.config(state=state)
        interval_minutes.config(state=state)
        interval_seconds.config(state=state)
        for rb in backup_frequency_radiobuttons:
            rb.config(state=state)
        day_menu.config(state=state)
        calendar.config(state=state)

    def update_frequency_options():
        config_exists = os.path.exists(f"{CONFIG_FILE}_{current_profile.get()}.json")
        if backup_frequency.get() == "Weekly":
            day_menu.place(x=700, y=650)
            calendar_frame.place_forget()
        elif backup_frequency.get() == "Monthly":
            if not config_exists:
                current_date = datetime.datetime.now()
                calendar.selection_set(current_date)
                calendar.see(current_date)
            calendar_frame.place(x=700, y=650)
            day_menu.place_forget()
        else:
            day_menu.place_forget()
            calendar_frame.place_forget()

    def run_backup_and_log():
        sub_dirs_list = [sub_dirs_listbox.get(i) for i in range(sub_dirs_listbox.size())]
        start_backup_for_profile(current_profile.get(), source_dir.get(), dest_dir.get(), sub_dirs_list, tree)

    def load_profile(profile):
        toggle_input_widgets(False)

        backup_frequency.set('Daily')
        backup_time.delete(0, tk.END)
        hours.set('')
        backup_day_of_week.set('')
        calendar.selection_clear()
        zip_files_kept.delete(0, tk.END)
        interval_days.delete(0, tk.END)
        interval_hours.delete(0, tk.END)
        interval_minutes.delete(0, tk.END)
        interval_seconds.delete(0, tk.END)
        source_dir.set('')
        dest_dir.set('')
        sub_dirs_listbox.delete(0, tk.END)

        config_exists = os.path.exists(f"{CONFIG_FILE}_{profile}.json")
        if config_exists:
            config = load_config(profile)

            backup_frequency.set(config.get('backup_frequency', 'Daily'))
            backup_time_str = config.get('backup_time', '')
            backup_frequency_value = config.get('backup_frequency', 'Daily')

            if backup_frequency_value == 'Daily':
                backup_time.insert(0, backup_time_str)
                if backup_time_str:
                    backup_hour = backup_time_str.split(':')[0] + ":00"
                    hours.set(backup_hour)
            
            elif backup_frequency_value == 'Weekly':
                backup_day_of_week.set(config.get('backup_day_of_week', ''))
                backup_time.insert(0, backup_time_str)
                if backup_time_str:
                    backup_hour = backup_time_str.split(':')[0] + ":00"
                    hours.set(backup_hour)
            
            elif backup_frequency_value == 'Monthly':
                backup_day_of_month_value = config.get('backup_day_of_month', '01/01/2024')
                if isinstance(backup_day_of_month_value, str):
                    day_of_month_str = backup_day_of_month_value.split('/')[0]
                    if day_of_month_str:
                        day_of_month = int(day_of_month_str)
                    else:
                        day_of_month = 1
                else:
                    day_of_month = int(backup_day_of_month_value)

                current_date = datetime.datetime.now()
                valid_date = current_date.replace(day=day_of_month)
                calendar.selection_set(valid_date)

            zip_files_kept.insert(0, config.get('zip_files_kept', ''))
            interval_days.insert(0, config.get('interval_days', ''))
            interval_hours.insert(0, config.get('interval_hours', ''))
            interval_minutes.insert(0, config.get('interval_minutes', ''))
            interval_seconds.insert(0, config.get('interval_seconds', ''))
            source_dir.set(config.get('source_dir', ''))
            dest_dir.set(config.get('dest_dir', ''))
            for sub_dir in config.get('sub_dirs', []):
                sub_dirs_listbox.insert(tk.END, sub_dir)
            
            monitoring_states[profile] = config.get('monitoring_state', False)
        else:
            start_button.config(state=tk.DISABLED)

        update_button_states(profile, start_button, stop_button)
        update_frequency_options()

    def update_button_states(profile, start_button, stop_button):
        monitoring = monitoring_states.get(profile, False)
        config_exists = os.path.exists(f"{CONFIG_FILE}_{profile}.json")
        
        if monitoring:
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
        else:
            start_button.config(state=tk.NORMAL if config_exists else tk.DISABLED)
            stop_button.config(state=tk.DISABLED)
        
        for button in profile_buttons.values():
            button.config(state=tk.NORMAL)
        profile_buttons[profile].config(state=tk.DISABLED)
        toggle_input_widgets(monitoring)

    def initialize_state():
        profiles = ["Profile 1", "Profile 2", "Profile 3"]
        for profile in profiles:
            if os.path.exists(f"{CONFIG_FILE}_{profile}.json"):
                load_profile(profile)
                if monitoring_states.get(profile, False):
                    thread = threading.Thread(target=monitor_directories, args=(profile, tree), daemon=True)
                    monitoring_threads[profile] = thread
                    thread.start()
        current_profile.set("Profile 1")
        load_profile("Profile 1")
        update_button_states("Profile 1", start_button, stop_button)
        
        if not settings_saved_before():
            start_button.config(state=tk.DISABLED)

    start_button = tk.Button(app, text="Start Monitoring", command=lambda: start_monitoring(current_profile.get(), tree, update_button_states, start_button, stop_button, toggle_input_widgets))
    start_button.place(x=150, y=850)

    stop_button = tk.Button(app, text="Stop Monitoring", command=lambda: stop_monitoring(current_profile.get(), tree, update_button_states, start_button, stop_button, toggle_input_widgets))
    stop_button.place(x=255, y=850)

    tk.Button(app, text="Run Backup", command=run_backup_and_log, width=13).place(x=25, y=850)

    profile_frame = tk.Frame(app)
    profile_frame.place(x=700, y=850)

    profile_buttons = {
        "Profile 1": tk.Button(profile_frame, text="Profile 1", command=lambda: [current_profile.set("Profile 1"), load_profile("Profile 1")]),
        "Profile 2": tk.Button(profile_frame, text="Profile 2", command=lambda: [current_profile.set("Profile 2"), load_profile("Profile 2")]),
        "Profile 3": tk.Button(profile_frame, text="Profile 3", command=lambda: [current_profile.set("Profile 3"), load_profile("Profile 3")])
    }

    profile_buttons["Profile 1"].pack(side=tk.LEFT, padx=10)
    profile_buttons["Profile 2"].pack(side=tk.LEFT, padx=10)
    profile_buttons["Profile 3"].pack(side=tk.LEFT, padx=10)

    initialize_state()

    app.protocol("WM_DELETE_WINDOW", lambda: [
        save_current_state(source_dir, dest_dir, sub_dirs_listbox, backup_frequency, backup_time, backup_day_of_week, calendar, zip_files_kept, 
        interval_days, interval_hours, interval_minutes, interval_seconds, current_profile, tree), 
        app.destroy()
    ])

    app.mainloop()
