

class PamelaCookInteractor(PamelaCookUseCase):
    def __init__(self, pamela_cook_repository: PamelaCookRepository):
        self.pamela_cook_repository = pamela_cook_repository

    def signup(self, username: str, password: str) -> bool:
        return self.pamela_cook_repository.signup(username, password)
        