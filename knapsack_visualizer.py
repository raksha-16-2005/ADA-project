import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Visualizer")
        self.root.geometry("1000x700")  # Reasonable window size
        
        self.items = []
        self.capacity = tk.IntVar(value=10)  # Default capacity
        self.last_results = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout using frames
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input controls
        input_frame = tk.LabelFrame(top_frame, text="Add Items & Set Capacity")
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(input_frame, text="Value:").grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(input_frame, width=8)
        self.value_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Weight:").grid(row=0, column=2, padx=5)
        self.weight_entry = tk.Entry(input_frame, width=8)
        self.weight_entry.grid(row=0, column=3, padx=5)
        
        tk.Button(input_frame, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white").grid(row=0, column=4, padx=5)
        
        tk.Label(input_frame, text="Capacity:").grid(row=0, column=5, padx=5)
        self.capacity_entry = tk.Entry(input_frame, textvariable=self.capacity, width=8)
        self.capacity_entry.grid(row=0, column=6, padx=5)
        
        # Algorithm buttons
        btn_frame = tk.LabelFrame(top_frame, text="Run Algorithms")
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        buttons = [
            ("0/1 Knapsack", self.run_01_knapsack, "#2196F3"),
            ("Fractional", self.run_fractional_knapsack, "#9C27B0"),
            ("Compare", self.compare_efficiency, "#FF9800")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(btn_frame, text=text, command=command, bg=color, fg="white", width=10).grid(row=0, column=i, padx=3, pady=5)
        
        # Content paned window
        paned = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Items table
        items_frame = tk.Frame(paned)
        paned.add(items_frame, height=150)
        
        tk.Label(items_frame, text="Items List", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Create treeview with scrollbar
        tree_frame = tk.Frame(items_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Value", "Weight"), show="headings", height=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Weight", text="Weight")
        self.tree.column("ID", width=50)
        self.tree.column("Value", width=100)
        self.tree.column("Weight", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Results and visualization pane
        results_frame = tk.Frame(paned)
        paned.add(results_frame, height=400)
        
        # Split results horizontally
        h_paned = tk.PanedWindow(results_frame, orient=tk.HORIZONTAL)
        h_paned.pack(fill=tk.BOTH, expand=True)
        
        # Chart area
        chart_frame = tk.LabelFrame(h_paned, text="Visualization")
        h_paned.add(chart_frame, width=600)
        
        self.chart_frame = tk.Frame(chart_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Output area with scrollbar
        output_frame = tk.LabelFrame(h_paned, text="Results")
        h_paned.add(output_frame, width=300)
        
        text_frame = tk.Frame(output_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(text_frame, height=20, width=40, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def add_item(self):
        try:
            value = int(self.value_entry.get())
            weight = int(self.weight_entry.get())
            
            if value <= 0 or weight <= 0:
                messagebox.showerror("Error", "Please enter positive integers")
                return
                
            item_id = len(self.items) + 1
            self.items.append((value, weight))
            self.tree.insert("", "end", values=(item_id, value, weight))
            self.value_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")

    def run_01_knapsack(self):
        self.output_text.delete(1.0, tk.END)
        self.clear_chart()
        
        if not self.items or self.capacity.get() <= 0:
            messagebox.showerror("Error", "Please add items and set capacity")
            return
            
        start = time.time()
        W = self.capacity.get()
        n = len(self.items)
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        
        # Dynamic programming solution
        for i in range(1, n + 1):
            val, wt = self.items[i - 1]
            for w in range(W + 1):
                if wt <= w:
                    dp[i][w] = max(dp[i - 1][w], val + dp[i - 1][w - wt])
                else:
                    dp[i][w] = dp[i - 1][w]

        # Backtrack to find selected items
        w = W
        selected_items = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                val, wt = self.items[i - 1]
                selected_items.append((val, wt))
                w -= wt

        end = time.time()
        value = dp[n][W]
        duration = round((end - start) * 1000, 3)

        # Display results
        self.output_text.insert(tk.END, "0/1 KNAPSACK RESULT\n" + "-"*25 + "\n\n")
        self.output_text.insert(tk.END, f"Max Value: {value}\n\n")
        self.output_text.insert(tk.END, "Selected Items:\n")
        
        for val, wt in selected_items[::-1]:
            self.output_text.insert(tk.END, f"  Value: {val}, Weight: {wt}\n")
            
        self.output_text.insert(tk.END, f"\nExecution Time: {duration} ms\n")

        self.last_results["01"] = {"value": value, "time": duration, "items": selected_items}
        self.plot_01_chart(selected_items)

    def run_fractional_knapsack(self):
        self.output_text.delete(1.0, tk.END)
        self.clear_chart()
        
        if not self.items or self.capacity.get() <= 0:
            messagebox.showerror("Error", "Please add items and set capacity")
            return

        start = time.time()
        W = self.capacity.get()
        
        items_with_ratio = [(val, wt, val/wt, i) for i, (val, wt) in enumerate(self.items)]
        items_with_ratio.sort(key=lambda x: x[2], reverse=True)

        total_value = 0
        selected = []
        remaining_capacity = W

        for value, weight, ratio, orig_idx in items_with_ratio:
            if remaining_capacity == 0:
                break
                
            if weight <= remaining_capacity:
                selected.append((value, weight, 1.0, orig_idx))
                total_value += value
                remaining_capacity -= weight
            else:
                fraction = remaining_capacity / weight
                selected.append((value, weight, fraction, orig_idx))
                total_value += value * fraction
                remaining_capacity = 0

        end = time.time()
        duration = round((end - start) * 1000, 3)

        # Display results
        self.output_text.insert(tk.END, "FRACTIONAL KNAPSACK RESULT\n" + "-"*25 + "\n\n")
        self.output_text.insert(tk.END, f"Max Value: {round(total_value, 2)}\n\n")
        self.output_text.insert(tk.END, "Selected Items:\n")
        
        for val, wt, frac, idx in selected:
            if frac == 1.0:
                self.output_text.insert(tk.END, f"  Value: {val}, Weight: {wt} (100%)\n")
            else:
                self.output_text.insert(tk.END, 
                    f"  Value: {val}, Weight: {wt} (Used: {round(frac*100, 1)}%)\n")
            
        self.output_text.insert(tk.END, f"\nExecution Time: {duration} ms\n")

        self.last_results["fractional"] = {"value": total_value, "time": duration, "items": selected}
        self.plot_fractional_chart(selected)

    def compare_efficiency(self):
        self.output_text.delete(1.0, tk.END)

        if "01" not in self.last_results or "fractional" not in self.last_results:
            messagebox.showinfo("Info", "Please run both algorithms first")
            return

        val_01 = self.last_results["01"]["value"]
        time_01 = self.last_results["01"]["time"]
        val_frac = self.last_results["fractional"]["value"]
        time_frac = self.last_results["fractional"]["time"]

        self.output_text.insert(tk.END, "ALGORITHM COMPARISON\n" + "-"*25 + "\n\n")
        self.output_text.insert(tk.END, f"0/1 Knapsack:\n  Value: {val_01}\n  Time: {time_01} ms\n\n")
        self.output_text.insert(tk.END, f"Fractional Knapsack:\n  Value: {round(val_frac, 2)}\n  Time: {time_frac} ms\n\n")
        
        faster = "0/1 Knapsack" if time_01 < time_frac else "Fractional Knapsack"
        more_value = "0/1 Knapsack" if val_01 > val_frac else "Fractional Knapsack"

        self.output_text.insert(tk.END, f"Faster Method: {faster}\n")
        self.output_text.insert(tk.END, f"Higher Value Achieved: {more_value}\n")
        
        self.plot_comparison_chart()

    def plot_01_chart(self, selected_items):
        fig, ax = plt.subplots(figsize=(8, 4))
        
        selected_indices = [self.items.index((v, w)) for v, w in selected_items]
        labels = [f"Item {i+1}" for i in range(len(self.items))]
        used = [1.0 if i in selected_indices else 0.0 for i in range(len(self.items))]
        
        colors = ['#3498db' if u > 0 else '#e0e0e0' for u in used]
        ax.bar(range(len(labels)), used, color=colors)
        
        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Item Used")
        ax.set_title("0/1 Knapsack Item Selection")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        
        self.display_chart(fig)

    def plot_fractional_chart(self, selected_items):
        fig, ax = plt.subplots(figsize=(8, 4))
        
        usage = [0.0] * len(self.items)
        for _, _, frac, idx in selected_items:
            usage[idx] = frac
            
        colors = ['#e0e0e0' if u == 0 else '#2ecc71' for u in usage]
        ax.bar(range(len(usage)), usage, color=colors)
        
        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Fraction Used")
        ax.set_title("Fractional Knapsack Item Usage")
        ax.set_xticks(range(len(usage)))
        ax.set_xticklabels([f"Item {i+1}" for i in range(len(usage))])
        
        self.display_chart(fig)

    def plot_comparison_chart(self):
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Create usage data
        zero_one_usage = [0.0] * len(self.items)
        fractional_usage = [0.0] * len(self.items)
        
        for v, w in self.last_results["01"]["items"]:
            idx = self.items.index((v, w))
            zero_one_usage[idx] = 1.0
            
        for _, _, frac, idx in self.last_results["fractional"]["items"]:
            fractional_usage[idx] = frac
        
        # Create bar chart with side-by-side bars
        x = range(len(self.items))
        width = 0.4
        
        ax.bar([i - width/2 for i in x], zero_one_usage, width, label='0/1', color='#3498db')
        ax.bar([i + width/2 for i in x], fractional_usage, width, label='Fractional', color='#2ecc71')
        
        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Usage")
        ax.set_title("Algorithm Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels([f"Item {i+1}" for i in range(len(self.items))])
        ax.legend()
        
        self.display_chart(fig)

    def display_chart(self, fig):
        self.clear_chart()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()
