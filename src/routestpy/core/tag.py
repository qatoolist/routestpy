from typing import Any
from typing import List


class Tag:
    @classmethod
    def IS(cls, tag_string: str, scenario_collection: List[Any]) -> List[Any]:
        return [s for s in scenario_collection if tag_string in s.get_tags()]

    @classmethod
    def IS_NOT(cls, tag_string: str, scenario_collection: List[Any]) -> List[Any]:
        return [s for s in scenario_collection if tag_string not in s.get_tags()]

    @classmethod
    def OR(cls, tag_string1: str, tag_string2: str, scenario_collection: List) -> List:
        return [s for s in scenario_collection if tag_string1 in s.get_tags() or tag_string2 in s.get_tags()]

    @classmethod
    def AND(cls, tag_string1: str, tag_string2: str, scenario_collection: List) -> List:
        return [s for s in scenario_collection if tag_string1 in s.get_tags() and tag_string2 in s.get_tags()]

    @classmethod
    def IN(cls, tags_list: List[str], scenario_collection: List[Any]) -> List[Any]:
        return [s for s in scenario_collection if any(t in s.get_tags() for t in tags_list)]

    @classmethod
    def NOT_IN(cls, tags_list: List[str], scenario_collection: List[Any]) -> List[Any]:
        return [s for s in scenario_collection if set(s.get_tags()).isdisjoint(set(tags_list))]
