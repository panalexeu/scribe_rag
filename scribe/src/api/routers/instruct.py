from fastapi import APIRouter

router = APIRouter(
    tags=['instruct'],
    prefix='/instruct'
)


@router.get('/')
def invoke():
    return {'msg': 'instruction invoked'}
