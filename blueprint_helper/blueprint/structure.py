from typing import Dict, Any, Self
from .structure_info import StructureInfo
from .mesh import Mesh
from .primitives import Edge, Face
from ._exceptions import StructureException

class Structure:
    def __init__(self, info: StructureInfo, mesh: Mesh, rivets: Dict[str, Any]) -> None:
        self.__info = info
        self.__mesh = mesh
        self.__rivets = rivets

    def get_info(self) -> StructureInfo:
        return self.__info
    
    def get_mesh(self) -> Mesh:
        return self.__mesh
    
    def get_rivets(self) -> Dict[str, Any]:
        return self.__rivets
    
    def join(self, other: Self) -> None:
        version = self.__info.get_version()
        other_version = other.get_info().get_version()
        if version != other_version:
            raise StructureException(f"Версии структур не совпадают: {version} ≠ {other_version}")
        
        name = self.__info.get_name()
        joined_name_prefix = "  (ОБЪЕДИНЁННЫЙ)"
        if not name.endswith(joined_name_prefix):
            self.__info.set_name(name + joined_name_prefix)

        self.__info.set_smooth_angle(max(self.__info.get_smooth_angle(), other.get_info().get_smooth_angle()))
        self.__info.set_grid_size(min(self.__info.get_grid_size(), other.get_info().get_grid_size()))

        x_offset = self.__mesh.get_bounding_box().calculate_x_offset(other.get_mesh().get_bounding_box())
        y_offset = self.__mesh.get_bounding_box().calculate_y_offset(other.get_mesh().get_bounding_box())
        z_offset = self.__mesh.get_bounding_box().calculate_z_offset(other.get_mesh().get_bounding_box())

        replaced_vertex_indices = {}
        for vertex in other.get_mesh().get_vertices(True):
            new_index = self.__mesh.add_vertex(vertex.add(x_offset, y_offset, z_offset))
            replaced_vertex_indices[vertex.get_id()] = new_index

        for edge in other.get_mesh().get_edges(True):
            v1 = replaced_vertex_indices[edge.get_vertex1()]
            v2 = replaced_vertex_indices[edge.get_vertex2()]
            flag = edge.get_flag()
            self.__mesh.add_edge(Edge(v1, v2, flag))

        for face in other.get_mesh().get_faces(True):
            vi = []
            for v in face.get_vertex_indices():
                vi.append(replaced_vertex_indices[v])
            self.__mesh.add_face(Face(vi, face.get_thicknesses(), face.get_bitmask(), face.get_te()))