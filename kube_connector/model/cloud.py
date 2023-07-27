class Cloud:
    def __init__(self, req):
        self.name = req["name"]
        self.provider = req["provider"]
