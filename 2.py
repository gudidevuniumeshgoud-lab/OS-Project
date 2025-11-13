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
# ✅ PAGING VISUALIZATION (With FREE blocks labeled)
# -----------------------------------------------------------
def visualize_paging(total_memory, num_processes, process_sizes, page_size):
    frames = total_memory // page_size
    memory = np.zeros(frames, dtype=int)

    fig, ax = plt.subplots(figsize=(11, 2.7))
    ax.set_title("Paging (Fixed-size memory blocks)")
    ax.set_xlabel("Frame Index")

    frame_idx = 0
    for pid in range(num_processes):
        pages = (process_sizes[pid] + page_size - 1) // page_size

        for p in range(pages):
            if frame_idx < frames:
                memory[frame_idx] = pid + 1
                frame_idx += 1
            else:
                messagebox.showwarning("Memory Full", "Not enough memory for paging")
                break

    for i in range(frames):
        ax.add_patch(
            plt.Rectangle((i, 0), 1, 1, edgecolor="black", facecolor=f"C{memory[i]}")
        )

        if memory[i] != 0:
            ax.text(i + 0.33, 0.38, f"P{memory[i]}", fontsize=8)
        else:
            ax.text(i + 0.25, 0.38, "FREE", fontsize=8)

    ax.set_xlim(0, frames)
    ax.set_ylim(0, 1)
    plt.show()


# -----------------------------------------------------------
# ✅ SEGMENTATION VISUALIZATION
# -----------------------------------------------------------
def visualize_segmentation(total_memory, num_processes, segment_sizes):
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.set_title("Segmentation (Variable-sized memory blocks)")
    ax.set_xlabel("Memory Address Space (Base → Limit)")

    current_address = 0
    segment_table = []

    for pid in range(len(segment_sizes)):
        for seg_idx, seg_size in enumerate(segment_sizes[pid]):

            if current_address + seg_size > total_memory:
                messagebox.showwarning("Memory Full",
                    f"Not enough memory to allocate segment {seg_idx+1} of process {pid+1}.")
                break

            ax.add_patch(
                plt.Rectangle((current_address, 0), seg_size, 1, edgecolor="black", facecolor=f"C{pid}")
            )
            ax.text(current_address + seg_size / 4, 0.35, f"P{pid+1}:S{seg_idx+1}", fontsize=8)

            segment_table.append((pid + 1, seg_idx + 1, current_address, seg_size))
            current_address += seg_size

    if current_address < total_memory:
        free_space = total_memory - current_address
        ax.add_patch(
            plt.Rectangle((current_address, 0), free_space, 1, edgecolor="black", facecolor="white")
        )
        ax.text(current_address + free_space / 3.5, 0.35, "FREE", fontsize=8)

    ax.set_xlim(0, total_memory)
    ax.set_ylim(0, 1)
    plt.show()

    print("\n----- SEGMENT TABLE (Base / Limit) -----")
    print("Process | Segment | Base | Limit")
    print("-------------------------------------")
    for row in segment_table:
        print(f"P{row[0]}      | S{row[1]}      | {row[2]}   | {row[3]}")


# -----------------------------------------------------------
# ✅ SECOND PAGE (Main Simulation Interface)
# -----------------------------------------------------------
def open_simulation_page(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Memory Allocation Visualizer")
    root.geometry("480x550")
    root.configure(bg="#1e1f22")

    def add_styled_label(parent, text):
        return Label(parent, text=text.upper(), font=("Segoe UI", 9, "bold"), bg="#292b2e", fg="#04e2ff")

    container = Frame(root, bg="#292b2e", padx=20, pady=20)
    container.pack(pady=25)

    title = Label(root, text="MEMORY ALLOCATION VISUALIZER", font=("Segoe UI", 14, "bold"),
                  fg="#04e2ff", bg="#1e1f22")
    title.pack(pady=5)

    card = Frame(container, bg="#333539", padx=20, pady=20, relief="ridge", bd=3)
    card.pack()

    add_styled_label(card, "Total Memory Size (bytes)").pack(anchor="w")
    total_memory_entry = Entry(card, width=35); total_memory_entry.pack(pady=3)

    add_styled_label(card, "Number of Processes (Paging)").pack(anchor="w")
    num_processes_entry = Entry(card, width=35); num_processes_entry.pack(pady=3)

    add_styled_label(card, "Process Sizes (e.g., 300,200,150)").pack(anchor="w")
    process_sizes_entry = Entry(card, width=35); process_sizes_entry.pack(pady=3)

    add_styled_label(card, "Page / Frame Size").pack(anchor="w")
    page_size_entry = Entry(card, width=35); page_size_entry.pack(pady=3)

    add_styled_label(card, "Segmentation (ex: 100,200;150;300,80)").pack(anchor="w")
    segment_sizes_entry = Entry(card, width=35); segment_sizes_entry.pack(pady=4)

    def start_simulation():
        inputs = parse_inputs(total_memory_entry, num_processes_entry, process_sizes_entry, page_size_entry, segment_sizes_entry)
        if inputs:
            total_memory, num_processes, process_sizes, page_size, segment_sizes = inputs

            messagebox.showinfo("Paging Simulation", "Paging Visualization Starting...")
            visualize_paging(total_memory, num_processes, process_sizes, page_size)

            messagebox.showinfo("Segmentation Simulation", "Segmentation Visualization Starting...")
            visualize_segmentation(total_memory, num_processes, segment_sizes)

    Button(root, text="START SIMULATION", font=("Segoe UI", 11, "bold"),
           bg="#04e2ff", fg="black", width=20, command=start_simulation).pack(pady=15)


# -----------------------------------------------------------
# ✅ FIRST PAGE (Project Intro & Definitions)
# -----------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Memory Allocation Visualizer")
    root.geometry("500x500")
    root.configure(bg="#1e1f22")

    title = Label(root, text="MEMORY ALLOCATION VISUALIZER", font=("Segoe UI", 16, "bold"),
                  fg="#04e2ff", bg="#1e1f22")
    title.pack(pady=20)

    intro_frame = Frame(root, bg="#292b2e", padx=20, pady=20, relief="ridge", bd=3)
    intro_frame.pack(padx=30, pady=10)

    Label(intro_frame, text="📘 Paging Definition:", font=("Segoe UI", 11, "bold"),
          fg="#04e2ff", bg="#292b2e").pack(anchor="w", pady=(0, 5))
    Label(intro_frame,
          text="Paging divides memory into fixed-size blocks (pages and frames) "
               "to eliminate external fragmentation.",
          wraplength=400, justify="left", fg="white", bg="#292b2e").pack(anchor="w")

    Label(intro_frame, text="\n📗 Segmentation Definition:", font=("Segoe UI", 11, "bold"),
          fg="#04e2ff", bg="#292b2e").pack(anchor="w", pady=(10, 5))
    Label(intro_frame,
          text="Segmentation divides memory into variable-sized segments "
               "based on logical divisions like code, stack, and data.",
          wraplength=400, justify="left", fg="white", bg="#292b2e").pack(anchor="w")

    Button(root, text="NEXT ➜", font=("Segoe UI", 12, "bold"),
           bg="#04e2ff", fg="black", width=12, command=lambda: open_simulation_page(root)).pack(pady=30)

    root.mainloop()


if __name__ == "__main__":
    main()
