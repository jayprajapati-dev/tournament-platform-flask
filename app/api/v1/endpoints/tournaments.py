from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Tournament])
def read_tournaments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve tournaments.
    """
    tournaments = crud.tournament.get_multi(db, skip=skip, limit=limit)
    return tournaments

@router.post("/", response_model=schemas.Tournament)
def create_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_in: schemas.TournamentCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create new tournament.
    """
    tournament = crud.tournament.create_with_owner(
        db=db, obj_in=tournament_in, owner_id=current_user.id
    )
    return tournament

@router.put("/{tournament_id}", response_model=schemas.Tournament)
def update_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    tournament_in: schemas.TournamentUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update a tournament.
    """
    tournament = crud.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    tournament = crud.tournament.update(db=db, db_obj=tournament, obj_in=tournament_in)
    return tournament

@router.get("/{tournament_id}", response_model=schemas.Tournament)
def read_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
):
    """
    Get tournament by ID.
    """
    tournament = crud.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.delete("/{tournament_id}", response_model=schemas.Tournament)
def delete_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete a tournament.
    """
    tournament = crud.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    tournament = crud.tournament.remove(db=db, id=tournament_id)
    return tournament 