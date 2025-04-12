from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Team])
def read_teams(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve teams.
    """
    teams = crud.team.get_multi(db, skip=skip, limit=limit)
    return teams

@router.post("/", response_model=schemas.Team)
def create_team(
    *,
    db: Session = Depends(deps.get_db),
    team_in: schemas.TeamCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create new team.
    """
    tournament = crud.tournament.get(db=db, id=team_in.tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    team = crud.team.create(db=db, obj_in=team_in)
    return team

@router.put("/{team_id}", response_model=schemas.Team)
def update_team(
    *,
    db: Session = Depends(deps.get_db),
    team_id: int,
    team_in: schemas.TeamUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update a team.
    """
    team = crud.team.get(db=db, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    tournament = crud.tournament.get(db=db, id=team.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    team = crud.team.update(db=db, db_obj=team, obj_in=team_in)
    return team

@router.get("/{team_id}", response_model=schemas.Team)
def read_team(
    *,
    db: Session = Depends(deps.get_db),
    team_id: int,
):
    """
    Get team by ID.
    """
    team = crud.team.get(db=db, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.delete("/{team_id}", response_model=schemas.Team)
def delete_team(
    *,
    db: Session = Depends(deps.get_db),
    team_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete a team.
    """
    team = crud.team.get(db=db, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    tournament = crud.tournament.get(db=db, id=team.tournament_id)
    if not crud.user.is_superuser(current_user) and (tournament.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    team = crud.team.remove(db=db, id=team_id)
    return team 