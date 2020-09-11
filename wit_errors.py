class WitError(Exception):
    def __init__(self, err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.err = err

    def __str__(self):
        return self.err


class WitFileNotFound(WitError):
    def __init__(self, selected_path, *args, **kwargs):
        err = f'No file found, check the provided path {selected_path} '
        super().__init__(err, *args, **kwargs)


class WitRepositoryNotFound(WitError):
    def __init__(self, *args, **kwargs):
        err = 'No Wit repository was found\nThere is no .wit folder above the selected file, check the provided path'
        super().__init__(err, *args, **kwargs)

class WitCommitNotFound(WitError):
    def __init__(self, *args, **kwargs):
        err = 'The folder matching the commit_id was not found in the repository'
        super().__init__(err, *args, **kwargs)

class UncommitedChangesError(WitError):
    def __init__(self, *args, **kwargs):
        err = 'There is uncommited changes. please check wit status'
        super().__init__(err, *args, **kwargs)
