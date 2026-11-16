import pandas as pd

RECEIVED_COLUMNS = {
    "tracking_code",
    "unit",
    "received_at",
}

DISPATCHED_COLUMNS = {
    "tracking_code",
    "unit",
    "dispatched_at",
}


def prepare_report(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    date_column: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Prepares the report by validating columns, converting date columns to UTC,
    and generating summary statistics.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing shipment data.
        required_columns (set[str]): The set of required column names.
        date_column (str): The name of the date column to convert to UTC.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: A tuple containing the
        validated DataFrame, the summary statistics DataFrame, and the original
        DataFrame with the date column converted to UTC.
    """
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    normalized = dataframe.copy()

    normalized["tracking_code"] = (
        normalized["tracking_code"].astype("string").str.strip().str.upper()
    )

    normalized["unit"] = (
        normalized["unit"]
        .astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    normalized[date_column] = pd.to_datetime(
        normalized[date_column],
        utc=True,
        errors="coerce",
    )

    invalid_mask = (
        normalized["tracking_code"].isna()
        | normalized["tracking_code"].eq("")
        | normalized["unit"].isna()
        | normalized["unit"].eq("")
        | normalized[date_column].isna()
    )

    invalid_rows = normalized.loc[invalid_mask].copy()
    valid_rows = normalized.loc[~invalid_mask].copy()

    duplicate_mask = valid_rows.duplicated(subset=["tracking_code"], keep=False)

    duplicates = valid_rows.loc[duplicate_mask].copy()

    unique_rows = valid_rows.drop_duplicates(
        subset=["tracking_code"],
        keep="first",
    ).copy()

    return unique_rows, duplicates, invalid_rows


def reconcile_reports(
    received_df: pd.DataFrame,
    dispatched_df: pd.DataFrame,
    reference_time: pd.Timestamp,
    threshold_hours: int = 24,
) -> dict[str, pd.DataFrame]:

    if reference_time.tzinfo is None:
        raise ValueError("threshold_hours must be timezone-aware.")

    if threshold_hours <= 0:
        raise ValueError("threshold_hours must be greater than zero.")

    received, received_duplicates, received_invalid = prepare_report(
        received_df,
        RECEIVED_COLUMNS,
        "received_at",
    )

    dispatched, dispatched_duplicates, dispatched_invalid = prepare_report(
        dispatched_df,
        DISPATCHED_COLUMNS,
        "dispatched_at",
    )

    comparison = pd.merge(
        received,
        dispatched,
        on="tracking_code",
        how="outer",
        suffixes=("_received", "_dispatched"),
        indicator=True,
    )

    comparison["status"] = "dispatched"

    comparison.loc[
        comparison["_merge"] == "left_only",
        "status",
    ] = "pending"

    comparison.loc[
        comparison["_merge"] == "right_only",
        "status",
    ] = "dispatch_without_receipt"

    unit_mismatch = comparison["_merge"].eq("both") & comparison["unit_received"].ne(
        comparison["unit_dispatched"]
    )

    comparison.loc[
        unit_mismatch,
        "status",
    ] = "unit_mismatch"

    comparison["is_delayed"] = False

    pending_mask = comparison["status"].eq("pending")

    elapsed_time = reference_time - comparison["received_at"]

    delayed_mask = pending_mask & elapsed_time.gt(pd.Timedelta(hours=threshold_hours))

    comparison.loc[delayed_mask, "status"] = "delayed"
    comparison.loc[delayed_mask, "is_delayed"] = True

    shipments = comparison[
        [
            "tracking_code",
            "unit_received",
            "unit_dispatched",
            "received_at",
            "dispatched_at",
            "status",
            "is_delayed",
        ]
    ].copy()

    return {
        "shipments": shipments,
        "duplicates_received": received_duplicates,
        "duplicates_dispatched": dispatched_duplicates,
        "invalid_received": received_invalid,
        "invalid_dispatched": dispatched_invalid,
    }
