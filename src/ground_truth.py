import os
import rasterio
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt


class GroundTruth:
    """
    Classe pour traiter les données raster et analyser l'évolution des classes.
    """

    def __init__(self):
        pass

    def mask_evolution(self, folder_path):
        """
        Calcule l'évolution des masques pour tous les fichiers .tif dans un dossier.

        Args:
            folder_path (str): Chemin vers le dossier contenant les fichiers .tif.

        Returns:
            np.array: Matrice d'évolution des masques.
            list: Liste des dates extraites des fichiers.
        """
        tif_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".tif")])
        evol_matrix = np.empty((len(tif_files), 7))  # 7 classes
        dates = []

        for index, tif_path in enumerate(tif_files):
            with rasterio.open(tif_path) as src:
                for i in range(1, 8):  # Assumer 7 bandes
                    band = src.read(i).astype(np.float32)

                    # Vérifier si la bande est vide
                    if np.sum(band) == 0:
                        evol_matrix[index][i - 1] = 0
                        continue

                    band_max = np.max(band)
                    band_normalized = band / band_max if band_max != 0 else band
                    total_band = np.sum(band_normalized)
                    pc_band = total_band / (band.shape[0] * band.shape[1]) * 100
                    evol_matrix[index][i - 1] = pc_band

            # Détecter et extraire la date du nom du fichier
            filename = os.path.basename(tif_path)
            match = re.search(r'\d{4}[-_]\d{2}[-_]\d{2}', filename)
            if match:
                dates.append(match.group(0).replace("_", "-"))
            else:
                print(f"Format de date inconnu dans le fichier : {filename}")

        return evol_matrix, dates

    def store_mask_evol(self, evol_matrix, dates, folder_name):
        """
        Sauvegarde la matrice d'évolution des masques sous forme de fichier CSV.

        Args:
            evol_matrix (np.array): Matrice d'évolution des masques.
            dates (list): Liste des dates extraites des fichiers.
            folder_name (str): Nom du dossier.
        """
        df = pd.DataFrame(evol_matrix, columns=[f"Band_{i+1}" for i in range(7)], index=dates)
        csv_filename = f"{folder_name}.csv"
        df.to_csv(csv_filename)
        print(f"CSV saved: {csv_filename}")

    def show_mask_evol(self, evol_matrix, dates, folder_name):
        """
        Affiche un graphique de l'évolution des masques.

        Args:
            evol_matrix (np.array): Matrice d'évolution des masques.
            dates (list): Liste des dates extraites des fichiers.
            folder_name (str): Nom du dossier.
        """
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        class_names = [
            'Classe 1 - Impervious Surfaces', 'Classe 2 - Agriculture',
            'Classe 3 - Forest and Other Vegetation', 'Classe 4 - Wetlands',
            'Classe 5 - Soil', 'Classe 6 - Water', 'Classe 7 - Ice and Snow'
        ]

        plt.figure(figsize=(10, 6))
        for i in range(evol_matrix.shape[1]):  # Boucle sur chaque classe
            plt.plot(dates, evol_matrix[:, i], label=class_names[i], color=colors[i])

        plt.title(f"Évolution des masques - {folder_name}")
        plt.xlabel("Dates")
        plt.ylabel("Proportion de la classe (%)")
        plt.ylim(0, 100)
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{folder_name}.png")
        #plt.show()
        print(f"Graph saved: {folder_name}.png")


