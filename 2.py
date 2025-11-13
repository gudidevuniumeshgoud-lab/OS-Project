import tkinter as tk
from tkinter import messagebox, Entry, Button, Label, Frame
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------------------------------------
# ✅ INPUT PARSER
# -----------------------------------------------------------
def parse_inputs(total_memory_entry, num_processes_entry, process_sizes_entry, page_size_entry, segment_sizes_entry):
    try:
        total_memory = int(total_memory_entry.get())
        num_processes = int(num_processes_entry.get())
        process_sizes = [int(x.strip()) for x in process_sizes_entry.get().split(',')]

        if len(process_sizes) != num_processes:
            raise ValueError("Process count does not match given process sizes.")

        page_size = int(page_size_entry.get())

        segment_sizes_list = segment_sizes_entry.get().split(";")
        segment_sizes = []
        for seg in segment_sizes_list:
            if seg.strip():
                segment_sizes.append([int(x.strip()) for x in seg.split(",")])

        return total_memory, num_processes, process_sizes, page_size, segment_sizes

    except Exception as e:
        messagebox.showerror("Input Error", str(e))
        return None


# -----------------------------------------------------------
# ✅ COMBINED VISUALIZATION (Paging + Segmentation)
# -----------------------------------------------------------
def visualize_combined(total_memory, num_processes, process_sizes, page_size, segment_sizes):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6))
    fig.suptitle("Memory Allocation: Paging vs Segmentation", fontsize=14, fontweight="bold")

    # ---- Paging Visualization ----
    frames = total_memory // page_size
    memory = np.zeros(frames, dtype=int)
    frame_idx = 0

    for pid in range(num_processes):
        pages = (process_sizes[pid] + page_size - 1) // page_size
        for p in range(pages):
            if frame_idx < frames:
                memory[frame_idx] = pid + 1
                frame_idx += 1
            else:
                break

    ax1.set_title("Paging (Fixed-size Blocks)")
    ax1.set_xlabel("Frame Index")
    for i in range(frames):
        ax1.add_patch(
            plt.Rectangle((i, 0), 1, 1, edgecolor="black",
                          facecolor=f"C{memory[i]}" if memory[i] != 0 else "white")
        )
        text = f"P{memory[i]}" if memory[i] != 0 else "FREE"
        ax1.text(i + 0.25, 0.38, text, fontsize=8)
    ax1.set_xlim(0, frames)
    ax1.set_ylim(0, 1)

    # ---- Segmentation Visualization ----
    ax2.set_title("Segmentation (Variable-sized Blocks)")
    ax2.set_xlabel("Memory Address Space (Base → Limit)")
    current_address = 0

    for pid in range(len(segment_sizes)):
        for seg_idx, seg_size in enumerate(segment_sizes[pid]):
            if current_address + seg_size > total_memory:
                break
            ax2.add_patch(
                plt.Rectangle((current_address, 0), seg_size, 1, edgecolor="black", facecolor=f"C{pid}")
            )
            ax2.text(current_address + seg_size / 4, 0.35, f"P{pid+1}:S{seg_idx+1}", fontsize=8)
            current_address += seg_size

    if current_address < total_memory:
        free_space = total_memory - current_address
        ax2.add_patch(
            plt.Rectangle((current_address, 0), free_space, 1, edgecolor="black", facecolor="white")
        )
        ax2.text(current_address + free_space / 3.5, 0.35, "FREE", fontsize=8)

    ax2.set_xlim(0, total_memory)
    ax2.set_ylim(0, 1)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# -----------------------------------------------------------
