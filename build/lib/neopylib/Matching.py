from .Constraints.Constraints import ConstraintType, LinkConstraint
from .GraphEntities import Pattern

class NeoMatcher:
    @staticmethod
    def parse(pattern: Pattern, return_objects: list, constraints: LinkConstraint = None) -> str:
        pattern.evaluate()
        return_string = ", ".join(list(map(lambda x:x.gid, return_objects)))
        constraints_string = f"\nWHERE {constraints.parse()}" if constraints is not None else ""
        return f"MATCH {pattern.parse()} {constraints_string} \nRETURN {return_string};"
        