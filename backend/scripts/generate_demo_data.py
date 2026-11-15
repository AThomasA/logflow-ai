import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pandas as pd

# 1 Configurações do gerador.

SEED = 42
NUMBER_OF_SHIPMENTS = 30

UNITS = [
    "joão pessoa",
    "recife",
]

BASE_DIR = Path(__file__).resolve().parents[2]
SAMPLES_DIR = BASE_DIR / "data" / "samples"

# 2 Função para gerar os recebimentos.


def generate_received_shipments(
    number_of_shipments: int, reference_time: datetime
) -> list[dict]:

    random.seed(SEED)

    shipments = []

    for number in range(1, number_of_shipments + 1):
        unit = random.choice(UNITS)
        hours_ago = random.randint(1, 72)
        received_at = reference_time - timedelta(hours=hours_ago)

        shipment = {
            "tracking_code": f"BR{1000 + number}",
            "unit": unit,
            "received_at": received_at,
        }

        shipments.append(shipment)

    return shipments


# 3 Função para gerar os despachos.


def generate_dispatched_shipments(
    received_shipments: list[dict],
    reference_time: datetime,
) -> list[dict]:

    random.seed(SEED + 1)

    dispatched_shipments = []

    for shipment in received_shipments:
        # Nem todas serão dispachadas.
        should_dispatch = random.random() < 0.65

        if not should_dispatch:
            continue

        received_at = shipment["received_at"]

        avaliable_hours = int((reference_time - received_at).total_seconds() // 3600)

        dispatch_delay = random.randint(
            1,
            min(20, avaliable_hours),
        )

        dispatched_at = received_at + timedelta(hours=dispatch_delay)

        dispatched_shipments.append(
            {
                "tracking_code": shipment["tracking_code"],
                "unit": shipment["unit"],
                "dispatched_at": dispatched_at,
            }
        )

    return dispatched_shipments


# 4 Introduzir incosistências intencionais.


def introduce_demo_inconsistencies(
    received_shipments: list[dict],
    dispatched_shipments: list[dict],
    reference_time: datetime,
) -> None:

    # Duplicidade no relatorio de recebimentos.
    received_shipments.append(received_shipments[0].copy())

    # Registro sem código de rastreio
    invalid_shipment = received_shipments[1].copy()
    invalid_shipment["tracking_code"] = None
    received_shipments.append(invalid_shipment)

    # Despacho sem recebimento correspondente.
    dispatched_shipments.append(
        {
            "tracking_code": "BR9999",
            "unit": "recife",
            "dispatched_at": reference_time,
        }
    )


# 5 Salvar os relatórios


def save_reports(
    received_shipments: list[dict],
    dispatched_shipments: list[dict],
) -> None:

    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    received_df = pd.DataFrame(received_shipments)
    dispatched_df = pd.DataFrame(dispatched_shipments)

    received_df.to_csv(SAMPLES_DIR / "received_report.csv", index=False)
    dispatched_df.to_csv(SAMPLES_DIR / "dispatched_report.csv", index=False)

    received_excel_df = received_df.copy()
    received_excel_df["received_at"] = received_excel_df["received_at"].dt.tz_localize(
        None
    )
    dispatched_excel_df = dispatched_df.copy()
    dispatched_excel_df["dispatched_at"] = dispatched_excel_df[
        "dispatched_at"
    ].dt.tz_localize(None)

    received_excel_df.to_excel(SAMPLES_DIR / "received_report.xlsx", index=False)
    dispatched_excel_df.to_excel(SAMPLES_DIR / "dispatched_report.xlsx", index=False)

    print("Demo reports generated successfully!")
    print(f"Output directory: {SAMPLES_DIR}")
    print(f"Received records: {len(received_df)}")
    print(f"Dispatched records: {len(dispatched_df)}")


# 6 Executar o processo completo


def main() -> None:

    reference_time = datetime.now(UTC)

    received_shipments = generate_received_shipments(
        NUMBER_OF_SHIPMENTS,
        reference_time,
    )

    dispatched_shipments = generate_dispatched_shipments(
        received_shipments,
        reference_time,
    )

    introduce_demo_inconsistencies(
        received_shipments,
        dispatched_shipments,
        reference_time,
    )

    save_reports(
        received_shipments,
        dispatched_shipments,
    )


if __name__ == "__main__":
    main()
