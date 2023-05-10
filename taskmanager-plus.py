import tkinter as tk
import psutil

def get_running_processes():
    """Retrieve a list of running processes"""
    processes = []
    for process in psutil.process_iter(['pid', 'name']):
        processes.append((process.info['pid'], process.info['name']))
    return processes

def kill_process(pid):
    """Terminate a process given its PID"""
    try:
        process = psutil.Process(pid)
        process.terminate()
        return True
    except psutil.NoSuchProcess:
        return False

def on_close_process():
    """Handle the force-close button click event"""
    selected_process = process_listbox.get(tk.ACTIVE)
    if selected_process:
        pid = int(selected_process.split(":")[0])
        if kill_process(pid):
            status_label.config(text="Process terminated successfully.", fg="green")
        else:
            status_label.config(text="Failed to terminate process.", fg="red")

def on_search():
    """Handle the search button click event"""
    search_text = search_entry.get().lower()
    process_listbox.delete(0, tk.END)
    for pid, name in processes:
        if search_text in name.lower():
            process_listbox.insert(tk.END, f"{pid}: {name}")

window = tk.Tk()
window.title("Task Manager+")
window.geometry("400x400")
search_frame = tk.Frame(window)
search_frame.pack(pady=10)
search_label = tk.Label(search_frame, text="Search:")
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=on_search)
search_button.pack(side=tk.LEFT)
process_listbox = tk.Listbox(window, selectbackground="gray", selectforeground="white")
process_listbox.pack(fill=tk.BOTH, expand=True)
processes = get_running_processes()
for pid, name in processes:
    process_listbox.insert(tk.END, f"{pid}: {name}")
close_button = tk.Button(window, text="Force Close", command=on_close_process)
close_button.pack(pady=10)
status_label = tk.Label(window, text="", fg="black")
status_label.pack()
window.mainloop()
