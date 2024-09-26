import ast

from .checker import Checker
from .issue import Issue


RELATIONSHIP_FIELDS = ['ForeignKey', 'ManyToManyField', 'OneToOneField']


class DJ21(Issue):
    code = 'DJ21'
    description = 'Pass the model name as a string on relationship fields such {field}.'

class DJ22(Issue):
    code = 'DJ22'
    description = 'Use get_user_model() instead of models.User on relationship fields such {field}.'



class ModelRelationshipFieldChecker(Checker):

    def run(self, node):
        call_name = self.get_call_name(node)
        if call_name not in RELATIONSHIP_FIELDS:
            return

        issues = []
        for keyword in node.keywords:
            if keyword.arg == 'to':
                if not isinstance(keyword.value, ast.Call) and not isinstance(getattr(keyword.value, 'value', None), str):
                    issues.append(
                        DJ21(
                            lineno=node.lineno,
                            col=node.col_offset,
                            parameters={'field': call_name}
                        )
                    )
                if (
                    getattr(keyword.value, 'value', None) in ['models.User', 'User']
                    or getattr(keyword.value, 'attr', None) == 'User'
                    or getattr(keyword.value, 'id', None) == 'User'
                ):
                    issues.append(
                        DJ22(
                            lineno=node.lineno,
                            col=node.col_offset,
                            parameters={'field': call_name}
                        )
                    )


        return issues

