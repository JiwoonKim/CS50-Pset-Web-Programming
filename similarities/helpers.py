from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""

    # initialize matrix of size len(a) * len(b)
    matrix = []
    # iterate over matrix
    for i in range(len(a) + 1):
        row = []
        for j in range(len(b) + 1):
            # initialize [0, 0]
            if i == 0 and j == 0:
                row.append((0, 0))
            # initialize [0, j] (first row: inserted only)
            elif i == 0 and j != 0:
                row.append((j, Operation.INSERTED))
            # initialize [i, 0] (first column: deleted only)
            elif i != 0 and j == 0:
                row.append((i, Operation.DELETED))
            # fill in the rest
            else:
                # create substitution value
                sub = 0
                if a[i - 1] == b[j - 1]:
                    sub = 0
                else:
                    sub = 1
                op = Operation.DELETED
                # compare deletion, insertion, substitution cases
                deletion = matrix[i - 1][j]
                insertion = row[j - 1]
                substitution = matrix[i - 1][j - 1]
                minimum_value = min(deletion[0] + 1, insertion[0] + 1, substitution[0] + sub)
                if minimum_value == deletion[0] + 1:
                    row.append((minimum_value, Operation.DELETED))
                elif minimum_value == insertion[0] + 1:
                    row.append((minimum_value, Operation.INSERTED))
                else:
                    row.append((minimum_value, Operation.SUBSTITUTED))
        matrix.append(row)
    return matrix