class Config:
    """
    Class to store all configuration variables
    """
    def __init__(self):
        self.selected_port = None
        self.baud_rate = 115200
        self.sample_time = -1   # Sample until program is closed
        self.regex = ""

    def get_port(self):
        return self.selected_port

    def get_baud_rate(self):
        return self.baud_rate

    def get_sample_time(self):
        return self.sample_time

    def get_regex(self):
        return self.regex

    def set_sample_time(self, sample_time):
        """
        Set the sample time
        :param sample_time: Number of seconds for plot the data
        :return:
        """
        self.sample_time = sample_time

    def set_regex(self, regex):
        """
        Set the regex
        :param regex: Regex for filtering data
        :return:
        """
        self.regex = regex

    def set_port(self, port):
        """
        Set the port
        :param port: Port number of the computer
        :return:
        """
        self.selected_port = port.name

    def set_baud_rate(self, baud_rate):
        """
        Set the baud rate
        :param baud_rate: Baud rate for the port
        :return:
        """
        self.baud_rate = baud_rate

    def __str__(self):
        return f"<Config port={self.get_port()} baud_rate={self.get_baud_rate()}, sample_time={self.get_sample_time()}, regex={self.get_regex()}>"