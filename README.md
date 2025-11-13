# 🧠 Memory Allocation Visualizer (Paging + Segmentation)

A graphical **Memory Allocation Visualizer** built using **Python
(Tkinter GUI + Matplotlib Graphs)**.

------------------------------------------------------------------------

## ✅ Features

-   Paging (Fixed-size frame allocation)
-   Segmentation (Variable-size memory blocks)
-   Unlimited processes supported
-   GUI Built with Tkinter
-   Visualization using Matplotlib
-   Shows FREE blocks clearly in paging
-   Generates Segment Table with Base + Limit

------------------------------------------------------------------------

## 📌 How It Works

### Paging:

-   Memory is divided into **equal sized frames**.
-   Processes are divided into **pages**.
-   Pages get assigned to frames randomly.

### Segmentation:

-   Memory is allocated based on **segment sizes**.
-   Each process may have multiple variable-sized segments.
-   Segments are placed sequentially and visualized.

------------------------------------------------------------------------

## 📦 Requirements

Install dependencies:

``` sh
pip install matplotlib numpy
```

Tkinter is included with Python (Windows & Linux).

------------------------------------------------------------------------

## ▶️ How to Run the Program

1.  Save the code as:

```{=html}
<!-- -->
```
    memory_visualizer.py

2.  Run it:

``` sh
python memory_visualizer.py
```

------------------------------------------------------------------------

## 🧪 Example Input

    Total Memory Size: 1000
    Process Sizes (Paging): 200,300,150
    Page Size: 100
    Segmentation: 100,200;150;300,80

------------------------------------------------------------------------

## Output

-   Paging graph and FREE block visualization
-   Segmentation memory map + Table printed on terminal


