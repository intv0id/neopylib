from enum import Enum
from dataclasses import dataclass

class ConstraintType(Enum):
    OBJECT_IS = 1
    OBJECT_ISNOT = 2
    PROPERTY_EQUAL = 3
    PROPERTY_NEQUAL = 4
    PROPERTY_LE = 5
    PROPERTY_GE = 6
    PROPERTY_LT = 7
    PROPERTY_GT = 8
    LABEL_EQUAL = 9
    LABEL_NEQUAL = 10    
    CONSTRAINT_AND = 11
    CONSTRAINT_OR = 12


@dataclass
class LinkConstraint():
    ct: ConstraintType
    obj1: object
    obj2: object
    
    def properties(self, p1: str, p2: str):
        assert self.ct == ConstraintType.OBJECT_IS, "Other attribute assigned in same constraint"
        self.ct = ConstraintType.PROPERTY_EQUAL
        self.obj1 = p1
        self.obj2 = p2
        
    def labels(self, l1: str, l2: str):
        assert self.ct == ConstraintType.OBJECT_IS, "Other attribute assigned in same constraint"
        self.ct = ConstraintType.LABEL_EQUAL
        self.obj1 = l1
        self.obj2 = l2
        
    def __or__(self, other):
        return LinkConstraint(ConstraintType.CONSTRAINT_OR, self, other)
    
    def __and__(self, other):
        return LinkConstraint(ConstraintType.CONSTRAINT_AND, self, other)

    @staticmethod
    def _property_operator(operator: str, obj1, obj2):
        from ..GraphEntities import SymbolicAttribute
        if isinstance(obj1, SymbolicAttribute) and isinstance(obj2, SymbolicAttribute):
            return f"{obj1.ge.gid}.{obj1.key} {operator} {obj2.ge}:{obj2.key}"
        elif isinstance(obj1, SymbolicAttribute) and isinstance(obj2, str):
            return f"{obj1.ge.gid}.{obj1.key} {operator} \"{obj2}\""
        elif isinstance(obj1, SymbolicAttribute) and isinstance(obj2, int):
            return f"{obj1.ge.gid}.{obj1.key} {operator} {obj2}"
        else:
            raise Exception("Unknown operator for given types")

    
    def parse(self) -> str:
        if self.ct == ConstraintType.CONSTRAINT_AND:
            return f"({self.obj1.parse()}) AND ({self.obj2.parse()})"
        elif self.ct == ConstraintType.CONSTRAINT_OR:
            return f"({self.obj1.parse()}) OR ({self.obj2.parse()})"
        elif self.ct == ConstraintType.OBJECT_IS:
            return f"{self.obj1.gid} = {self.obj2.gid}"
        elif self.ct == ConstraintType.PROPERTY_EQUAL:
            return self._property_operator("=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.PROPERTY_NEQUAL:
            return self._property_operator("<>", self.obj1, self.obj2)
        elif self.ct == ConstraintType.PROPERTY_LE:
            return self._property_operator("<=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.PROPERTY_GE:
            return self._property_operator(">=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.PROPERTY_LT:
            return self._property_operator("<", self.obj1, self.obj2)
        elif self.ct == ConstraintType.PROPERTY_GT:
            return self._property_operator(">", self.obj1, self.obj2)
        elif self.ct == ConstraintType.LABEL_EQUAL:
            return self._property_operator("=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.LABEL_NEQUAL:
            return self._property_operator("<>", self.obj1, self.obj2)
        else:
            raise Exception("Unknown operator")
