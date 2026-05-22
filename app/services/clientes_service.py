from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.constants import STATUS_AGUARDANDO_ANALISE
from app.exceptions import ClienteAlreadyExistsError
from app.models import Cliente
from app.repositories.clientes_repository import ClientesRepository
from app.schemas import ClienteCreate
from app.services.pipefy_service import PipefyService


class ClientesService:
    def __init__(self, db: Session, pipefy_service: PipefyService | None = None):
        self.db = db
        self.clientes_repository = ClientesRepository(db)
        self.pipefy_service = pipefy_service or PipefyService()

    def create_cliente(self, payload: ClienteCreate) -> tuple[Cliente, dict]:
        if self.clientes_repository.get_by_email(str(payload.cliente_email)):
            raise ClienteAlreadyExistsError("Cliente já cadastrado com este e-mail.")

        pipefy_payload = self.pipefy_service.build_create_card_payload(payload)
        cliente = Cliente(
            cliente_nome=payload.cliente_nome,
            cliente_email=str(payload.cliente_email),
            tipo_solicitacao=payload.tipo_solicitacao,
            valor_patrimonio=payload.valor_patrimonio,
            status=STATUS_AGUARDANDO_ANALISE,
        )

        try:
            self.clientes_repository.add(cliente)
            cliente.pipefy_card_id = f"simulated_card_{cliente.id}"
            self.db.commit()
            self.db.refresh(cliente)
        except IntegrityError as exc:
            self.db.rollback()
            raise ClienteAlreadyExistsError("Cliente já cadastrado com este e-mail.") from exc

        return cliente, pipefy_payload
