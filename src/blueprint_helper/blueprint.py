import json
from typing import Dict, Any, Optional

KEY_VERSION = "v"
KEY_NAME = "name"
KEY_SMOOTH_ANGLE = "smoothAngle"
KEY_GRID_SIZE = "gridSize"
KEY_FORMAT = "format"
KEY_MESH = "mesh"
KEY_RIVETS = "rivets"

KEY_MESH_MAJOR_VERSION = "majorVersion"
KEY_MESH_MINOR_VERSION = "minorVersion"
KEY_MESH_VERTICES = "vertices"
KEY_MESH_EDGES = "edges"
KEY_MESH_EDGE_FLAGS = "edgeFlags"
KEY_MESH_FACES = "faces"

KEY_FACES_VERTEX_INDICES = "v"
KEY_FACES_THICKNESSES = "t"
KEY_FACES_BITMASK = "tm"
KEY_FACES_TE = "te"

KEY_RIVETS_PROFILES = "profiles"
KEY_RIVETS_NODES = "nodes"

KEY_PROFILES_MODEL = "model"
KEY_PROFILES_SPACING = "spacing"
KEY_PROFILES_DIAMETER = "diameter"
KEY_PROFILES_HEIGHT = "height"
KEY_PROFILES_PADDING = "padding"

class BlueprintDataException(Exception):
    pass


class Point:
    def __init__(self, x: int|float, y: int|float, z: int|float, id: int = -1):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def get_x(self) -> int|float:
        return self.x
    
    def get_y(self) -> int|float:
        return self.y
    
    def get_y(self) -> int|float:
        return self.y
    
    def get_id(self) -> int:
        return self.id
    
    def __str__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z}, id={self.id})"


class Face:
    def __init__(self, vertex_indeces: list[int], thicknesses: list[int], bitmask: int, te: int = 0):
        vertex_indeces_count = len(vertex_indeces)
        if vertex_indeces_count < 3:
            raise ValueError("Список индексов вершин должен содержать от 3-х до 4-х индексов")
        if len(thicknesses) != vertex_indeces_count:
            raise ValueError(f"Количество толщин каждой вершины в списке толщин каждой вершины ('thicknesses') должно соответствовать количеству индексов вершин: {vertex_indeces_count}")
        
        self.vertex_indeces = vertex_indeces
        self.thicknesses = thicknesses
        self.bitmask = bitmask
        self.te = te

    def get_vertex_indeces(self) -> list[int]:
        return self.vertex_indeces
    
    def get_thicknesses(self) -> list[int]:
        return self.thicknesses
    
    def get_bitmask(self) -> int:
        return self.bitmask
    
    def get_te(self) -> int:
        return self.te


