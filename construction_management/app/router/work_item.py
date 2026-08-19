from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.work_item import WorkItem
from app.schemas.work_item import WorkItemCreate, WorkItemResponse

router = APIRouter(prefix="/work-items", tags=["work_items"])


@router.post("/", response_model=WorkItemResponse)
def create_work_item(payload: WorkItemCreate, db: Session = Depends(get_db)):
    item = WorkItem(
        site_id=payload.site_id,
        title=payload.title,
        description=payload.description,
        assignee_id=payload.assignee_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=WorkItemResponse)
def get_work_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(WorkItem).filter(WorkItem.id == item_id).first()
    return item
