import matplotlib
matplotlib.use('TkAgg')


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

def fcfs(requests, head):
    order = [head] + requests
    seek_times = [abs(order[i] - order[i - 1]) for i in range(1, len(order))]
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def sstf(requests, head):
    order = [head]
    remaining = requests.copy()
    seek_times = []
    
    while remaining:
        closest = min(remaining, key=lambda x: abs(x - order[-1]))
        seek_times.append(abs(closest - order[-1]))
        order.append(closest)
        remaining.remove(closest)
    
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def scan(requests, head, disk_size):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    order = [head] + right + [disk_size] + left[::-1]
    seek_times = [abs(order[i] - order[i - 1]) for i in range(1, len(order))]
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def c_scan(requests, head, disk_size):
    right = sorted([r for r in requests if r >= head])
    left = sorted([r for r in requests if r < head])
    order = [head] + right + [disk_size] + [0] + left
    seek_times = [abs(order[i] - order[i - 1]) for i in range(1, len(order))]
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def look(requests, head):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    order = [head] + right + left[::-1]
    seek_times = [abs(order[i] - order[i - 1]) for i in range(1, len(order))]
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def c_look(requests, head):
    right = sorted([r for r in requests if r >= head])
    left = sorted([r for r in requests if r < head])
    order = [head] + right + left
    seek_times = [abs(order[i] - order[i - 1]) for i in range(1, len(order))]
    total_seek_time = sum(seek_times)
    avg_seek_time = total_seek_time / len(seek_times)
    return order, total_seek_time, avg_seek_time, seek_times

def run_simulation():
    refresh()
    
    requests = list(map(int, entry_requests.get().split(',')))
    head = int(entry_head.get())
    disk_size = int(entry_disk_size.get())
    algorithm = algo_var.get()
    
    if algorithm == "FCFS":
        order, total_seek_time, avg_seek_time, seek_times = fcfs(requests, head)
    elif algorithm == "SSTF":
        order, total_seek_time, avg_seek_time, seek_times = sstf(requests, head)
    elif algorithm == "SCAN":
        order, total_seek_time, avg_seek_time, seek_times = scan(requests, head, disk_size)
    elif algorithm == "C-SCAN":
        order, total_seek_time, avg_seek_time, seek_times = c_scan(requests, head, disk_size)
    elif algorithm == "LOOK":
        order, total_seek_time, avg_seek_time, seek_times = look(requests, head)
    elif algorithm == "C-LOOK":
        order, total_seek_time, avg_seek_time, seek_times = c_look(requests, head)

    label_result.config(text=f"Total Seek Time: {total_seek_time}\nAverage Seek Time: {avg_seek_time:.2f}")
    animate_graph(order)
    display_table(order, seek_times)

def refresh():
    for widget in frame_graph.winfo_children():
        widget.destroy()
    for widget in frame_table.winfo_children():
        widget.destroy()
    label_result.config(text="")

def display_table(order, seek_times):
    tree = ttk.Treeview(frame_table, columns=("Next Track", "Tracks Traversed"), show='headings')
    tree.heading("Next Track", text="Next Track")
    tree.heading("Tracks Traversed", text="Tracks Traversed")
    
    for i in range(1, len(order)):
        tree.insert("", "end", values=(order[i], seek_times[i-1]))
    
    tree.pack()

def animate_graph(order):
    fig, ax = plt.subplots()
    ax.set_title("Disk Scheduling Visualization")
    ax.set_xlabel("Track Number")
    ax.set_ylabel("Request Order")
    ax.set_xlim(-1, max(order) + 1)
    ax.set_ylim(-1, len(order))
    ax.grid()

    line, = ax.plot([], [], marker='o', linestyle='-', color='b')
    current_index = [0]  # To hold the current frame index as a mutable object

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        if current_index[0] < len(order):
            x = order[:current_index[0] + 1]
            y = range(current_index[0] + 1)
            line.set_data(x, y)
            current_index[0] += 1
        return line,

    ani = FuncAnimation(fig, update, frames=len(order), init_func=init, blit=True, interval=1000)

    # Keep the final graph displayed
    def keep_final_graph():
        x = order
        y = range(len(order))
        line.set_data(x, y)
        canvas.draw()

    ani.event_source.stop()  # Stop the animation after it completes
    ani.event_source.add_callback(keep_final_graph)  # Keep the final graph

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("1000x600")
root.configure(bg='#add8e6')

frame_input = tk.Frame(root, bg='#add8e6')
frame_input.pack(pady=20)

tk.Label(frame_input, text="Requests (comma-separated):", bg='#add8e6').grid(row=0, column=0)
entry_requests = tk.Entry(frame_input)
entry_requests.grid(row=0, column=1)

tk.Label(frame_input, text="Head Position:", bg='#add8e6').grid(row=1, column=0)
entry_head = tk.Entry(frame_input)
entry_head.grid(row=1, column=1)

tk.Label(frame_input, text="Disk Size:", bg='#add8e6').grid(row=2, column=0)
entry_disk_size = tk.Entry(frame_input)
entry_disk_size.grid(row=2, column=1)

algo_var = tk.StringVar(value="FCFS")
ttk.Combobox(frame_input, textvariable=algo_var, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]).grid(row=3, columnspan=2)

tk.Button(frame_input, text="Run", command=run_simulation).grid(row=4, column=0)
tk.Button(frame_input, text="Refresh", command=refresh).grid(row=4, column=1)

frame_graph = tk.Frame(root, bg='#add8e6')
frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_table = tk.Frame(root, bg='#add8e6')
frame_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

label_result = tk.Label(root, text="", bg='#add8e6')
label_result.pack()

root.mainloop()