class Mesh:
    def __init__(self, vertices: list[float], edges: list[int], faces: list[Dict[str, Any]], major_version: int = 0, minor_version: int = 3):
        vertices_count = len(vertices)
        if vertices_count % 3 != 0:
            raise ValueError("Количество вершин ('vertices') должно быть кратно 3-м")
        if len(edges) < 6:
            raise ValueError("Список рёбер ('edges') должен содержать минимум 6 индексов вершин")
        if len(faces) < 1:
            raise ValueError("Список граней ('faces') должен содержать минимум один объект")
        
        self._max_x = round(max(vertices[0::3]) * 1000, 1)
        self._max_y = round(max(vertices[1::3]) * 1000, 1)
        self._max_z = round(max(vertices[2::3]) * 1000, 1)

        self._min_x = round(min(vertices[0::3]) * 1000, 1)
        self._min_y = round(min(vertices[1::3]) * 1000, 1)
        self._min_z = round(min(vertices[2::3]) * 1000, 1)

        self._vertices = {}
        for i in range(0, int(vertices_count / 3)):
            self._vertices[i] = Point(
                round(vertices[i] * 1000, 1), 
                round(vertices[i + 1] * 1000, 1), 
                round(vertices[i + 2] * 1000, 1), 
                i
            )

        self._edges = edges
        
        self._faces = []
        for key, face_data in enumerate(faces):
            for parameter in [KEY_FACES_VERTEX_INDICES, KEY_FACES_THICKNESSES, KEY_FACES_BITMASK, KEY_FACES_TE]:
                if parameter not in face_data:
                    raise ValueError(f"Отсутствует параметр '{parameter}' в данных грани '{key}' в списке граней ('faces')")
                
            self._faces.append(Face(
                face_data[KEY_FACES_VERTEX_INDICES], 
                face_data[KEY_FACES_THICKNESSES], 
                face_data[KEY_FACES_BITMASK], 
                face_data[KEY_FACES_TE])
            )

        self.major_version = major_version
        self.minor_version = minor_version
    
    def get_vertices(self) -> Dict[int, Point]:
        return self._vertices
    
    def get_edges(self, as_vertices: bool = False) -> list[int]:
        if as_vertices:
            vertices = []
            for index in self.edges:
                vertices.append(self.edges[index])
            return vertices
        
        return self.edges
    
    def get_edges(self) -> list[int]:
        return self._edges
    
    def get_faces(self) -> Dict[int, Face]:
        return self._faces
    
    def get_vertex_count(self) -> int:
        return len(self._vertices)
    
    def get_edges_count(self) -> int:
        return len(self._edges)
    
    def get_faces_count(self) -> int:
        return len(self._faces)
    
    def get_max_x(self) -> float:
        return self._max_x
    
    def get_max_y(self) -> float:
        return self._max_y
    
    def get_max_z(self) -> float:
        return self._max_z
    
    def get_min_x(self) -> float:
        return self._min_x
    
    def get_min_y(self) -> float:
        return self._min_y
    
    def get_min_z(self) -> float:
        return self._min_z

class StructureInfo:
    def __init__(self, version: str, name: str, smooth_angle: int, grid_size: int, format: str = "freeform"):
        self._version = version
        self._name = name
        self._smooth_angle = smooth_angle
        self._grid_size = grid_size
        self._format = format

    def get_version(self) -> str:
        return self._version
    
    def get_name(self) -> str:
        return self._name
    
    def get_smooth_angle(self) -> str:
        return self._smooth_angle
    
    def get_grid_size(self) -> str:
        return self._grid_size
    
    def get_format(self) -> str:
        return self._format
    
    def __str__(self):
        return f"StructureInfo(version=\"{self._version}\", name=\"{self._name}\", smooth_angle={self._smooth_angle}, grid_size={self._grid_size}, format=\"{self._format}\")"
    

class Structure:
    def __init__(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filepath}' не найден")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ошибка при загрузке данный файла '{filepath}'", e.doc, e.pos)

        for parameter in [KEY_VERSION, KEY_NAME, KEY_SMOOTH_ANGLE, KEY_GRID_SIZE, KEY_FORMAT, KEY_MESH, KEY_RIVETS]:
            if parameter not in data:
                raise BlueprintDataException(f"Отсутствует параметр: '{parameter}'")
            
        self._info = StructureInfo(
            data[KEY_VERSION], 
            data[KEY_NAME], 
            data[KEY_SMOOTH_ANGLE], 
            data[KEY_GRID_SIZE], 
            data[KEY_FORMAT]
        )
            
        mesh_data = data.get(KEY_MESH, {})
        if not isinstance(mesh_data, dict):
            raise ValueError(f"Параметр '{KEY_MESH}' не соответствует типу данных 'object' (JSON)")
        
        for parameter in [KEY_MESH_MAJOR_VERSION, KEY_MESH_MINOR_VERSION, KEY_MESH_VERTICES, KEY_MESH_EDGES, KEY_MESH_FACES]:
            if parameter not in mesh_data:
                raise ValueError(f"Отсутствует параметр '{parameter}' в данных параметра '{KEY_MESH}'")
            
        self._mesh = Mesh(
            mesh_data[KEY_MESH_VERTICES], 
            mesh_data[KEY_MESH_EDGES], 
            mesh_data[KEY_MESH_FACES], 
            mesh_data[KEY_MESH_MAJOR_VERSION], 
            mesh_data[KEY_MESH_MINOR_VERSION]
        )

    def get_info(self) -> StructureInfo:
        return self._info
    
    def get_mesh(self) -> Mesh:
        return self._mesh
        
    
def load(filepath: str) -> Structure:
    return Structure(filepath)