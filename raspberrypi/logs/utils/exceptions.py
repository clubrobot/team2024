import sys
from setups.setup_logger import *

from logs.logger import Logger
from logs.utils.colors import colorise, Colors

DEBUG_VERBOSE = 2
DEBUG_TELEPLOT = 1
DEBUG_NONE = 0


class ExceptionConfigurator():

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        """ if issubclass(exc_type, KeyboardInterrupt): #handle "CTRL+C"
            sys.__excepthook__(exc_type, exc_value, exc_traceback) """

        if ExceptionConfigurator.current_debug_level==DEBUG_NONE: return

        if ExceptionConfigurator.current_debug_level>=DEBUG_TELEPLOT:
            try:#If there is the logger object or originin the args
                if(type(exc_value.args[1])==Logger):#If the second arg in exec is a logger object
                    exc_value.args[1].sendLog(colorise(exc_type.__name__, Colors.RED) + ": " + str(exc_value.args[0]))
                else:
                    Logger.sendLogStatic(colorise(exc_type.__name__, Colors.RED) + ": " + exc_value.args[0], exc_value.args[1])

            except:#if there is only a message
                Logger.sendLogStatic(colorise(exc_type.__name__, Colors.RED) + ": " + str(exc_value))

        if ExceptionConfigurator.current_debug_level==DEBUG_VERBOSE:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

#Setup the hook for exceptions
sys.excepthook = ExceptionConfigurator.handle_exception
                


if __name__ == "__main__":
    a=[0,1]
    Log = Logger("test")
    print(type(Log))
    print(Logger)
    while True:
        pass

    raise Exception("a", Log)
    print("hello")