import json
import os
from .structure import Structure
from .structure_info import StructureInfo
from .mesh import Mesh
from ._constants import *
from ._exceptions import BlueprintDataException

def load(filepath: str) -> Structure:
    if not filepath.endswith(".blueprint"):
        raise ValueError("Расширение файла должно соответствовать '.blueprint'")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filepath}' не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка при загрузке данных файла '{filepath}'", e.doc, e.pos)

    for parameter in [KEY_VERSION, KEY_NAME, KEY_SMOOTH_ANGLE, KEY_GRID_SIZE, KEY_FORMAT, KEY_MESH, KEY_RIVETS]:
        if parameter not in data:
            raise BlueprintDataException(f"Отсутствует параметр: '{parameter}'")
            
    info = StructureInfo(
        data[KEY_VERSION], 
        data[KEY_NAME], 
        data[KEY_SMOOTH_ANGLE], 
        data[KEY_GRID_SIZE], 
        data[KEY_FORMAT]
    )
            
    if not isinstance((mesh_data := data.get(KEY_MESH, {})), dict):
        raise ValueError(f"Параметр '{KEY_MESH}' не соответствует типу данных 'object' (JSON)")
        
    for parameter in [KEY_MESH_MAJOR_VERSION, KEY_MESH_MINOR_VERSION, KEY_MESH_VERTICES, KEY_MESH_EDGES, KEY_MESH_FACES]:
        if parameter not in mesh_data:
            raise ValueError(f"Отсутствует параметр '{parameter}' в данных параметра '{KEY_MESH}'")
            
    mesh = Mesh(
        mesh_data[KEY_MESH_VERTICES], 
        mesh_data[KEY_MESH_EDGES], 
        mesh_data[KEY_MESH_EDGE_FLAGS],
        mesh_data[KEY_MESH_FACES], 
        mesh_data[KEY_MESH_MAJOR_VERSION], 
        mesh_data[KEY_MESH_MINOR_VERSION]
    )

    return Structure(info, mesh, data[KEY_RIVETS])

def save(structure: Structure, filepath: str) -> None:
    if not filepath.endswith(".blueprint"):
        filepath += ".blueprint"
    
    if (directory := os.path.dirname(filepath)) and not os.path.exists(directory):
        os.makedirs(directory)

    info = structure.get_info()
    mesh = structure.get_mesh()
    rivets = structure.get_rivets()

    data = {
        KEY_VERSION: info.get_version(),
        KEY_NAME: info.get_name(),
        KEY_SMOOTH_ANGLE: info.get_smooth_angle(),
        KEY_GRID_SIZE: info.get_grid_size(),
        KEY_FORMAT: info.get_format(),
        KEY_MESH: {
            KEY_MESH_MAJOR_VERSION: mesh.get_major_version(),
            KEY_MESH_MINOR_VERSION: mesh.get_minor_version(),
            KEY_MESH_VERTICES: mesh.get_vertices(),
            KEY_MESH_EDGES: mesh.get_edges(),
            KEY_MESH_EDGE_FLAGS: mesh.get_edge_flags(),
            KEY_MESH_FACES: mesh.get_faces()
        },
        KEY_RIVETS: rivets
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)