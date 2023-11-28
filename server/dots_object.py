from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class BgImage:
    image_source: str
    x: float
    y: float
    w: float
    h: float
    sc: int
    op: float

    @staticmethod
    def from_dict(obj: Any) -> 'BgImage':
        assert isinstance(obj, dict)
        image_source = from_str(obj.get("imageSource"))
        x = from_float(obj.get("x"))
        y = from_float(obj.get("y"))
        w = from_float(obj.get("w"))
        h = from_float(obj.get("h"))
        sc = from_int(obj.get("sc"))
        op = from_float(obj.get("op"))
        return BgImage(image_source, x, y, w, h, sc, op)

    def to_dict(self) -> dict:
        result: dict = {}
        result["imageSource"] = from_str(self.image_source)
        result["x"] = to_float(self.x)
        result["y"] = to_float(self.y)
        result["w"] = to_float(self.w)
        result["h"] = to_float(self.h)
        result["sc"] = from_int(self.sc)
        result["op"] = to_float(self.op)
        return result


@dataclass
class Rect:
    id: int
    x: float
    y: float
    w: float
    h: float

    @staticmethod
    def from_dict(obj: Any) -> 'Rect':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        x = from_float(obj.get("x"))
        y = from_float(obj.get("y"))
        w = from_float(obj.get("w"))
        h = from_float(obj.get("h"))
        return Rect(id, x, y, w, h)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["x"] = to_float(self.x)
        result["y"] = to_float(self.y)
        result["w"] = to_float(self.w)
        result["h"] = to_float(self.h)
        return result


@dataclass
class DotObject:
    type: str
    project_name: str
    icon_source: str
    bg_image: BgImage
    rects: List[Rect]

    @staticmethod
    def from_dict(obj: Any) -> 'DotObject':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        project_name = from_str(obj.get("projectName"))
        icon_source = from_str(obj.get("iconSource"))
        bg_image = BgImage.from_dict(obj.get("bgImage"))
        rects = from_list(Rect.from_dict, obj.get("rects"))
        return DotObject(type, project_name, icon_source, bg_image, rects)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["projectName"] = from_str(self.project_name)
        result["iconSource"] = from_str(self.icon_source)
        result["bgImage"] = to_class(BgImage, self.bg_image)
        result["rects"] = from_list(lambda x: to_class(Rect, x), self.rects)
        return result


def dot_object_from_dict(s: Any) -> DotObject:
    return DotObject.from_dict(s)


def dot_object_to_dict(x: DotObject) -> Any:
    return to_class(DotObject, x)