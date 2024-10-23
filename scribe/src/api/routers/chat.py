from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.bootstrap import Container

router = APIRouter(
    tags=['chat'],
    prefix='/chat'
)


@router.post('/')
@inject
def post_chat(
        printer=Depends(Provide[Container.printer])
):
    return {'chat': 'injected'}
