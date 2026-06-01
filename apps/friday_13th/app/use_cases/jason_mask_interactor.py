

class JasonMaskInteractor(JasonMaskUseCase):

    def __init__(self, jason_mask_repository: JasonMaskRepository):
        self.jason_mask_repository = jason_mask_repository
        
