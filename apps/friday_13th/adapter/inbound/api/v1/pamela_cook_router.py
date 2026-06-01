pamela_cook_router = APIRouter(prefix="/friday-13th/pamela-cook", tags=["pamela-cook"])

@pamela_cook_router.post("/signup")
async def signup(request: Request, port: PamelaCookUseCase = Depends(get_pamela_cook_use_case_port)):
    pamela_cook = PamelaCookUseCase()
    return pamela_cook.signup(request.username, request.password)
