from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.crud import crud_log
from app.models.request import Request, RequestResponse
from app.models.score import Score

router = APIRouter()

@router.post("/request", response_model=RequestResponse)
def track_request(*, db: Session = Depends(dependencies.get_db), request_in: Request) -> RequestResponse:
    log = crud_log.create(db=db, request=request_in)
    if not log:
        raise HTTPException(
            status_code=400,
            detail="Error while creating request",
        )
    return RequestResponse(request_id=log.id)
    

@router.post("/request/score")
def track_score(*, db: Session = Depends(dependencies.get_db), score_in: Score) -> Score:
    # score = crud_score.create(db=db, score=score_in)
    # if not score:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Error while creating score",
    #     )
    # return score
    return Score()

# @router.post("/request/metadata")
# def track_metadata(*, db: Session = Depends(dependencies.get_db), metadata: dict) -> dict:
#     score = crud_score.create(db=db, obj_in=score_in)
#     if not score:
#         raise HTTPException(
#             status_code=400,
#             detail="Error while creating score",
#         )
#     return score
