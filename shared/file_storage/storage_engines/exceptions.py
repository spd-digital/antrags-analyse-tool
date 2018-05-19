class FilenameMissingExtensionError(AssertionError):
    def __init__(self, file_name):
        self.file_name = file_name
        message = u'file name {} is missing a file extension'.format(file_name)
        super(FilenameMissingExtensionError, self).__init__(message)
