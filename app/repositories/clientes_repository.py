from sqlalchemy.orm import Session

from app.constants import STATUS_PROCESSADO
from app.models import Cliente


class ClientesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.cliente_email == email).first()

    def add(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.flush()
        return cliente

    def mark_processed(self, cliente: Cliente, card_id: str, prioridade: str) -> Cliente:
        cliente.status = STATUS_PROCESSADO
        cliente.prioridade = prioridade
        cliente.pipefy_card_id = card_id
        self.db.flush()
        return cliente
