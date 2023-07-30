from opensimplex import OpenSimplex
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import numpy as np
import time
from joblib import Parallel, delayed

class PerlinNoiseGenerator:
    def __init__(self, seed=None, octaves=1, persistence=0.5, lacunarity=2.0, scale=1.0):
        self.seed = seed
        self.octaves = max(1, octaves)  # Ensure octaves is at least 1
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scale = scale
        self.simplex = OpenSimplex(seed=seed)

    def generate_noise(self, x, y):
        noise = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0  # Used for normalizing result to -1.0 - 1.0

        for _ in range(self.octaves):
            noise += amplitude * self.simplex.noise2(x * frequency * self.scale, y * frequency * self.scale)
            max_value += amplitude
            amplitude *= self.persistence
            frequency *= self.lacunarity

        return noise / max_value

    def generate_noise_grid(self, width, height):
        noise_grid = np.empty((height, width), dtype=float)

        def generate_noise_column(x):
            return [self.generate_noise(x, y) for y in range(height)]

        # Use all available CPU cores
        noise_grid = Parallel(n_jobs=-1)(
            delayed(generate_noise_column)(x) for x in range(width)
        )
        return np.transpose(noise_grid)

    def map_noise_to_color(self, noise_value, intensity=1.0):  # Add intensity parameter with default value
        scaled_value = int((noise_value + 1) * 127.5 * intensity)
        return scaled_value 


def generate_and_display_noise(event=None):
    print("Generating and displaying noise...")
    start_time = time.time()
    config = {
        "seed": int(slider_dict["seed"].get()),
        "octaves": int(slider_dict["octaves"].get()),
        "persistence": slider_dict["persistence"].get(),
        "lacunarity": slider_dict["lacunarity"].get(),
        "scale": slider_dict["scale"].get(),
    }

    intensity = intensity_slider.get()  # Get the intensity value from the slider

    perlin_gen = PerlinNoiseGenerator(**config)

    width, height = int(width_textbox.get()), int(height_textbox.get())
    noise_grid = perlin_gen.generate_noise_grid(width, height)

    # Map the noise values to grayscale intensities
    grayscale_image = np.vectorize(lambda x: perlin_gen.map_noise_to_color(x, intensity))(noise_grid)

    # Convert the numpy array to a PIL Image
    grayscale_image_pil = Image.fromarray(np.uint8(grayscale_image))

    # Update the label to display the grayscale image
    photo = ImageTk.PhotoImage(grayscale_image_pil)
    label.config(image=photo)
    label.image = photo

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Noise generated and displayed in {elapsed_time} seconds.")


def export_noise():
    print("Exporting noise...")
    width = int(width_textbox.get())
    height = int(height_textbox.get())

    config = {
        "seed": int(slider_dict["seed"].get()),
        "octaves": int(slider_dict["octaves"].get()),
        "persistence": slider_dict["persistence"].get(),
        "lacunarity": slider_dict["lacunarity"].get(),
        "scale": slider_dict["scale"].get()
    }

    intensity = intensity_slider.get()  # Get the intensity value from the slider

    perlin_gen = PerlinNoiseGenerator(**config)
    noise_grid = perlin_gen.generate_noise_grid(width, height)

    # Map the noise values to grayscale intensities
    grayscale_image = np.vectorize(lambda x: perlin_gen.map_noise_to_color(x, intensity))(noise_grid)

    # Convert the numpy array to a PIL Image
    grayscale_image_pil = Image.fromarray(np.uint8(grayscale_image))

    # Save as PNG
    grayscale_image_pil.save("noise.png", "PNG")

    # Convert image data to a numpy array
    image_array = np.array(grayscale_image_pil, dtype=np.uint8)

    # Save the numpy array to a .raw file
    with open("noise.raw", 'wb') as f:
        image_array.tofile(f)

    print("Noise exported.")


# GUI Interface
root = tk.Tk()
root.title("Perlin Noise Generator")
root.geometry("1280x720")
root.resizable(False, False)

slider_frame = ttk.Frame(root)
slider_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

# Width and height text boxes
width_var = tk.StringVar(value="100")
height_var = tk.StringVar(value="100")

width_label = ttk.Label(slider_frame, text="Width:")
width_textbox = ttk.Entry(slider_frame, textvariable=width_var, validate="key")
width_label.pack()
width_textbox.pack(pady=5)  # padding after width textbox
width_textbox.bind("<Return>", generate_and_display_noise)  # bind Return event
width_textbox.bind("<FocusOut>", generate_and_display_noise)  # bind FocusOut event

height_label = ttk.Label(slider_frame, text="Height:")
height_textbox = ttk.Entry(slider_frame, textvariable=height_var, validate="key")
height_label.pack()
height_textbox.pack(pady=15)  # padding after height textbox
height_textbox.bind("<Return>", generate_and_display_noise)  # bind Return event
height_textbox.bind("<FocusOut>", generate_and_display_noise)  # bind FocusOut event

# Parameters with sliders and text boxes
params = [
    ("seed", 0, 100, "50.00", tk.StringVar(value="50.00")),
    ("octaves", 0, 10, "4.00", tk.StringVar(value="4.00")),
    ("persistence", 0, 1, "0.50", tk.StringVar(value="0.50")),
    ("lacunarity", 0, 10, "2.00", tk.StringVar(value="2.00")),
    ("scale", 0, 1, "0.10", tk.StringVar(value="0.10"))
]

# Create dictionaries to store the slider and text box widgets
slider_dict = {}

for name, from_, to, default, var in params:
    label = ttk.Label(slider_frame, text=name.capitalize() + ":")
    textbox = ttk.Entry(slider_frame, textvariable=var, validate="key")
    textbox.name = name  # Store the name of the parameter as an attribute
    slider = ttk.Scale(slider_frame, from_=from_, to=to, length=200, orient=tk.HORIZONTAL, variable=var)
    
    label.pack()
    textbox.pack()
    slider.pack(pady=5)  # padding after slider
    textbox.bind("<Return>", generate_and_display_noise)  # bind Return event
    textbox.bind("<FocusOut>", generate_and_display_noise)  # bind FocusOut event
    slider.bind("<ButtonRelease-1>", generate_and_display_noise)

    slider_dict[name] = slider

# Create a label for the Intensity slider
intensity_label = ttk.Label(slider_frame, text="Intensity:")
intensity_label.pack()
intensity_slider = ttk.Scale(slider_frame, from_=0.1, to=2.0, length=200, orient=tk.HORIZONTAL)
intensity_slider.set(1.0)  # Set the initial value of the slider
intensity_slider.pack(pady=5)  # padding after intensity slider
intensity_slider.bind("<ButtonRelease-1>", generate_and_display_noise)

# Create a button to export the noise
export_button = ttk.Button(slider_frame, text="Export Noise", command=export_noise)
export_button.pack(pady=20)  # padding after export button

# Create a label to display the grayscale image
label = ttk.Label(root)
label.pack()

# Bind sliders for persistence and lacunarity
slider_dict["persistence"].bind("<ButtonRelease-1>", generate_and_display_noise)
slider_dict["lacunarity"].bind("<ButtonRelease-1>", generate_and_display_noise)


generate_and_display_noise()  # Generate and display the initial noise
root.mainloop()
