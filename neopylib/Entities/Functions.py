from .GraphEntities import SymbolicFunction, GraphEntity

class label(SymbolicFunction):
    def __init__(self, ge: GraphEntity):
        super().__init__(ge=ge, name="label")

class id_(SymbolicFunction):
    def __init__(self, ge: GraphEntity):
        super().__init__(ge=ge, name="id")
