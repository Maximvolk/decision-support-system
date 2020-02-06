# Knowledge base mock. Here will be decision model
class KnowledgeBase:
    def __init__(self):
        self.default_recommendation = 'Try to Google it'
        self.data = {
            'permission denied': 'Try with "sudo" or edit file permissions',
            'No such file or directory': 'Check file exists and its name',
            'unmet dependencies': 'Check package dependencies and install them first',
            'broken packages.': 'Check package dependencies or try to reinstall package',
        }

    def infer(self, problem_description):
        for key, value in self.data.items():
            if key in problem_description:
                return value

        return self.default_recommendation

    def complement(self, problem_resume, recommendation):
        # Replace if exists
        self.data[problem_resume] = recommendation
