import math
import re
from collections import OrderedDict
from typing import List

from word2numberi18n import w2n


class Preprocessor:
    def __init__(self, replacements: dict):
        self._replacements: OrderedDict = OrderedDict(
            sorted(
                replacements.items(), reverse=True, key=lambda kv: (len(kv[1]), kv[0])
            )
        )

    def _replace(self, s: str):
        for term in self._replacements:
            s = re.sub(f"\\b{term}\\b", self._replacements[term], s)

        return s

    def _split_by_operations(self, s: str) -> List[str]:
        return re.findall(r"[\w\s\.]+|\+|/|\*|-", s)

    def _is_number(self, s):
        try:
            f = float(s)
            if f == f and f < math.inf and f > -math.inf:
                return True
        except:
            pass

        return False

    def text_to_math(self, s: str) -> str:
        s = self._replace(s)
        list = self._split_by_operations(s)
        result = ""
        for item in list:
            trimmed_item = item.strip()
            if self._is_number(trimmed_item) or trimmed_item in ["+", "-", "*", "/"]:
                result += trimmed_item
            else:
                try:
                    result += str(w2n.word_to_num(trimmed_item))
                except:
                    return ""

        return result
