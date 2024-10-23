from typing import Annotated

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator

from src.handlers.chat import ChatPostRequest

router = APIRouter(
    tags=['chat'],
    prefix='/chat'
)


@router.post('/')
@inject
def post_chat(
    mediatr=Annotated[Mediator, Depends(Provide['mediatr'])]
):
    mediatr.send(ChatPostRequest(msg='chat posted'))
