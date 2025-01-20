import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewtonInterpolation:
    def __init__(self):
        """Initialize the Newton Interpolation calculator."""
        self.x_points = []
        self.y_points = []
        self.coefficients = []
        
    def calculate_divided_difference(self, x, y):
        """
        Calculate divided differences for the given points.
        
        Args:
            x (list): x coordinates
            y (list): y coordinates
            
        Returns:
            numpy.ndarray: Table of divided differences
        """
        n = len(x)
        # Create a matrix to store divided differences
        coef = np.zeros([n, n])
        
        # First column is y values
        coef[:,0] = y
        
        # Calculate divided differences
        for j in range(1,n):
            for i in range(n-j):
                coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j] - x[i])
                
        return coef
    
    def newton_interpolation(self, x_points, y_points, x):
        """
        Perform Newton interpolation at point x.
        
        Args:
            x_points (list): Known x coordinates
            y_points (list): Known y coordinates
            x (float): Point at which to interpolate
            
        Returns:
            float: Interpolated value at x
        """
        self.x_points = x_points
        self.y_points = y_points
        
        # Calculate divided differences
        coef = self.calculate_divided_difference(x_points, y_points)
        self.coefficients = coef[0,:]  # Store first row for the polynomial
        
        n = len(x_points)
        p = coef[0][0]  # First coefficient
        
        # Calculate interpolation value using Newton's formula
        for i in range(1, n):
            term = coef[0][i]
            for j in range(i):
                term = term * (x - x_points[j])
            p = p + term
            
        return p

class InterpolationGUI:
    def __init__(self):
        """Initialize the GUI application."""
        self.window = tk.Tk()
        self.window.title("Newton's Divided Difference Interpolation")
        self.interpolator = NewtonInterpolation()
        
       # Configure grid weights for proper spacing
        self.window.grid_rowconfigure(0, weight=0)  # Title row
        self.window.grid_rowconfigure(1, weight=1)  # Content row
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        # Add title label at the top
        title_label = ttk.Label(
            self.window, 
            text="Newton's Divided Difference Interpolation",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Create input frame (left side)
        input_frame = ttk.LabelFrame(self.window, text="Input Data")
        input_frame.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        
        # Configure input frame grid
        input_frame.grid_columnconfigure(1, weight=1) 
        
        # Create a sub-frame for coordinate inputs
        coord_frame = ttk.Frame(input_frame)
        coord_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        coord_frame.grid_columnconfigure(1, weight=1)  
        
        # X coordinate input 
        ttk.Label(coord_frame, text="X coordinate:", width=12).grid(row=0, column=0, padx=(5,2), pady=5)
        self.x_entry = ttk.Entry(coord_frame)
        self.x_entry.grid(row=0, column=1, padx=(2,5), pady=5, sticky="ew")
        
        # Y coordinate input 
        ttk.Label(coord_frame, text="Y coordinate:", width=12).grid(row=1, column=0, padx=(5,2), pady=5)
        self.y_entry = ttk.Entry(coord_frame)
        self.y_entry.grid(row=1, column=1, padx=(2,5), pady=5, sticky="ew")
        
        # Add point button 
        add_button = ttk.Button(input_frame, text="Add Point", command=self.add_point)
        add_button.grid(row=1, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        
        # Points display text area 
        self.points_text = tk.Text(input_frame, height=10, width=30)
        self.points_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Interpolation frame
        interp_frame = ttk.LabelFrame(self.window, text="Interpolation")
        interp_frame.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
        interp_frame.grid_columnconfigure(1, weight=1)  
        
        # Interpolation point input
        ttk.Label(interp_frame, text="Interpolate at x:", width=12).grid(row=0, column=0, padx=(5,2), pady=5)
        self.interp_entry = ttk.Entry(interp_frame)
        self.interp_entry.grid(row=0, column=1, padx=(2,5), pady=5, sticky="ew")
        
        # Calculate button - expand to frame width
        calc_button = ttk.Button(interp_frame, text="Calculate", command=self.calculate_interpolation)
        calc_button.grid(row=1, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        
        # Result display label
        self.result_label = ttk.Label(interp_frame, text="Result: ")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Initialize point storage
        self.x_points = []
        self.y_points = []
        
        # Create matplotlib figure and canvas (right side)
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
        
        # Configure plot
        self.ax.set_title("Interpolation Plot")
        self.ax.grid(True)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.canvas.draw()

        
    def add_point(self):
        """Add a new point to the interpolation data."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            
            self.x_points.append(x)
            self.y_points.append(y)
            
            # Update points display
            self.points_text.delete(1.0, tk.END)
            for i in range(len(self.x_points)):
                self.points_text.insert(tk.END, f"Point {i+1}: ({self.x_points[i]}, {self.y_points[i]})\n")
            
            # Clear entries
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            
            # Update plot
            self.update_plot()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def calculate_interpolation(self):
        """Calculate and display interpolated value."""
        try:
            if len(self.x_points) < 2:
                messagebox.showerror("Error", "Please enter at least 2 points")
                return
                
            x_interp = float(self.interp_entry.get())
            result = self.interpolator.newton_interpolation(self.x_points, self.y_points, x_interp)
            
            self.result_label.config(text=f"Result: f({x_interp}) ≈ {result:.4f}")
            
            # Update plot with interpolation point
            self.update_plot(x_interp, result)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value")
    
    def update_plot(self, x_interp=None, y_interp=None):
        """Update the plot with current points and interpolated value."""
        self.ax.clear()
        
        # Plot original points
        self.ax.scatter(self.x_points, self.y_points, color='blue', label='Given Points')
        
        if len(self.x_points) > 1:
            # Create smooth curve for interpolation
            x_smooth = np.linspace(min(self.x_points), max(self.x_points), 200)
            y_smooth = [self.interpolator.newton_interpolation(self.x_points, self.y_points, x) for x in x_smooth]
            self.ax.plot(x_smooth, y_smooth, 'g-', label='Interpolation')
        
        if x_interp is not None and y_interp is not None:
            self.ax.scatter([x_interp], [y_interp], color='red', label='Interpolated Point')
        
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.canvas.draw()
    
    def run(self):
        """Start the GUI application."""
        self.window.mainloop()

if __name__ == "__main__":
    app = InterpolationGUI()
    app.run()