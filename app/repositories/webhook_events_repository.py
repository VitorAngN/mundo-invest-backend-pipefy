from sqlalchemy.orm import Session

from app.models import WebhookEvent


class WebhookEventsRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists(self, event_id: str) -> bool:
        return self.db.query(WebhookEvent.id).filter(WebhookEvent.event_id == event_id).first() is not None

    def get_by_event_id(self, event_id: str) -> WebhookEvent | None:
        return self.db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first()

    def add(self, event: WebhookEvent) -> WebhookEvent:
        self.db.add(event)
        self.db.flush()
        return event
