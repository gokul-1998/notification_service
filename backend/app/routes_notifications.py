from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db, Notification, NotificationStatus, User
from app.schemas import NotificationCreate, NotificationResponse, NotificationStatusUpdate
from app.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

@router.post("/", response_model=dict)
async def create_notification(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Admin only: Create a notification and send it to all users"""
    # Create notification
    db_notification = Notification(
        title=notification.title,
        message=notification.message,
        created_by=current_user.id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Create notification status for all users
    all_users = db.query(User).all()
    for user in all_users:
        notification_status = NotificationStatus(
            notification_id=db_notification.id,
            user_id=user.id,
            is_read=False
        )
        db.add(notification_status)
    
    db.commit()
    
    return {
        "message": "Notification sent to all users",
        "notification_id": db_notification.id,
        "recipients": len(all_users)
    }

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for the current user"""
    query = db.query(
        Notification.id,
        Notification.title,
        Notification.message,
        Notification.created_by,
        Notification.created_at,
        NotificationStatus.is_read,
        NotificationStatus.read_at
    ).join(
        NotificationStatus,
        NotificationStatus.notification_id == Notification.id
    ).filter(
        NotificationStatus.user_id == current_user.id
    )
    
    if unread_only:
        query = query.filter(NotificationStatus.is_read == False)
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        NotificationResponse(
            id=n.id,
            title=n.title,
            message=n.message,
            created_by=n.created_by,
            created_at=n.created_at,
            is_read=n.is_read,
            read_at=n.read_at
        )
        for n in notifications
    ]

@router.get("/unread-count", response_model=dict)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    count = db.query(NotificationStatus).filter(
        NotificationStatus.user_id == current_user.id,
        NotificationStatus.is_read == False
    ).count()
    
    return {"unread_count": count}

@router.put("/{notification_id}/read", response_model=dict)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    notification_status = db.query(NotificationStatus).filter(
        NotificationStatus.notification_id == notification_id,
        NotificationStatus.user_id == current_user.id
    ).first()
    
    if not notification_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification_status.is_read = True
    notification_status.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}

@router.put("/mark-all-read", response_model=dict)
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for the current user"""
    db.query(NotificationStatus).filter(
        NotificationStatus.user_id == current_user.id,
        NotificationStatus.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    db.commit()
    
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Admin only: Delete a notification"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted"}
