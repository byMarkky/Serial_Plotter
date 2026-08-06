class Config:

    def __init__(self):
        self.selected_port = None
        self.baud_rate = 115200

    def set_port(self, port):
        #print(port.name)
        self.selected_port = port.name

    def set_baud_rate(self, baud_rate):
        #print("Baud_Rate: " + baud_rate)
        self.baud_rate = baud_rate