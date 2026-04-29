import json
import os
from typing import Dict, Any, Self

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

class MeshException(Exception):
    pass

class StructureException(Exception):
    pass

class Point:
    def __init__(self, x: (int | float), y: (int | float), z: (int | float), id: int = -1) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def get_x(self) -> (int | float):
        return self.x
    
    def get_y(self) -> (int | float):
        return self.y
    
    def get_z(self) -> (int | float):
        return self.z
    
    def get_id(self) -> int:
        return self.id
    
    def add(self, x: (int | float), y: (int | float), z: (int | float)) -> Self:
        return Point(self.x + x, self.y + y, self.z + z, self.id)
    
    def __str__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z}, id={self.id})"

class Edge:
    def __init__(self, vertex1: int, vertex2: int, flag: int) -> None:
        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self._flag = flag
    
    def get_vertex1(self) -> int:
        return self._vertex1
    
    def get_vertex2(self) -> int:
        return self._vertex2
    
    def get_flag(self) -> int:
        return self._flag

class Face:
    def __init__(self, vertex_indeces: list[int], thicknesses: list[int], bitmask: int, te: int = 0) -> None:
        vertex_indeces_count = len(vertex_indeces)
        if vertex_indeces_count < 3:
            raise ValueError("Список индексов вершин (vertex_indeces) должен содержать от 3-х до 4-х индексов")
        if len(thicknesses) != vertex_indeces_count:
            raise ValueError(f"Список толщин каждой вершины (thicknesses) должен содержать {vertex_indeces_count} значений")
        
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
    def __init__(self, vertices: list[float], edges: list[int], edge_flags: list[int], faces: list[Dict[str, Any]], major_version: int = 0, minor_version: int = 3) -> None:
        vertex_count = len(vertices)
        edges_count = len(edges)
        if vertex_count % 3 != 0:
            raise ValueError("Количество вершин (vertices) должно быть кратно 3-м")
        if len(edges) < 6:
            raise ValueError("Список рёбер (edges) должен содержать минимум 6 индексов вершин")
        if edges_count % 2 != 0:
            raise ValueError("Количество рёбер (edges) должно быть кратно 2-м")
        if len(edge_flags) != edges_count / 2:
            raise ValueError(f"Список флагов рёбер (edge_flags) должен содержать {int(edges_count / 2)} значений (количество рёбер)")
        if len(faces) < 1:
            raise ValueError("Список граней (faces) должен содержать минимум один объект")
        
        self._max_x = round(max(vertices[0::3]) * 1000, 1)
        self._max_y = round(max(vertices[1::3]) * 1000, 1)
        self._max_z = round(max(vertices[2::3]) * 1000, 1)

        self._min_x = round(min(vertices[0::3]) * 1000, 1)
        self._min_y = round(min(vertices[1::3]) * 1000, 1)
        self._min_z = round(min(vertices[2::3]) * 1000, 1)

        self._vertices = vertices
        self._edges = edges
        self._edge_flags = edge_flags
        
        for key, face_data in enumerate(faces):
            for parameter in [KEY_FACES_VERTEX_INDICES, KEY_FACES_THICKNESSES, KEY_FACES_BITMASK, KEY_FACES_TE]:
                if parameter not in face_data:
                    raise ValueError(f"Отсутствует параметр '{parameter}' в данных грани '{key}' в списке граней ('faces')")
        
        self._faces = faces

        self._major_version = major_version
        self._minor_version = minor_version

    def get_major_version(self) -> int:
        return self._major_version
    
    def get_minor_version(self) -> int:
        return self._minor_version
    
    def get_vertices(self, as_point: bool = False) -> (list[float] | list[Point]):
        if as_point:
            return [vertex for i in range(self.get_vertex_count()) if (vertex := self.get_vertex(i))]
        return self._vertices
    
    def get_edges(self, as_class: bool = False) -> (list[int] | list[Edge]):
        if as_class:
            return [edge for i in range(self.get_edges_count()) if (edge := self.get_edge(i))]
        return self._edges
    
    def get_edge_flags(self) -> list[int]:
        return self._edge_flags
    
    def get_faces(self, as_class: bool = False) -> (Dict[str, Any] | list[Face]):
        if as_class:
            return [face for i in range(self.get_faces_count()) if (face := self.get_face(i))]
        return self._faces

    def get_vertex(self, vertex_index: int) -> (Point | bool):
        i = vertex_index * 3
        try:
            x = round(self._vertices[i] * 1000, 1)
            y = round(self._vertices[i + 1] * 1000, 1)
            z = round(self._vertices[i + 2] * 1000, 1)
            return Point(x, y, z, vertex_index)
        except IndexError:
            return False
    
    def get_edge(self, edge_index: int) -> (Edge | bool):
        i = edge_index * 2
        try:
            v1 = self._edges[i]
            v2 = self._edges[i + 1]
            flag = self._edge_flags[edge_index]
            return Edge(v1, v2, flag)
        except IndexError:
            return False
    
    def get_face(self, face_index: int) -> (Face | bool):
        try:
            face_data = self._faces[face_index]
            return Face(
                face_data[KEY_FACES_VERTEX_INDICES], 
                face_data[KEY_FACES_THICKNESSES], 
                face_data[KEY_FACES_BITMASK], 
                face_data[KEY_FACES_TE]
            )
        except IndexError:
            return False
    
    def get_vertex_count(self) -> int:
        return int(len(self._vertices) / 3)
    
    def get_edges_count(self) -> int:
        return int(len(self._edges) / 2)
    
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
    
    def add_vertex(self, vertex: Point) -> int:
        self._vertices.append(vertex.get_x() / 1000)
        self._vertices.append(vertex.get_y() / 1000)
        self._vertices.append(vertex.get_z() / 1000)
        return self.get_vertex_count() - 1
    
    def add_edge(self, edge: Edge) -> int:
        v1 = edge.get_vertex1()
        v2 = edge.get_vertex2()

        for v in (v1, v2):
            if not self.get_vertex(v):
                raise MeshException(f"Ребро содержит несуществующую вершину: {v}")
        
        self._edges.append(edge.get_vertex1())
        self._edges.append(edge.get_vertex2())
        self._edge_flags.append(edge.get_flag())
        return self.get_edges_count() - 1
    
    def add_face(self, face: Face) -> int:
        for v in face.get_vertex_indeces():
            if not self.get_vertex(v):
                raise MeshException(f"Грань содержит несуществующую вершину: {v}")
        self._faces.append({
            KEY_FACES_VERTEX_INDICES: face.get_vertex_indeces(),
            KEY_FACES_THICKNESSES: face.get_thicknesses(),
            KEY_FACES_BITMASK: face.get_bitmask(),
            KEY_FACES_TE: face.get_te()
        })
        return self.get_faces_count() - 1

    def set_vertex(self, vertex_index, vertex: Point) -> bool:
        i = vertex_index * 3
        try:
            self._vertices[i] = vertex.get_x() / 1000
            self._vertices[i + 1] = vertex.get_y() / 1000
            self._vertices[i + 2] = vertex.get_z() / 1000
            return True
        except IndexError:
            return False

