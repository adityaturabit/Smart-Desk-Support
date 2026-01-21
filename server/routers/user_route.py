from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from server.dependencies import get_db, get_current_user
from server.models.db_model import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/support")
def get_support_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != "team_lead":
            raise HTTPException(status_code=403, detail="Only Team Lead allowed")

        agents = (
            db.query(User)
            .filter(User.role == "support")
            .all()
        )

        return [
            {
                "id": a.id,
                "name": a.name,
                "emp_id": a.emp_id,
                "role":a.role,
                "dept_name": a.department.dept_name if a.department else None
            }
            for a in agents
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
