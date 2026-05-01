from typing import Dict, Any, Union, List
from ._constants import *
from .primitives import Point, Edge, Face
from .bounding_box import BoundingBox
from ._exceptions import MeshException

class Mesh:
    def __init__(self, vertices: List[float], edges: List[int], edge_flags: List[int], faces: List[Dict[str, Any]], major_version: int = 0, minor_version: int = 3) -> None:
        vertex_count = len(vertices)
        edges_count = len(edges)
        edge_flags_count = len(edge_flags)

        if vertex_count % 3 != 0:
            raise ValueError(f"Количество вершин (vertices) должно быть кратно 3, получено {vertex_count}")

        if edges_count < 6:
            raise ValueError(f"Список рёбер (edges) должен содержать минимум 6 индексов вершин, получено {edges_count}")

        if edges_count % 2 != 0:
            raise ValueError(f"Количество индексов в списке рёбер (edges) должно быть чётным, получено {edges_count}")

        if len(edge_flags) != edges_count // 2:
            raise ValueError(f"Список флагов рёбер (edge_flags) должен содержать {edges_count // 2} значений (по числу рёбер), получено {edge_flags_count}")

        if len(faces) < 1:
            raise ValueError("Список граней (faces) не может быть пустым, должен содержать хотя бы один объект")
        
        self.__bb = BoundingBox(
            round(min(vertices[0::3]) * 1000, 1),
            round(min(vertices[1::3]) * 1000, 1),
            round(min(vertices[2::3]) * 1000, 1),
            round(max(vertices[0::3]) * 1000, 1),
            round(max(vertices[1::3]) * 1000, 1),
            round(max(vertices[2::3]) * 1000, 1)
        )
        self.__vertices = vertices
        self.__edges = edges
        self.__edge_flags = edge_flags
        
        for key, face_data in enumerate(faces):
            for parameter in [KEY_FACES_VERTEX_INDICES, KEY_FACES_THICKNESSES, KEY_FACES_BITMASK, KEY_FACES_TE]:
                if parameter not in face_data:
                    raise ValueError(f"Отсутствует параметр '{parameter}' в данных грани '{key}' в списке граней ('faces')")
        
        self.__faces = faces
        self.__major_version = major_version
        self.__minor_version = minor_version

    def get_major_version(self) -> int:
        return self.__major_version
    
    def get_minor_version(self) -> int:
        return self.__minor_version
    
    def get_bounding_box(self) -> BoundingBox:
        return self.__bb
    
    def get_vertices(self, as_point: bool = False) -> Union[List[float], List[Point]]:
        if as_point:
            return [vertex for i in range(self.get_vertex_count()) if (vertex := self.get_vertex(i))]
        return self.__vertices
    
    def get_edges(self, as_class: bool = False) -> Union[List[int], List[Edge]]:
        if as_class:
            return [edge for i in range(self.get_edges_count()) if (edge := self.get_edge(i))]
        return self.__edges
    
    def get_edge_flags(self) -> List[int]:
        return self.__edge_flags
    
    def get_faces(self, as_class: bool = False) -> Union[Dict[str, Any], List[Face]]:
        if as_class:
            return [face for i in range(self.get_faces_count()) if (face := self.get_face(i))]
        return self.__faces

    def get_vertex(self, vertex_index: int) -> Union[Point, bool]:
        i = vertex_index * 3
        try:
            x = round(self.__vertices[i] * 1000, 1)
            y = round(self.__vertices[i + 1] * 1000, 1)
            z = round(self.__vertices[i + 2] * 1000, 1)
            return Point(x, y, z, vertex_index)
        except IndexError:
            return False
    
    def get_edge(self, edge_index: int) -> Union[Edge,  bool]:
        i = edge_index * 2
        try:
            v1 = self.__edges[i]
            v2 = self.__edges[i + 1]
            flag = self.__edge_flags[edge_index]
            return Edge(v1, v2, flag)
        except IndexError:
            return False
    
    def get_face(self, face_index: int) -> Union[Face, bool]:
        try:
            face_data = self.__faces[face_index]
            return Face(
                face_data[KEY_FACES_VERTEX_INDICES], 
                face_data[KEY_FACES_THICKNESSES], 
                face_data[KEY_FACES_BITMASK], 
                face_data[KEY_FACES_TE]
            )
        except IndexError:
            return False
    
    def get_vertex_count(self) -> int:
        return len(self.__vertices) // 3
    
    def get_edges_count(self) -> int:
        return len(self.__edges) // 2
    
    def get_faces_count(self) -> int:
        return len(self.__faces)
    
    def add_vertex(self, vertex: Point) -> int:
        x = vertex.get_x()
        y = vertex.get_y()
        z = vertex.get_z()
        
        self.__vertices.append(x/ 1000)
        self.__vertices.append(y / 1000)
        self.__vertices.append(z / 1000)

        self.__bb.expand_to_include_point(x, y, z)
        return self.get_vertex_count() - 1
    
    def add_edge(self, edge: Edge) -> int:
        v1 = edge.get_vertex1()
        v2 = edge.get_vertex2()

        for v in (v1, v2):
            if not self.get_vertex(v):
                raise MeshException(f"Ребро содержит несуществующую вершину: {v}")
        
        self.__edges.append(edge.get_vertex1())
        self.__edges.append(edge.get_vertex2())
        self.__edge_flags.append(edge.get_flag())
        return self.get_edges_count() - 1
    
    def add_face(self, face: Face) -> int:
        for v in face.get_vertex_indices():
            if not self.get_vertex(v):
                raise MeshException(f"Грань содержит несуществующую вершину: {v}")
        self.__faces.append({
            KEY_FACES_VERTEX_INDICES: face.get_vertex_indices(),
            KEY_FACES_THICKNESSES: face.get_thicknesses(),
            KEY_FACES_BITMASK: face.get_bitmask(),
            KEY_FACES_TE: face.get_te()
        })
        return self.get_faces_count() - 1

    def set_vertex(self, vertex_index, vertex: Point) -> bool:
        i = vertex_index * 3
        try:
            x = vertex.get_x()
            y = vertex.get_y()
            z = vertex.get_z()

            self.__vertices[i] = x / 1000
            self.__vertices[i + 1] = y / 1000
            self.__vertices[i + 2] = z / 1000

            self.__bb.expand_to_include_point(x, y, z)
            return True
        except IndexError:
            raise ValueError(f"Индекс вершины {vertex_index} не существует (допустимый диапазон: 0–{self.get_vertex_count() - 1})")

    def offset(self, x: float, y: float, z: float) -> None:
        for i in range(self.get_vertex_count()):
            self.__vertices[i] += x / 1000
            self.__vertices[i + 1] += y / 1000
            self.__vertices[i + 2] += z / 1000
        self.__bb.offset(x, y, z)