def main():
    ground_truth = GroundTruth()

    # Liste des dossiers contenant les fichiers .tif
    folders = [
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/1311_3077_13_10N/Labels/Raster/10N-122W-40N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/1417_3281_13_11N/Raster/11N-117W-33N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/1487_3335_13_11N/Labels/Raster/11N-114W-31N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/1700_3100_13_13N/Labels/Raster/13N-105W-40N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2006_3280_13_15N/Labels/Raster/15N-91W-33N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2029_3764_13_15N/Labels/Raster/15N-90W-14N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2065_3647_13_16N/Labels/Raster/16N-89W-19N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2235_3403_13-17N/Labels/Raster/17N-81W-29N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2415_3082_13_18N/Labels/Raster/18N-73W-40N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2459_4406_13-19S/Labels/Raster/19S-71W-13S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2470_5030_13_19S/Labels/Raster/19S-5E-34N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2528_4620_13_19S/Labels/Raster/19S-53W-22S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2624_4314_13_20S/Labels/Raster/20S-64W-9S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2697_3715_13_20N/Labels/Raster/20N-61W-16N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2832_4366_13_21S/Labels/Raster/21S-55W-11S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/2850_4139_13_21S/Labels/Raster/21S-54W-1S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/3002_4273_13_22S/Labels/Raster/22S-48W-7S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/3998_3016_13_30N/Labels/Raster/30N-4W-42N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4127_2991_13_31N/Labels/Raster/31N-1E-43N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4169_3944_13_31N/Labels/Raster/31N-3E-6N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4223_3246_13_31N/Labels/Raster/31N-36E-34N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4240_3972_13_32N/Labels/Raster/32N-6E-5N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4254_2915_13_32N/Labels/Raster/32N-6E-45N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4397_4302_13_33S/Labels/Raster/33S-13E-9S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4421_3800_13_33N/Labels/Raster/33N-14E-12N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4426_3835_13_33N/Labels/Raster/33N-14E-11N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4622_3159_13_34N/Labels/Raster/34N-23E-38N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4768_4131_13_35S/Labels/Raster/35S-29E-1S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4780_3377_13_36N/Labels/Raster/36N-30E-30N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4791_3920_13_36N/Labels/Raster/36N-30E-7N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4806_3588_13_36N/Labels/Raster/36N-31E-21N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4838_3506_13_36N/Labels/Raster/36N-32E-25N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4856_4087_13_36N/Labels/Raster/36N-33E-0N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/4881_3344_13_36N/Labels/Raster/36N-34E-31N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/5111_4560_13-38S/Labels/Raster/38S-44E-19S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/5125_4049_13_38N/Labels/Raster/38N-45E-2N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/5863_3800_13_43N/Labels/Raster/43N-77E-12N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/5926_3715_13_44N/Labels/Raster/44N-80E-16N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/5989_3554_13_44N/Labels/Raster/44N-83E-23N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6204_3495_13-46N/Labels/Raster/46N-92E-25N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6381_3681_13_47N/Labels/Raster/47N-100E-17N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6466_3380_13_48N/Labels/Raster/48N-104E-29N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6468_3360_13_48N/Labels/Raster/48N-104E-30N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6475_3361_13_48N/Labels/Raster/48N-104E-30N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6688_3456_13_49N/Labels/Raster/49N-113E-22N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6730_3430_13_50N/Labels/Raster/50N-115E-28N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6752_3115_13_50N/Labels/Raster/50N-116E-39N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6810_3478_13_50N/Labels/Raster/50N-119E-26N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6813_3313_13_50N/Labels/Raster/50N-119E-32N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/6824_4117_13_50S/Labels/Raster/50S-119E-0S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/7026_3201_13-52N/Labels/Raster/52N-128E-36N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/7312_3008_13_54N/Labels/Raster/54N-141E-43N-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/7367_5050_13-54S/Labels/Raster/54S-143E-38S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/7513_4968_13_56S/Labels/Raster/56S-150E-35S-L3H-SR",
        "/Users/ghalia/Desktop/Telecom_IA/Projet Fil Rouge/airbus_ghalia/data/labels/8077_5007_13_60S/Labels/Raster/60S-174E-37S-L3H-SR"
    ]
    for folder_path in folders:
        folder_name = os.path.basename(folder_path)
        try:
            print(f"Processing folder: {folder_path}")
            evol_matrix, dates = ground_truth.mask_evolution(folder_path)
            ground_truth.store_mask_evol(evol_matrix, dates, folder_name)
            ground_truth.show_mask_evol(evol_matrix, dates, folder_name)
        except Exception as e:
            print(f"Erreur lors du traitement du dossier {folder_path}: {e}")


if __name__ == "__main__":
    main()