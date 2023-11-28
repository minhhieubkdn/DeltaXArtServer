from dots_object import *
from constant import *
import matplotlib.pyplot as plt
import math
import json
from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
import constant as ct

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


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
    x: int
    y: int
    sc: int
    op: float

    @staticmethod
    def from_dict(obj: Any) -> 'BgImage':
        assert isinstance(obj, dict)
        image_source = from_str(obj.get("imageSource"))
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        sc = from_int(obj.get("sc"))
        op = from_float(obj.get("op"))
        return BgImage(image_source, x, y, sc, op)

    def to_dict(self) -> dict:
        result: dict = {}
        result["imageSource"] = from_str(self.image_source)
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        result["sc"] = from_int(self.sc)
        result["op"] = to_float(self.op)
        return result


@dataclass
class LineLine:
    x: float
    y: float

    @staticmethod
    def from_dict(obj: Any) -> 'LineLine':
        assert isinstance(obj, dict)
        x = from_float(obj.get("x"))
        y = from_float(obj.get("y"))
        return LineLine(x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = to_float(self.x)
        result["y"] = to_float(self.y)
        return result


@dataclass
class LinePara:
    width: int
    color: str
    item_scale: float

    @staticmethod
    def from_dict(obj: Any) -> 'LinePara':
        assert isinstance(obj, dict)
        width = from_int(obj.get("width"))
        color = from_str(obj.get("color"))
        item_scale = from_float(obj.get("itemScale"))
        return LinePara(width, color, item_scale)

    def to_dict(self) -> dict:
        result: dict = {}
        result["width"] = from_int(self.width)
        result["color"] = from_str(self.color)
        result["itemScale"] = to_float(self.item_scale)
        return result


@dataclass
class LinesObjectLine:
    line_para: LinePara
    line: List[LineLine]

    @staticmethod
    def from_dict(obj: Any) -> 'LinesObjectLine':
        assert isinstance(obj, dict)
        line_para = LinePara.from_dict(obj.get("linePara"))
        line = from_list(LineLine.from_dict, obj.get("line"))
        return LinesObjectLine(line_para, line)

    def to_dict(self) -> dict:
        result: dict = {}
        result["linePara"] = to_class(LinePara, self.line_para)
        result["line"] = from_list(lambda x: to_class(LineLine, x), self.line)
        return result


@dataclass
class LinesObject:
    type: str
    project_name: str
    icon_source: str
    bg_image: BgImage
    lines: List[LinesObjectLine]

    @staticmethod
    def from_dict(obj: Any) -> 'LinesObject':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        project_name = from_str(obj.get("projectName"))
        icon_source = from_str(obj.get("iconSource"))
        bg_image = BgImage.from_dict(obj.get("bgImage"))
        lines = from_list(LinesObjectLine.from_dict, obj.get("lines"))
        return LinesObject(type, project_name, icon_source, bg_image, lines)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["projectName"] = from_str(self.project_name)
        result["iconSource"] = from_str(self.icon_source)
        result["bgImage"] = to_class(BgImage, self.bg_image)
        result["lines"] = from_list(
            lambda x: to_class(LinesObjectLine, x), self.lines)
        return result


def lines_object_from_dict(s: Any) -> LinesObject:
    return LinesObject.from_dict(s)


def lines_object_to_dict(x: LinesObject) -> Any:
    return to_class(LinesObject, x)
