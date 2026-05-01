import math
from typing import Self, List

class Point:
    def __init__(self, x: float, y: float, z: float, id: int = -1) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def get_x(self) -> float:
        return self.x
    
    def get_y(self) -> float:
        return self.y
    
    def get_z(self) -> float:
        return self.z
    
    def get_id(self) -> int:
        return self.id
    
    def add(self, x: float, y: float, z: float) -> Self:
        return Point(self.x + x, self.y + y, self.z + z, self.id)
    
    def addPoint(self, p: Self) -> Self:
        return self.add(p.x, p.y, p.z)
    
    def subtract(self, x: float, y: float, z: float) -> Self:
        return self.add(-x, -y, -z)
    
    def subtractPoint(self, p: Self) -> Self:
        return self.add(-p.x, -p.y, -p.z)
    
    def distance(self, p: Self) -> float:
        return math.sqrt(self.distanceSquared(p))
    
    def distanceSquared(self, p: Self) -> float:
        dx = self.x - p.x
        dy = self.y - p.y
        dz = self.z - p.z
        return (dx * dx) + (dy * dy) + (dz * dz)
    
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
    def __init__(self, vertex_indices: List[int], thicknesses: List[int], bitmask: int, te: int = 0) -> None:
        vertex_indices_count = len(vertex_indices)
        if vertex_indices_count < 3 or vertex_indices_count > 4:
            raise ValueError(f"Список индексов вершин (vertex_indices) должен содержать от 3 до 4 индексов, получено {vertex_indices_count}")
        
        thicknesses_count = len(thicknesses)
        if thicknesses_count != vertex_indices_count:
            raise ValueError(f"Список толщин вершин (thicknesses) должен содержать ровно {vertex_indices_count} значений, получено {thicknesses_count}")
        
        self.__vertex_indices = vertex_indices
        self.__thicknesses = thicknesses
        self.__bitmask = bitmask
        self.__te = te

    def get_vertex_indices(self) -> List[int]:
        return self.__vertex_indices
    
    def get_thicknesses(self) -> List[int]:
        return self.__thicknesses
    
    def get_bitmask(self) -> int:
        return self.__bitmask
    
    def get_te(self) -> int:
        return self.__te