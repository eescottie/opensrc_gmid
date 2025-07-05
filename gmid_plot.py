import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
import re

def load_wrdata(filename):
    data_blocks = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        if re.match(r'^[A-Za-z]', lines[i].strip()):
            headers = lines[i].split()
            if len(headers) < 2:
                i += 1
                continue
            block = {h: [] for h in headers}
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^[A-Za-z]', lines[i].strip()):
                vals = lines[i].split()
                if len(vals) == len(headers):
                    for h, v in zip(headers, vals):
                        try:
                            block[h].append(float(v))
                        except ValueError:
                            block[h].append(np.nan)
                i += 1
            for h in headers:
                block[h] = np.array(block[h])
            data_blocks.append(block)
        else:
            i += 1
    return data_blocks

def plot_first_two_columns(data_blocks):
    fig, ax = plt.subplots(figsize=(8,6))
    colors = plt.cm.tab10.colors
    lines = []
    labels = []
    all_x = []
    x_names = []
    y_names = []

    for block_idx, block in enumerate(data_blocks):
        headers = list(block.keys())
        if len(headers) < 2:
            continue
        x_name = headers[0]
        y_name = headers[1]
        x = block[x_name]
        y = block[y_name]
        if len(x) == 0 or len(y) == 0 or len(x) != len(y):
            continue
        
        sort_idx = np.argsort(x)
        x_sorted = x[sort_idx]
        y_sorted = y[sort_idx]

        color = colors[block_idx % len(colors)]
        line, = ax.plot(x_sorted, y_sorted, label=f'{y_name} vs {x_name}', color=color)
        lines.append((line, x_sorted, y_sorted))
        labels.append(f'{y_name} vs {x_name}')
        all_x.append(x_sorted)
        x_names.append(x_name)
        y_names.append(y_name)

    if not lines:
        messagebox.showerror("Error", "No valid data found to plot.")
        return

    x_label = ', '.join(x_names)
    y_label = ', '.join(y_names)
    title = f"{y_label} vs {x_label}"

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # Place legend outside right
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    plt.subplots_adjust(right=0.75, bottom=0.25)  # leave room at bottom for info box

    # Draw canvas once to get legend bbox
    fig.canvas.draw()
    legend_bbox = leg.get_window_extent()

    # Convert legend bbox from pixels to figure fraction
    inv_fig_trans = fig.transFigure.inverted()
    legend_bbox_fig = inv_fig_trans.transform(legend_bbox)
    # legend_bbox_fig is [[x0, y0], [x1, y1]] in figure coords

    # Calculate position for info box just below legend
    x0, y0 = legend_bbox_fig[0]
    x1, y1 = legend_bbox_fig[1]
    info_box_x = x0
    info_box_y = y0 - 0.05  # slightly below legend
    info_box_width = x1 - x0
    info_box_height = 0.04

    # Create a new axes for info box below legend
    info_ax = fig.add_axes([info_box_x, info_box_y, info_box_width, info_box_height])
    info_ax.axis('off')
    info_text = info_ax.text(0, 1, '', va='top', ha='left', fontsize=10,
                             bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9))

    # Vertical cursor line inside plot
    vline = ax.axvline(color='k', lw=0.8, ls='--')

    def on_mouse_move(event):
        if not event.inaxes or event.xdata is None:
            vline.set_visible(False)
            info_text.set_text('')
            fig.canvas.draw_idle()
            return
        x = event.xdata
        vline.set_xdata([x, x])
        vline.set_visible(True)
        info = f"x = {x:.4g}\n"
        for idx, (line, xvec, yvec) in enumerate(lines):
            if len(xvec) == 0:
                continue
            i = np.searchsorted(xvec, x)
            if i == 0:
                y_val = yvec[0]
            elif i >= len(xvec):
                y_val = yvec[-1]
            else:
                x0_, x1_ = xvec[i-1], xvec[i]
                y0_, y1_ = yvec[i-1], yvec[i]
                if x1_ != x0_:
                    y_val = y0_ + (y1_ - y0_) * (x - x0_) / (x1_ - x0_)
                else:
                    y_val = y0_
            info += f"{labels[idx]}: y = {y_val:.4g}\n"
        info_text.set_text(info)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        title="Select ngspice wrdata file",
        filetypes=[("Text files", "*.txt *.dat *.out"), ("All files", "*.*")]
    )
    if not filename:
        messagebox.showinfo("No file", "No file selected. Exiting.")
        return
    try:
        data_blocks = load_wrdata(filename)
        if not data_blocks:
            messagebox.showerror("Error", "No data blocks found in file.")
            return
        plot_first_two_columns(data_blocks)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load or plot file:\n{e}")

if __name__ == "__main__":
    main()

