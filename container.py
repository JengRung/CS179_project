class container():
    def __init__(self,name,weight) -> None:
        self.name = name
        self.weight = weight
    
    def get_name(self) -> str:
        return self.name
    
    def get_weight(self):
        return self.weight