import base64
import logging
from datetime import datetime

def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def decode_base64_to_file(base64_string, output_path):
    with open(output_path, 'wb') as file:
        file.write(base64.b64decode(base64_string))

def log_message(tree, message, file_path=""):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row_id = tree.insert("", "end", values=(time, message, file_path))
    item = tree.item(row_id)
    tags = []

    if "Started Monitoring Directories" in message:
        tags.append("started_monitoring")
    elif "Monitoring active" in message:
        tags.append("monitoring_active")
    elif "Starting backup" in message:
        tags.append("starting_backup")
    elif "Stopped Monitoring Directories" in message:
        tags.append("stopped_monitoring")
    elif "Settings saved" in message:
        tags.append("settings_saved")
    elif "Backup Completed!" in message:
        tags.append("backup_completed")
    elif "Deleted old backup:" in message:
        tags.append("deleted_old_file")
    elif "Error" in message:
        tags.append("error")

    tree.tag_configure("started_monitoring", background="lightblue")
    tree.tag_configure("monitoring_active", foreground="green")
    tree.tag_configure("starting_backup", background="cyan")
    tree.tag_configure("stopped_monitoring", background="lightcoral")
    tree.tag_configure("settings_saved", background="goldenrod", foreground="purple")
    tree.tag_configure("backup_completed", background="lightgreen")
    tree.tag_configure("deleted_old_file", foreground="red")
    tree.tag_configure("error", background="red", foreground="white")

    tree.item(row_id, tags=tags)
    tree.see(row_id)
