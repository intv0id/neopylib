from .Constraints.Constraints import LinkConstraint, ConstraintType
from .Constraints.Helpers import alpha_enum
from dataclasses import dataclass, field

@dataclass
class GraphEntity:
    gid: str = ""
    properties: dict = field(default_factory=dict)

    def parse_properties(self):
        if len(self.properties) == 0: return ""
        return "{" + ",".join(f"{key}:\"{value}\"" for (key, value) in self.properties.items()) + "}"

    def __getitem__(self, key):
        return SymbolicProperty(self, key)

@dataclass
class Node(GraphEntity):
    labels: set = field(default_factory=set)
        
    def __eq__(self, other):
        return LinkConstraint(ct=ConstraintType.OBJECT_IS, obj1=self, obj2=other)

    def __hash__(self):
        return id(self)

    def parse(self):
        labels_parsed = (":"+", ".join(self.labels)) if self.labels else ""
        prop_parsed = self.parse_properties()
        return f"({self.gid}{labels_parsed}{prop_parsed})"

@dataclass
class Edge(GraphEntity):
    node1: Node = None
    node2: Node = None
    directed: bool= False
    relationship_type: str = None
    def __post_init__(self):
        if(self.node1 is None or self.node2 is None):
            raise ValueError("node1 and node2 need to be defined.")
    def __hash__(self):
        return id(self)
    def __eq__(self, other):
        return LinkConstraint(ct=ConstraintType.OBJECT_IS, obj1=self, obj2=other)
    def __neq__(self, other):
        return LinkConstraint(ct=ConstraintType.OBJECT_ISNOT, obj1=self, obj2=other)
    def parse(self)->str:
        rt_parsed = f":{self.relationship_type}" if self.relationship_type else ""
        prop_parsed = self.parse_properties()
        dir_parsed = ">" if self.directed else ""
        return f"{self.node1.parse()}-[{self.gid}{rt_parsed}{prop_parsed}]-{dir_parsed}{self.node2.parse()}"

@dataclass
class Pattern():
    nodes: set
    edges: set

    def evaluate(self):
        gid_iterator = alpha_enum()
        for n in self.nodes:
            n.gid = next(gid_iterator)
        for e in self.edges:
            e.gid = next(gid_iterator)
    
    def parse(self):
        return ",\n".join(list(map(Edge.parse, self.edges)))


@dataclass 
class SymbolicAttribute():
    ge: GraphEntity
    key: str
    
@dataclass
class SymbolicProperty(SymbolicAttribute):
    value: str = None
    def __eq__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_EQUAL, obj1=self, obj2=other)
    def __ne__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_NEQUAL, obj1=self, obj2=other)
    
    def __le__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_LE, obj1=self, obj2=other)
    def __ge__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_GE, obj1=self, obj2=other)
    
    def __lt__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_LT, obj1=self, obj2=other)
    def __gt__(self, other):
        return LinkConstraint(ct=ConstraintType.PROPERTY_GT, obj1=self, obj2=other)