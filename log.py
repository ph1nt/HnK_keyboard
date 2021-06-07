"""print varius level information"""


class ClsDebug:
    """for developing only"""

    CRITICAL = 0
    ALARM = 1
    WARRING = 2
    PROBLEM = 3
    INFO = 5
    # Set correct level below
    level = 0

    def set(self, level=0):
        """Set correct level below"""
        self.level = level

    def log(self, level=0, txt=""):
        """print deebug of correct level"""
        if level >= self.level:
            print(" >>> DEBUG: {}".format(txt))


debug = ClsDebug()
