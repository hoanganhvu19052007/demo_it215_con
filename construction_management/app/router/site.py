from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.site import ConstructionSite
from app.schemas.site import ConstructionSiteCreate, ConstructionSiteResponse

router = APIRouter(prefix="/sites", tags=["sites"])


@router.post("/", response_model=ConstructionSiteResponse)
def create_site(payload: ConstructionSiteCreate, db: Session = Depends(get_db)):
    site = ConstructionSite(name=payload.name, description=payload.description, owner_id=payload.owner_id)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/")
def list_sites(db: Session = Depends(get_db)):
    sites = db.query(ConstructionSite).all()
    return sites


@router.get("/{site_id}")
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id).first()
    if not site:
        return {"detail": "Not found"}
    return site
