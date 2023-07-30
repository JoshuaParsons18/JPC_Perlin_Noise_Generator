class Config:
    def __init__(self, seed=None, octaves=1, persistence=0.5, lacunarity=2.0, scale=1.0):
        self.seed = seed
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scale = scale
