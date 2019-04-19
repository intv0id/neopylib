from enum import Enum
from dataclasses import dataclass

class ConstraintType(Enum):
    OBJECT_IS = 1
    OBJECT_ISNOT = 2
    SYMBOLIC_EQUAL = 3
    SYMBOLIC_NEQUAL = 4
    SYMBOLIC_LE = 5
    SYMBOLIC_GE = 6
    SYMBOLIC_LT = 7
    SYMBOLIC_GT = 8
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
        self.ct = ConstraintType.SYMBOLIC_EQUAL
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
    def _property_type_convertion(obj):
        from ..Entities.GraphEntities import SymbolicProperty, SymbolicFunction
        if isinstance(obj, SymbolicProperty):
            return f"{obj.ge.gid}.{obj.name}"
        elif isinstance(obj, SymbolicFunction):
            return f"{obj.name}({obj.ge.gid})"
        elif isinstance(obj, int):
            return f"{obj}"
        elif isinstance(obj, str):
            return f"\"{obj}\""
        else:
            raise Exception(f"Unsupported type {type(obj)}")

    @staticmethod
    def _property_operator(operator: str, obj1, obj2):
        return f"{LinkConstraint._property_type_convertion(obj1)} {operator} {LinkConstraint._property_type_convertion(obj2)}"

    def parse(self) -> str:
        if self.ct == ConstraintType.CONSTRAINT_AND:
            return f"({self.obj1.parse()}) AND ({self.obj2.parse()})"
        elif self.ct == ConstraintType.CONSTRAINT_OR:
            return f"({self.obj1.parse()}) OR ({self.obj2.parse()})"
        elif self.ct == ConstraintType.OBJECT_IS:
            return f"{self.obj1.gid} = {self.obj2.gid}"
        elif self.ct == ConstraintType.SYMBOLIC_EQUAL:
            return self._property_operator("=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.SYMBOLIC_NEQUAL:
            return self._property_operator("<>", self.obj1, self.obj2)
        elif self.ct == ConstraintType.SYMBOLIC_LE:
            return self._property_operator("<=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.SYMBOLIC_GE:
            return self._property_operator(">=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.SYMBOLIC_LT:
            return self._property_operator("<", self.obj1, self.obj2)
        elif self.ct == ConstraintType.SYMBOLIC_GT:
            return self._property_operator(">", self.obj1, self.obj2)
        elif self.ct == ConstraintType.LABEL_EQUAL:
            return self._property_operator("=", self.obj1, self.obj2)
        elif self.ct == ConstraintType.LABEL_NEQUAL:
            return self._property_operator("<>", self.obj1, self.obj2)
        else:
            raise Exception("Unknown operator")
