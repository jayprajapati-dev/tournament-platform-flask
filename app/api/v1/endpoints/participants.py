from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Participant])
def read_participants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve participants.
    """
    participants = crud.participant.get_multi(db, skip=skip, limit=limit)
    return participants

@router.post("/", response_model=schemas.Participant)
def create_participant(
    *,
    db: Session = Depends(deps.get_db),
    participant_in: schemas.ParticipantCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create new participant.
    """
    tournament = crud.tournament.get(db=db, id=participant_in.tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    participant = crud.participant.create(db=db, obj_in=participant_in)
    return participant

@router.put("/{participant_id}", response_model=schemas.Participant)
def update_participant(
    *,
    db: Session = Depends(deps.get_db),
    participant_id: int,
    participant_in: schemas.ParticipantUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update a participant.
    """
    participant = crud.participant.get(db=db, id=participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    tournament = crud.tournament.get(db=db, id=participant.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    participant = crud.participant.update(db=db, db_obj=participant, obj_in=participant_in)
    return participant

@router.get("/{participant_id}", response_model=schemas.Participant)
def read_participant(
    *,
    db: Session = Depends(deps.get_db),
    participant_id: int,
):
    """
    Get participant by ID.
    """
    participant = crud.participant.get(db=db, id=participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@router.delete("/{participant_id}", response_model=schemas.Participant)
def delete_participant(
    *,
    db: Session = Depends(deps.get_db),
    participant_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete a participant.
    """
    participant = crud.participant.get(db=db, id=participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    tournament = crud.tournament.get(db=db, id=participant.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    participant = crud.participant.remove(db=db, id=participant_id)
    return participant 