from fastapi import APIRouter, Depends

router = APIRouter(prefix="/friday-13th/jason", tags=["jason_mask"])

@router.post("/login")
async def login(file: UploadFile = File(...), port: JasonDirectorUseCase = Depends(get_jason_director_use_case_port)):
    jason_director = JasonDirectorUseCase()
