from typing import List
from typing import Any

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

    @classmethod
    def evaluate(cls, expression: str, scenario_collection: List) -> List:
        #Needs a review
        # Remove all whitespace characters from the expression
        expression = expression.replace(" ", "")

        # Check if the expression is a single tag string
        if "(" not in expression and ")" not in expression:
            return cls.IS(expression, scenario_collection)

        # Find the outermost set of parentheses
        stack = []
        for i, c in enumerate(expression):
            if c == "(":
                stack.append(i)
            elif c == ")":
                start = stack.pop()
                if not stack:
                    # Evaluate the expression inside the parentheses recursively
                    inner_result = cls.evaluate(expression[start+1:i], scenario_collection)
                    outer_result = expression[:start] + "result" + expression[i+1:]

                    # Evaluate the AND and OR operators
                    while "and" in outer_result or "or" in outer_result:
                        and_index = outer_result.find("and")
                        or_index = outer_result.find("or")

                        if and_index != -1 and and_index < or_index or or_index == -1:
                            # Evaluate the "and" operator
                            tag_string1 = outer_result[and_index-1]
                            tag_string2 = outer_result[and_index+4]
                            temp_result = cls.AND(tag_string1, tag_string2, inner_result)
                            outer_result = outer_result[:and_index-1] + "temp_result" + outer_result[and_index+5:]
                        else:
                            # Evaluate the "or" operator
                            tag_string1 = outer_result[or_index-1]
                            tag_string2 = outer_result[or_index+3]
                            temp_result1 = cls.IS(tag_string1, inner_result)
                            temp_result2 = cls.IS(tag_string2, inner_result)
                            temp_result = list(set(temp_result1 + temp_result2))

                            outer_result = outer_result[:or_index-1] + "temp_result" + outer_result[or_index+4:]

                    # Evaluate the final tag
                    if "result" in outer_result:
                        tag_string = outer_result.replace("result", "")
                        temp_result = cls.IS(tag_string, inner_result)
                        outer_result = outer_result.replace(tag_string, "temp_result")

                    # Merge the inner and outer results
                    if "result" in outer_result:
                        result = []
                        for s1 in eval(outer_result):
                            for s2 in inner_result:
                                if s1.scenario.get_name() == s2.scenario.get_name():
                                    result.append(s2)
                        return result

        # If the expression has no parentheses, evaluate it as a single tag
        return cls.IS(expression, scenario_collection)