class StructureInfo:
    def __init__(self, version: str, name: str, smooth_angle: int, grid_size: int, format: str = "freeform") -> None:
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
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_smooth_angle(self, angle: int) -> None:
        if angle < 0 or angle > 90:
            raise ValueError("Угол (angle) должен быть указан в диапазоне от 1 до 90 градусов")
        self._smooth_angle = angle

    def set_grid_size(self, grid_size: int) -> None:
        if grid_size < 0 or grid_size > 100:
            raise ValueError("Размер (grid_size) должен быть указан в диапазоне от 1 до 100 градусов")
        self._grid_size = grid_size
    
    def __str__(self):
        return f"StructureInfo(version=\"{self._version}\", name=\"{self._name}\", smooth_angle={self._smooth_angle}, grid_size={self._grid_size}, format=\"{self._format}\")"
    

class Structure:
    def __init__(self, info: StructureInfo, mesh: Mesh, rivets: Dict[str, Any]) -> None:
        self._info = info
        self._mesh = mesh
        self._rivets = rivets

    def get_info(self) -> StructureInfo:
        return self._info
    
    def get_mesh(self) -> Mesh:
        return self._mesh
    
    def get_rivets(self) -> Dict[str, Any]:
        return self._rivets
    
    def join(self, other: Self) -> None:
        version = self._info.get_version()
        other_version = other.get_info().get_version()
        if version != other_version:
            raise StructureException(f"Несовместимые версии структур: {version} != {other_version}")
        
        self._info.set_name(self._info.get_name() + " (ОБЪЕДИНЁННЫЙ)")
        self._info.set_smooth_angle(max(self._info.get_smooth_angle(), other.get_info().get_smooth_angle()))
        self._info.set_grid_size(min(self._info.get_grid_size(), other.get_info().get_grid_size()))

        height_offset = 0
        x_overlap = self._mesh.get_min_x() < other.get_mesh().get_max_x() and self._mesh.get_max_x() > other.get_mesh().get_min_x()
        y_overlap = self._mesh.get_min_y() < other.get_mesh().get_max_y() and self._mesh.get_max_y() > other.get_mesh().get_min_y()
        z_overlap = self._mesh.get_min_z() < other.get_mesh().get_max_z() and self._mesh.get_max_z() > other.get_mesh().get_min_z()

        if x_overlap and y_overlap and z_overlap:
            height_offset = self._mesh.get_max_y() - other.get_mesh().get_min_y()

        replaced_vertex_indices = {}
        for vertex in other.get_mesh().get_vertices(True):
            new_index = self._mesh.add_vertex(vertex.add(0, height_offset, 0))
            replaced_vertex_indices[vertex.get_id()] = new_index

        for edge in other.get_mesh().get_edges(True):
            v1 = replaced_vertex_indices[edge.get_vertex1()]
            v2 = replaced_vertex_indices[edge.get_vertex2()]
            flag = edge.get_flag()
            self._mesh.add_edge(Edge(v1, v2, flag))

        for face in other.get_mesh().get_faces(True):
            vi = []
            for v in face.get_vertex_indeces():
                vi.append(replaced_vertex_indices[v])
            self._mesh.add_face(Face(vi, face.get_thicknesses(), face.get_bitmask(), face.get_te()))

    
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
            
    mesh_data = data.get(KEY_MESH, {})
    if not isinstance(mesh_data, dict):
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
    
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
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