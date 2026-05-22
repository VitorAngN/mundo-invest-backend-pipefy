from app.config import Settings
from app.constants import PRIORIDADE_ALTA, STATUS_PROCESSADO
from app.schemas import ClienteCreate
from app.services.pipefy_service import PipefyService


def test_build_create_card_payload_usa_mutation_e_variaveis_oficiais():
    service = PipefyService(Settings())
    payload = ClienteCreate(
        cliente_nome="João Silva",
        cliente_email="joao.silva@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000,
    )

    result = service.build_create_card_payload(payload)

    assert "mutation CreateClientCard($input: CreateCardInput!)" in result["query"]
    assert "createCard(input: $input)" in result["query"]
    assert "card" in result["query"]
    assert "id" in result["query"]

    variables = result["variables"]
    assert variables["input"]["pipe_id"] == "PIPE_ID_AQUI"
    assert variables["input"]["title"] == "João Silva"

    fields = variables["input"]["fields_attributes"]
    assert fields == [
        {"field_id": "cliente_nome", "field_value": "João Silva"},
        {"field_id": "cliente_email", "field_value": "joao.silva@example.com"},
        {"field_id": "tipo_solicitacao", "field_value": "Atualização cadastral"},
        {"field_id": "valor_patrimonio", "field_value": "250000"},
    ]


def test_build_create_card_payload_preserva_patrimonio_decimal_quando_necessario():
    service = PipefyService(Settings())
    payload = ClienteCreate(
        cliente_nome="João Silva",
        cliente_email="joao.silva@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000.75,
    )

    result = service.build_create_card_payload(payload)

    fields = result["variables"]["input"]["fields_attributes"]
    assert fields[3] == {"field_id": "valor_patrimonio", "field_value": "250000.75"}


def test_build_update_card_fields_payload_usa_update_card_field_com_aliases():
    service = PipefyService(Settings())

    result = service.build_update_card_fields_payload(
        card_id="card_456",
        prioridade=PRIORIDADE_ALTA,
    )

    assert "mutation UpdateClientCard(" in result["query"]
    assert "$statusInput: UpdateCardFieldInput!" in result["query"]
    assert "$priorityInput: UpdateCardFieldInput!" in result["query"]
    assert "status: updateCardField(input: $statusInput)" in result["query"]
    assert "priority: updateCardField(input: $priorityInput)" in result["query"]

    variables = result["variables"]
    assert variables["statusInput"] == {
        "card_id": "card_456",
        "field_id": "status_cliente",
        "new_value": STATUS_PROCESSADO,
    }
    assert variables["priorityInput"] == {
        "card_id": "card_456",
        "field_id": "prioridade",
        "new_value": PRIORIDADE_ALTA,
    }