# ✅ SIMULATION PAGE
# -----------------------------------------------------------
def open_simulation_page(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Memory Allocation Visualizer")
    root.geometry("520x640")
    root.configure(bg="#121212")

    def add_label(parent, text):
        return Label(parent, text=text, font=("Segoe UI", 10, "bold"), bg="#1E1E1E", fg="#00BFFF")

    Label(root, text="MEMORY ALLOCATION VISUALIZER", font=("Segoe UI", 17, "bold"),
          fg="#00BFFF", bg="#121212").pack(pady=15)

    container = Frame(root, bg="#1E1E1E", padx=25, pady=25, relief="ridge", bd=2)
    container.pack(padx=20, pady=10)

    add_label(container, "Total Memory Size (bytes)").pack(anchor="w")
    total_memory_entry = Entry(container, width=40, font=("Segoe UI", 10)); total_memory_entry.pack(pady=5)

    add_label(container, "Number of Processes (Paging)").pack(anchor="w")
    num_processes_entry = Entry(container, width=40, font=("Segoe UI", 10)); num_processes_entry.pack(pady=5)

    add_label(container, "Process Sizes (e.g., 300,200,150)").pack(anchor="w")
    process_sizes_entry = Entry(container, width=40, font=("Segoe UI", 10)); process_sizes_entry.pack(pady=5)

    add_label(container, "Page / Frame Size").pack(anchor="w")
    page_size_entry = Entry(container, width=40, font=("Segoe UI", 10)); page_size_entry.pack(pady=5)

    add_label(container, "Segmentation (e.g., 100,200;150;300,80)").pack(anchor="w")
    segment_sizes_entry = Entry(container, width=40, font=("Segoe UI", 10)); segment_sizes_entry.pack(pady=5)

    # ---- Simulation Function ----
    def start_simulation():
        inputs = parse_inputs(total_memory_entry, num_processes_entry, process_sizes_entry, page_size_entry, segment_sizes_entry)
        if inputs:
            total_memory, num_processes, process_sizes, page_size, segment_sizes = inputs
            visualize_combined(total_memory, num_processes, process_sizes, page_size, segment_sizes)

    # Buttons
    btn_frame = Frame(root, bg="#121212")
    btn_frame.pack(pady=20)

    start_btn = Button(btn_frame, text="🚀 RUN SIMULATION", font=("Segoe UI", 11, "bold"),
                       bg="#00BFFF", fg="black", width=18, command=start_simulation)
    start_btn.grid(row=0, column=0, padx=10)

    back_btn = Button(btn_frame, text="⬅ BACK", font=("Segoe UI", 11, "bold"),
                      bg="#FF6F61", fg="white", width=10, command=lambda: main_page(root))
    back_btn.grid(row=0, column=1, padx=10)


# -----------------------------------------------------------
# ✅ FIRST PAGE (Intro)
# -----------------------------------------------------------
def main_page(root=None):
    if root is None:
        root = tk.Tk()
    else:
        for widget in root.winfo_children():
            widget.destroy()

    root.title("Memory Allocation Visualizer")
    root.geometry("550x620")
    root.configure(bg="#121212")

    Label(root, text="MEMORY ALLOCATION VISUALIZER", font=("Segoe UI", 18, "bold"),
          fg="#00BFFF", bg="#121212").pack(pady=20)

    intro_frame = Frame(root, bg="#1E1E1E", padx=25, pady=25, relief="ridge", bd=2)
    intro_frame.pack(padx=20, pady=10)

    Label(intro_frame, text="📘 Paging:", font=("Segoe UI", 12, "bold"),
          fg="#00BFFF", bg="#1E1E1E").pack(anchor="w")
    Label(intro_frame, text="Paging divides memory into fixed-size blocks (pages & frames) to reduce external fragmentation.",
          wraplength=460, justify="left", fg="white", bg="#1E1E1E", font=("Segoe UI", 10)).pack(anchor="w", pady=5)

    Label(intro_frame, text="\n📗 Segmentation:", font=("Segoe UI", 12, "bold"),
          fg="#00BFFF", bg="#1E1E1E").pack(anchor="w")
    Label(intro_frame, text="Segmentation divides memory into variable-sized segments like code, stack, and data.",
          wraplength=460, justify="left", fg="white", bg="#1E1E1E", font=("Segoe UI", 10)).pack(anchor="w", pady=5)

    Label(intro_frame, text="\n🎯 Objective:", font=("Segoe UI", 12, "bold"),
          fg="#00BFFF", bg="#1E1E1E").pack(anchor="w")
    Label(intro_frame, text="This project visually compares Paging and Segmentation together — to understand how OS memory allocation differs between fixed and variable block systems.",
          wraplength=460, justify="left", fg="white", bg="#1E1E1E", font=("Segoe UI", 10)).pack(anchor="w", pady=5)

    next_btn = Button(root, text="NEXT ➜", font=("Segoe UI", 12, "bold"),
                      bg="#00BFFF", fg="black", width=15, command=lambda: open_simulation_page(root))
    next_btn.pack(pady=30)

    root.mainloop()


if __name__ == "__main__":
    main_page()
