import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Configuración de las posiciones de los planetas (valores aproximados para visualización)
planets = {
    "Mercurio": (0.4, 0, 0),
    "Venus": (0.7, 0, 0),
    "Tierra": (1.0, 0, 0),
    "Marte": (1.5, 0, 0),
    "Júpiter": (5.2, 0, 0),
    "Saturno": (9.5, 0, 0),
    "Urano": (19.8, 0, 0),
    "Neptuno": (30.0, 0, 0)
}

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configuración de la gráfica
ax.set_title("Alineación de Planetas en 3D")
ax.set_xlabel("X (AU)")
ax.set_ylabel("Y (AU)")
ax.set_zlabel("Z (AU)")

# Dibujar los planetas
for planet, position in planets.items():
    x, y, z = position
    ax.scatter(x, y, z, label=planet, s=100)  # Punto en 3D para cada planeta
    ax.text(x, y, z, planet, fontsize=8)     # Etiqueta del planeta

# Ajustar los límites para una mejor visualización
ax.set_xlim([-1, 35])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Mostrar la leyenda y la gráfica
ax.legend()
plt.show()