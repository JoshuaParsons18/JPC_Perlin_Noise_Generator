# Perlin Noise Generator

The Perlin Noise Generator is a Python program that allows you to generate and visualize Perlin noise. Perlin noise is a type of gradient noise used in computer graphics to create natural-looking textures, patterns, and terrain. It is widely used in procedural generation for games, simulations, and visual effects.

## How to Use

### Prerequisites

Before using the Perlin Noise Generator, you need to have the following software installed on your system:

- Python 3
- Tkinter (Python's standard GUI library)

### Installation

1. Clone the repository or download the source code as a ZIP file.

2. Navigate to the project directory.

3. Install the required Python dependencies using the following command:

   ```bash
   pip install opensimplex pillow joblib
   ```

### Running the Program

To run the Perlin Noise Generator, execute the following command in the project directory:

```bash
python PerlinNoiseGenerator.py
```

The GUI window will open, allowing you to interact with the generator.

### Using the GUI

The GUI interface provides the following options to customize the Perlin noise generation:

- **Width and Height**: Set the dimensions of the noise grid.

- **Seed**: The seed value for random number generation. Changing the seed will produce different noise patterns.

- **Octaves**: The number of octaves used in the noise generation. Higher octaves create more detailed noise patterns.

- **Persistence**: A value between 0 and 1 that controls how much each successive octave contributes to the final noise.

- **Lacunarity**: The factor by which the frequency of each successive octave changes.

- **Scale**: The scale of the noise. Smaller values produce larger and more stretched patterns.

- **Intensity Slider**: Adjust the intensity of the generated noise. This affects the grayscale image's contrast.

- **Generate**: Click this button to generate and display the Perlin noise.

- **Export Noise**: Click this button to export the generated noise as a PNG image.

### Exporting the Noise

After adjusting the settings and generating the noise, you can export the current noise image by clicking the "Export Noise" button. The exported image will be saved as "noise.png" in the project directory. The exported image will have the same intensity as the one displayed on the GUI.

## About Perlin Noise

Perlin noise was developed by Ken Perlin in the 1980s and has become a popular tool for generating natural-looking textures and random patterns in computer graphics. It is widely used in various applications, including generating terrain for video games, creating procedural textures, and simulating natural phenomena.

For more information on Perlin noise, you can refer to the following resources:

- [Wikipedia: Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise)
- [Ken Perlin's Original Paper](https://mrl.nyu.edu/~perlin/paper445.pdf)

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to modify the content to better suit your project and add any other relevant information or details about the Perlin Noise Generator.
