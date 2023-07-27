class Message:
    def __init__(self):
        self.status = "Failed"
        self.reply = ""
        self.data = ""

    def from_dict(self, m):
        self.status = m["status"]
        if "reply" in m.keys():
            self.reply = m["reply"]
        if "data" in m.keys():
            self.data = m["data"]

    def cast_dict(self):
        if self.status == "Failed":
            return {"status": self.status, "reply": self.reply}
        else:
            if self.reply != "" and self.data != "":
                return {"status": self.status, "reply": self.reply, "data": self.data}
            elif self.reply != "":
                return {"status": self.status, "reply": self.reply}
            elif self.data != "":
                return {"status": self.status, "data": self.data}
            else:
                return {"status": self.status}
