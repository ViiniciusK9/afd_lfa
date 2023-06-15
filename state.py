class STATE:
    def __init__(self, initial : bool, identifier) -> None:
        self.ways = list()
        self.initial = initial
        self.identifier = identifier
        self.final = False
    

    def add_way(self, identifie_state, way):
        self.ways.append((identifie_state, way))


    def set_final(self, final : bool):
        self.final = final