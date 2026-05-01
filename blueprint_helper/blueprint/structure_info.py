class StructureInfo:
    def __init__(self, version: str, name: str, smooth_angle: int, grid_size: int, format: str = "freeform") -> None:
        self.__version = version
        self.set_name(name)
        self.set_smooth_angle(smooth_angle)
        self.set_grid_size(grid_size)
        self.__format = format

    def get_version(self) -> str:
        return self.__version
    
    def get_name(self) -> str:
        return self.__name
    
    def get_smooth_angle(self) -> str:
        return self.__smooth_angle
    
    def get_grid_size(self) -> str:
        return self.__grid_size
    
    def get_format(self) -> str:
        return self.__format
    
    def set_name(self, name: str) -> None:
        self.__name = name

    def set_smooth_angle(self, angle: int) -> None:
        if angle < 0 or angle > 90:
            raise ValueError(f"Угол сглаживания (angle) должен быть в диапазоне от 0 до 90 градусов, получено {angle}")
        self.__smooth_angle = angle

    def set_grid_size(self, grid_size: int) -> None:
        if grid_size < 0 or grid_size > 100:
            raise ValueError(f"Размер сетки (grid_size) должен быть в диапазоне от 0 до 100, получено {grid_size}")
        self.__grid_size = grid_size
    
    def __str__(self):
        return f"StructureInfo(version=\"{self._version}\", name=\"{self._name}\", smooth_angle={self._smooth_angle}, grid_size={self._grid_size}, format=\"{self._format}\")"