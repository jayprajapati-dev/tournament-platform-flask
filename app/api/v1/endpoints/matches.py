from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Match])
def read_matches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve matches.
    """
    matches = crud.match.get_multi(db, skip=skip, limit=limit)
    return matches

@router.post("/", response_model=schemas.Match)
def create_match(
    *,
    db: Session = Depends(deps.get_db),
    match_in: schemas.MatchCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create new match.
    """
    tournament = crud.tournament.get(db=db, id=match_in.tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    match = crud.match.create(db=db, obj_in=match_in)
    return match

@router.put("/{match_id}", response_model=schemas.Match)
def update_match(
    *,
    db: Session = Depends(deps.get_db),
    match_id: int,
    match_in: schemas.MatchUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update a match.
    """
    match = crud.match.get(db=db, id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    tournament = crud.tournament.get(db=db, id=match.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    match = crud.match.update(db=db, db_obj=match, obj_in=match_in)
    return match

@router.get("/{match_id}", response_model=schemas.Match)
def read_match(
    *,
    db: Session = Depends(deps.get_db),
    match_id: int,
):
    """
    Get match by ID.
    """
    match = crud.match.get(db=db, id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.delete("/{match_id}", response_model=schemas.Match)
def delete_match(
    *,
    db: Session = Depends(deps.get_db),
    match_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete a match.
    """
    match = crud.match.get(db=db, id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    tournament = crud.tournament.get(db=db, id=match.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    match = crud.match.remove(db=db, id=match_id)
    return match 