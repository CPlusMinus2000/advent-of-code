# Point class, for various AoC problems

from typing import List, Tuple, Dict, Union

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{self.x},{self.y}"
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can only compare Point to Point")

        return self.x < other.x and self.y < other.y
    
    def __le__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can only compare Point to Point")

        return self.x <= other.x and self.y <= other.y
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can only compare Point to Point")

        return self.x >= other.x and self.y >= other.y
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can only compare Point to Point")

        return self.x > other.x and self.y > other.y
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0
    
    def __len__(self) -> int:
        return 2
    
    def __getstate__(self) -> Tuple:
        return self.x, self.y
    
    def __setstate__(self, state) -> None:
        self.x, self.y = state
    
    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)
    
    def __pos__(self) -> "Point":
        return self
    
    def __add__(self, other) -> "Point":
        if not isinstance(other, Point):
            raise TypeError("Can only add Point to Point")
        
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> "Point":
        if not isinstance(other, Point):
            raise TypeError("Can only subtract Point from Point")
        
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other) -> Union["Point", float]:
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x * other, self.y * other)
        elif isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Can only multiply Point by float or Point")
    
    def __rmul__(self, other) -> Union["Point", float]:
        return self.__mul__(other)
    
    def __truediv__(self, other) -> Union["Point", float]:
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x / other, self.y / other)
        else:
            raise TypeError("Can only divide Point by float")
    
    def __floordiv__(self, other) -> Union["Point", float]:
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x // other, self.y // other)
        else:
            raise TypeError("Can only divide Point by float")
    
    def __mod__(self, other) -> Union["Point", float]:
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x % other, self.y % other)
        else:
            raise TypeError("Can only modulo Point by float or Point")
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __getitem__(self, key: Union[int, str]) -> float:
        if key == 0 or key == "x":
            return self.x
        elif key == 1 or key == "y":
            return self.y
        else:
            raise IndexError("Point has only 2 dimensions")
    
    def __setitem__(self, key: Union[int, str], value: float) -> None:
        if key == 0 or key == "x":
            self.x = value
        elif key == 1 or key == "y":
            self.y = value
        else:
            raise IndexError("Point has only 2 dimensions")
    
    def __copy__(self) -> "Point":
        return Point(self.x, self.y)
    
    def __iter__(self) -> iter:
        yield self.x
        yield self.y
    
    def __dir__(self) -> List[str]:
        return ["x", "y"]
    
    def asdict(self) -> Dict:
        return {"x": self.x, "y": self.y}
    
    def reflect(self, axis: str, value: float) -> "Point":
        if axis == "x":
            self.x = 2 * value - self.x
        elif axis == "y":
            self.y = 2 * value - self.y
        else:
            raise ValueError("Axis must be x or y")

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __add__(self, other) -> "Point3D":
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) -> "Point3D":
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    def rotations(self) -> List["Point3D"]:
        """
        Return a list of all 24 possible orientations of this point,
        i.e. all right-handed coordinate system possibilities.
        """

        return [
            Point3D(self.x, self.y, self.z),
            Point3D(self.x, self.z, -self.y),
            Point3D(self.x, -self.z, self.y),
            Point3D(self.x, -self.y, -self.z),
            Point3D(-self.x, -self.y, self.z),
            Point3D(-self.x, self.y, -self.z),
            Point3D(-self.x, self.z, self.y),
            Point3D(-self.x, -self.z, -self.y),
            Point3D(self.y, -self.x, self.z),
            Point3D(self.y, self.x, -self.z),
            Point3D(self.y, self.z, self.x),
            Point3D(self.y, -self.z, -self.x),
            Point3D(-self.y, -self.z, self.x),
            Point3D(-self.y, self.z, -self.x),
            Point3D(-self.y, self.x, self.z),
            Point3D(-self.y, -self.x, -self.z),
            Point3D(self.z, self.x, self.y),
            Point3D(self.z, -self.x, -self.y),
            Point3D(self.z, -self.y, self.x),
            Point3D(self.z, self.y, -self.x),
            Point3D(-self.z, -self.x, self.y),
            Point3D(-self.z, self.x, -self.y),
            Point3D(-self.z, self.y, self.x),
            Point3D(-self.z, -self.y, -self.x)
        ]
    
    def rotate(self, rotation: int) -> "Point3D":
        """
        Rotate the point by the given index of the 24 possible orientations.
        """
        
        if rotation == 0:
            return self
        elif rotation == 1:
            return Point3D(self.x, self.z, -self.y)
        elif rotation == 2:
            return Point3D(self.x, -self.z, self.y)
        elif rotation == 3:
            return Point3D(self.x, -self.y, -self.z)
        elif rotation == 4:
            return Point3D(-self.x, -self.y, self.z)
        elif rotation == 5:
            return Point3D(-self.x, self.y, -self.z)
        elif rotation == 6:
            return Point3D(-self.x, self.z, self.y)
        elif rotation == 7:
            return Point3D(-self.x, -self.z, -self.y)
        elif rotation == 8:
            return Point3D(self.y, -self.x, self.z)
        elif rotation == 9:
            return Point3D(self.y, self.x, -self.z)
        elif rotation == 10:
            return Point3D(self.y, self.z, self.x)
        elif rotation == 11:
            return Point3D(self.y, -self.z, -self.x)
        elif rotation == 12:
            return Point3D(-self.y, -self.z, self.x)
        elif rotation == 13:
            return Point3D(-self.y, self.z, -self.x)
        elif rotation == 14:
            return Point3D(-self.y, self.x, self.z)
        elif rotation == 15:
            return Point3D(-self.y, -self.x, -self.z)
        elif rotation == 16:
            return Point3D(self.z, self.x, self.y)
        elif rotation == 17:
            return Point3D(self.z, -self.x, -self.y)
        elif rotation == 18:
            return Point3D(self.z, -self.y, self.x)
        elif rotation == 19:
            return Point3D(self.z, self.y, -self.x)
        elif rotation == 20:
            return Point3D(-self.z, -self.x, self.y)
        elif rotation == 21:
            return Point3D(-self.z, self.x, -self.y)
        elif rotation == 22:
            return Point3D(-self.z, self.y, self.x)
        elif rotation == 23:
            return Point3D(-self.z, -self.y, -self.x)
        else:
            raise ValueError(f"Invalid rotation index: {rotation}")
    
    def l1_norm(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)
