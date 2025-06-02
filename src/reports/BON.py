# Ajustar para usar apenas o módulo trimesh, sem a dependência do pacote 'stl'

import numpy as np
import trimesh

# Parâmetros do cilindro (base do modelo)
height = 30  # mm
radius = 10  # mm
segments = 32

# Geração dos vértices da base circular
theta = np.linspace(0, 2*np.pi, segments, endpoint=False)
circle_points = np.stack((radius * np.cos(theta), radius * np.sin(theta), np.zeros_like(theta)), axis=-1)
circle_top = circle_points + np.array([0, 0, height])

# Juntar as bases inferior e superior
vertices = np.concatenate((circle_points, circle_top), axis=0)

# Gerar faces laterais
faces = []
for i in range(segments):
    next_i = (i + 1) % segments
    # Lateral (duas triangulações)
    faces.append([i, next_i, segments + i])
    faces.append([next_i, segments + next_i, segments + i])
    # Base inferior
    faces.append([i, next_i, segments * 2])
    # Base superior
    faces.append([segments + i, segments + next_i, segments * 2 + 1])

# Adiciona vértices do centro das tampas
vertices = np.vstack([vertices, [[0, 0, 0], [0, 0, height]]])

# Cria malha Trimesh e exporta como 3MF
cylinder_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
output_path = "data/chico_bonbon_base.3mf"
cylinder_mesh.export(output_path)

output_path
