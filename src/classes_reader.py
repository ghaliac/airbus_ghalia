import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt


class ClassesReader:
    def __init__(self, file_path):
        """
        Classe pour lire et manipuler un fichier raster avec Rasterio.

        Args:
            file_path (str): Chemin vers le fichier raster.
        """
        self.file_path = file_path
        try:
            self.image = rasterio.open(self.file_path)
            self.bandes = self.image.count
            self.metadata = self.image.meta
            self.dict_classes = {
                "Impervious surfaces": 1,
                "Agriculture": 2,
                "Forest": 3,
                "Wetlands": 4,
                "Soil": 5,
                "Water": 6,
                "Snow": 7,
            }
            self.reverse_dict_classes = {
                v: k for k, v in self.dict_classes.items()
            }  # Inverse du dictionnaire

        except rasterio.errors.RasterioIOError as e:
            print(f"Erreur lors de l'ouverture du fichier : {e}")
            raise SystemExit(e)

    def __del__(self):
        """Ferme l'image raster lors de la suppression de l'instance."""
        if self.image and not self.image.closed:
            self.image.close()

    def show_band(self, band=1):
        """
        Affiche une bande spécifique de l'image.

        Args:
            band (int, optional): Numéro de la bande à afficher. Par défaut : 1.

        Raises:
            SystemExit: Si la bande n'existe pas.

        Returns:
            np.array: Données de la bande affichée.
        """
        if band < 1 or band > self.bandes:
            raise SystemExit(f"Bande {band} introuvable.")
        
        data = self.image.read(band)
        plt.imshow(data, cmap="gray")
        plt.colorbar(label="Valeurs des pixels")
        plt.title(f"Bande {band}")
        plt.axis("off")
        plt.show()
        return data

    def show_class(self, classe):
        """
        Affiche une classe spécifique de l'image.

        Args:
            classe (int): Numéro de la classe à afficher.

        Returns:
            np.array: Données de la classe affichée.
        """
        data = self.image.read(classe)
        classe_name = self.reverse_dict_classes.get(classe, f"Unknown Class ({classe})")
        plt.imshow(data, cmap="BuGn")
        plt.colorbar(label="Valeurs des pixels")
        plt.title(f"Classe : {classe_name}")
        plt.axis("off")
        plt.show()
        return data

    def get_n_bands(self):
        """
        Retourne le nombre de bandes de l'image.

        Returns:
            int: Nombre de bandes.
        """
        return self.bandes

    def detect_classes(self):
        """
        Détecte les classes présentes dans le fichier raster.

        Returns:
            list: Numéros des bandes où des classes sont présentes.
        """
        classes = []
        for i in range(1, self.bandes + 1):
            data = self.image.read(i)
            if np.any(data):  # Vérifie si la bande contient des données non nulles
                classes.append(i)
        return classes

    def show_class_list(self, class_list=None):
        """
        Affiche une liste de classes de l'image.

        Args:
            class_list (list, optional): Liste des classes à afficher. Par défaut : détecte automatiquement les classes.

        Returns:
            list[np.array]: Liste des données des classes affichées.
        """
        if class_list is None:
            class_list = self.detect_classes()
        
        class_list_data = []
        num_classes = len(class_list)
        fig, axes = plt.subplots(1, num_classes, figsize=(5 * num_classes, 5))
        
        if num_classes == 1:  # Gère un cas où il n'y a qu'une seule classe
            axes = [axes]

        for i, classe in enumerate(class_list):
            ax = axes[i]
            data = self.image.read(classe)
            ax.imshow(data, cmap="BuGn")
            classe_name = self.reverse_dict_classes.get(classe, f"Unknown Class ({classe})")
            ax.set_title(f"Classe : {classe_name}")
            ax.axis("off")
            class_list_data.append(data)

        plt.tight_layout()
        plt.show()
        return class_list_data
