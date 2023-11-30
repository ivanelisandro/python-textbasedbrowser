import os
import shutil


class Arguments:
    """
    Simple class for storing arguments processing rules and values.
    """
    minimum = 2
    local_path = None


class Startup:
    """
    Simplest possible interface to handle startup routines.
    Processes the local storage path for later retrieval.
    """

    @staticmethod
    def get_path():
        """
        Retrieves the local storage path processed from the
        startup arguments.
        """
        return Arguments.local_path

    @staticmethod
    def can_run(arguments):
        """
        Provides startup validation.
        returns True if it can successfully process all startup arguments
        and create the directory for local files, False otherwise.

        Once finished, the path can be retrieved from get_path() method.
        """
        if len(arguments) < Arguments.minimum:
            return False

        Arguments.local_path = arguments[1]

        if os.access(Arguments.local_path, os.F_OK):
            shutil.rmtree(Arguments.local_path)

        os.makedirs(Arguments.local_path, os.W_OK)
        return os.access(Arguments.local_path, os.W_OK)
