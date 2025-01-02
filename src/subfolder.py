import os

# Chemin vers le fichier contenant la sortie de tree
tree_output_file = "/Users/ghalia/Desktop/output.txt"

# Liste pour stocker les répertoires contenant des fichiers .tif
directories_with_tif = set()

with open(tree_output_file, "r") as file:
    current_dir = None
    for line in file:
        line = line.strip()
        if line.endswith("/"):  # Détecter un répertoire
            current_dir = line
        elif line.endswith(".tif") and current_dir:  # Si un fichier .tif est trouvé
            directories_with_tif.add(current_dir)

# Convertir en liste triée
directories_with_tif = sorted(directories_with_tif)

# Afficher les résultats
print("Directories containing .tif files:")
for directory in directories_with_tif:
    print(directory)