class UserAlreadyExist(Exception):
    def __init__(self):
        self.value = "такой пользователь уже существует"

    def __str__(self):
        return repr(self.value)


class CategoryExistException(Exception):
    def __init__(self):
        self.value = "такая категория уже есть"

    def __str__(self):
        return repr(self.value)


class CategoryNotExistException(Exception):
    def __init__(self):
        self.value = "такой категории нет"

    def __str__(self):
        return repr(self.value)


class IncomeCategoriesNotExist(Exception):
    def __init__(self):
        self.value = "категорий доходов пока нет"

    def __str__(self):
        return repr(self.value)


class ExpenseCategoriesNotExist(Exception):
    def __init__(self):
        self.value = "категорий расходов пока нет"

    def __str__(self):
        return repr(self.value)


class CategoriesNotExist(Exception):
    def __init__(self):
        self.value = "категорий пока нет"

    def __str__(self):
        return repr(self.value)


class HistoryNotExist(Exception):
    def __init__(self):
        self.value = "операций за данный период не существует"

    def __str__(self):
        return repr(self.value)
