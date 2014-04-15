class Dummy(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class Github(Dummy):

    def get_repo(self, *args, **kwargs):
        return Repo(*args, **kwargs)

class Repo(Dummy):

    def __init__(self, *args, **kwargs):
        super(Repo, self).__init__(*args, **kwargs)
        self.full_name = "mocked_repo"

    def get_pull(self, *args, **kwargs):
        return Pull(*args, **kwargs)

class Pull(Dummy):

    def __init__(self, *args, **kwargs):
        super(Pull, self).__init__(*args, **kwargs)
        self.number = args[0]
        self.base = Base(*args, **kwargs)
        self.title = "title"
        self.body = "body"

    def get_commits(self, *args, **kwargs):
        return []

class Base(Dummy):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.repo = Repo(*args, **kwargs)

