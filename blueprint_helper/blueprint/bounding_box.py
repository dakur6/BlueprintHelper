import copy
from typing import Self

class BoundingBox:
    def __init__(self, min_x: float, min_y: float, min_z: float, max_x: float, max_y: float, max_z: float) -> None:
        if min_x > max_x:
            raise ValueError(f"Минимальное значение X ({min_x}) не может превышать максимальное ({max_x})")
        if min_y > max_y:
            raise ValueError(f"Минимальное значение Y ({min_y}) не может превышать максимальное ({max_y})")
        if min_z > max_z:
            raise ValueError(f"Минимальное значение Z ({min_z}) не может превышать максимальное ({max_z})")
        
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z

        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

    def add_coord(self, x: float, y: float, z: float) -> Self:
        min_x = self.min_x
        min_y = self.min_y
        min_z = self.min_z
        max_x = self.max_x
        max_y = self.max_y
        max_z = self.max_z

        if x < 0:
            min_x += x
        else:
            max_x += x

        if y < 0:
            min_y += y
        else:
            max_y += y

        if z < 0:
            min_z += z
        else:
            max_z += z

        return BoundingBox(min_x, min_y, min_z, max_x, max_y, max_z)
    
    def expand_to_include_point(self, x: float, y: float, z: float) -> Self:
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.min_z = min(self.min_z, z)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        self.max_z = max(self.max_z, z)

        return self
    
    def offset(self, x: float, y: float, z: float) -> Self:
        self.min_x += x
        self.min_y += y
        self.min_z += z
        self.max_x += x
        self.max_y += y
        self.max_z += z

        return self
    
    def offset_copy(self, x: float, y: float, z: float) -> Self:
        return copy.copy(self).offset(x, y, z)
    
    def calculate_x_offset(self, other: Self) -> float:
        if not self._intersects_yz(other):
            return 0.0
        
        if other.max_x <= self.min_x:
            return 0.0
        if other.min_x >= self.max_x:
            return 0.0
        
        r_offset = self.min_x - other.max_x # Вправо
        l_offset = self.max_x - other.min_x # Влево

        if abs(r_offset) < abs(l_offset):
            return r_offset if r_offset < 0 else r_offset
        else:
            return l_offset if l_offset > 0 else l_offset
        
    def calculate_y_offset(self, other: Self) -> float:
        if not self._intersects_xz(other):
            return 0.0
        
        if other.max_y <= self.min_y:
            return 0.0
        if other.min_y >= self.max_y:
            return 0.0
        
        up_offset = self.min_y - other.max_y # Вверх
        down_offset = self.max_y - other.min_y # Вниз
        
        if down_offset < 0 and abs(down_offset) < abs(up_offset):
            return down_offset
        elif up_offset < 0:
            return up_offset
        
    def calculate_z_offset(self, other: Self) -> float:
        if not self._intersects_xy(other):
            return 0.0
        
        if other.max_z <= self.min_z:
            return 0.0
        if other.min_z >= self.max_z:
            return 0.0
        
        f_offset = self.min_z - other.max_z # Вперед
        b_offset = self.max_z - other.min_z # Назад
        
        if abs(f_offset) < abs(b_offset):
            return f_offset if f_offset < 0 else f_offset
        else:
            return b_offset if b_offset > 0 else b_offset

    def _intersects_yz(self, other: Self) -> bool:
        return (
            self.min_y < other.max_y and self.max_y > other.min_y and
            self.min_z < other.max_z and self.max_z > other.min_z
        )
    
    def _intersects_xz(self, other: Self) -> bool:
        return (
            self.min_x < other.max_x and self.max_x > other.min_x and
            self.min_z < other.max_z and self.max_z > other.min_z
        )
    
    def _intersects_xy(self, other: Self) -> bool:
        return (
            self.min_x < other.max_x and self.max_x > other.min_x and
            self.min_y < other.max_y and self.max_y > other.min_y
        )