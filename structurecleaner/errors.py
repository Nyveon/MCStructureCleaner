"""
MCStructureCleaner
Custom error types
"""


class Error(Exception):
    """Base error class"""

    pass


class InvalidRegionFileError(Error):
    """Raised when the file being processed is not a .mca file"""

    pass


class InvalidFileNameError(Error):
    """Raised when the filename is too short"""

    pass


class EmptyFileError(Error):
    """Raised when a 0byte file is being processed"""

    pass
