# src/data_loading.py
from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np


# ----------------------------
# Config
# ----------------------------
@dataclass(frozen=True)
class Paths:
    base_dir: Path
    raw_path: Path
    processed_dir: Path
    reports_dir: Path
    processed_csv: Path
    schema_report_md: Path


def get_paths() -> Paths:
    """
    Base dir = Project_MuonEDA (this file is in Project_MuonEDA/src/)
    """
    base_dir = Path(__file__).resolve().parents[1]
    raw_path = base_dir / "data" / "raw" / "munra_2.txt"
    processed_dir = base_dir / "data" / "processed"
    reports_dir = base_dir / "reports"

    processed_csv = processed_dir / "munra_clean.csv"
    schema_report_md = reports_dir / "schema_report.md"

    return Paths(
        base_dir=base_dir,
        raw_path=raw_path,
        processed_dir=processed_dir,
        reports_dir=reports_dir,
        processed_csv=processed_csv,
        schema_report_md=schema_report_md,
    )


# ----------------------------
# Loading (robust)
# ----------------------------
def load_munra_raw(raw_path: Path) -> pd.DataFrame:
    """
    Load the raw whitespace-separated file.
    We expect 10 fields per valid line. Bad lines are skipped.
    """
    if not raw_path.exists():
        raise FileNotFoundError(f"RAW file not found: {raw_path}")

    df = pd.read_csv(
        raw_path,
        sep=r"\s+",
        header=None,
        engine="python",
        on_bad_lines="skip",
    )

    # Drop totally empty rows if any sneaked in
    df = df.dropna(how="all")

    # Safety: ensure exactly 10 columns (if not, fail fast)
    if df.shape[1] != 10:
        raise ValueError(
            f"Expected 10 columns after parsing, got {df.shape[1]}. "
            f"Check delimiter or file format."
        )

    # Use neutral column names first (no physics assumptions)
    df.columns = [f"col_{i}" for i in range(10)]
    return df


# ----------------------------
# Basic structural cleaning
# ----------------------------
def basic_structural_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Only structural/format-level cleaning. No physical interpretations.
    - Ensure consistent dtypes (best-effort).
    - Strip whitespace in string columns.
    """
    out = df.copy()

    # Try to convert everything except last col to numeric
    # (In your dataset, col_9 is "COSMIC". We keep it robust anyway.)
    for c in out.columns:
        if c == "col_9":
            out[c] = out[c].astype(str).str.strip()
        else:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    # If any NaN appear due to parsing issues, keep rows but note in report
    return out


# ----------------------------
# Schema / functional profiling (no physics)
# ----------------------------
def _monotonic_hint(s: pd.Series) -> str:
    s = s.dropna()
    if s.empty:
        return "empty"
    if not pd.api.types.is_numeric_dtype(s):
        return "n/a"
    inc = s.is_monotonic_increasing
    dec = s.is_monotonic_decreasing
    if inc and not dec:
        return "monotonic_increasing"
    if dec and not inc:
        return "monotonic_decreasing"
    return "not_monotonic"


def _zero_fraction(s: pd.Series) -> str:
    s = s.dropna()
    if s.empty or not pd.api.types.is_numeric_dtype(s):
        return "n/a"
    return f"{(s.eq(0).mean()*100):.2f}%"


def _constant_hint(s: pd.Series) -> str:
    s2 = s.dropna()
    if s2.empty:
        return "empty"

    nun = s2.nunique()
    if nun == 1:
        return f"constant({s2.iloc[0]})"

    # If numeric with very small range and few unique values -> near-constant
    if pd.api.types.is_numeric_dtype(s2) and nun <= 5:
        mn = float(s2.min())
        mx = float(s2.max())
        rng = mx - mn
        if rng <= 0.5:  # functional threshold: "small variation"
            return f"near_constant(nunique={nun}, range={rng:.4g})"

    if nun <= 3:
        return f"low_cardinality(nunique={nun})"

    return "varies"


def build_schema_report(df: pd.DataFrame) -> str:
    """
    Produces a Markdown report with:
    - dtype
    - nunique
    - min/max (numeric)
    - zero fraction (numeric)
    - monotonic hint (numeric)
    - constant hint
    - a cautious 'possible role' hint (still hypothesis)
    """
    lines: list[str] = []
    lines.append("# MuNRa dataset schema report")
    lines.append("")
    lines.append("**Important:** This report is *functional/technical* profiling only.")
    lines.append("It does **not** assign physical meaning definitively. Any 'possible role' is a hypothesis.")
    lines.append("")
    lines.append(f"- Rows: **{df.shape[0]}**")
    lines.append(f"- Columns: **{df.shape[1]}**")
    lines.append("")

    # Candidate role hints based purely on patterns
    def possible_role(col: str, s: pd.Series) -> str:
        # Only pattern-based hints
        if col == "col_9" and s.nunique() == 1:
            return "label/type (constant category)"
        if pd.api.types.is_numeric_dtype(s):
            if s.nunique() == 1:
                return "constant sensor/setting (e.g., fixed parameter)"
                        # Near-constant numeric (few unique, tiny range)
            s_num = s.dropna()
            if s_num.nunique() <= 5 and (float(s_num.max()) - float(s_num.min())) <= 0.5:
                return "near-constant reading (low variation)"
            if _zero_fraction(s) != "n/a" and s.eq(0).mean() > 0.95:
                return "flag/status/unused channel (mostly zeros)"
            if _monotonic_hint(s) == "monotonic_increasing":
                return "counter or time-like variable (monotonic)"
        return "unknown"

    lines.append("## Column summary")
    lines.append("")
    lines.append("| column | dtype | nunique | min | max | % zeros | monotonic | const/low-card | possible role (hypothesis) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|")

    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        nun = int(s.dropna().nunique())

        if pd.api.types.is_numeric_dtype(s):
            s_num = s.dropna()
            mn = f"{s_num.min():.4g}" if not s_num.empty else ""
            mx = f"{s_num.max():.4g}" if not s_num.empty else ""
            zf = _zero_fraction(s)
            mono = _monotonic_hint(s)
        else:
            mn, mx, zf, mono = "", "", "n/a", "n/a"

        const_hint = _constant_hint(s)
        role = possible_role(col, s)

        lines.append(f"| {col} | {dtype} | {nun} | {mn} | {mx} | {zf} | {mono} | {const_hint} | {role} |")

    lines.append("")
    lines.append("## Notes / next steps")
    lines.append("")
    lines.append("- If a column is monotonic increasing, it is often a counter or timestamp-like field.")
    lines.append("- If a column is constant (or low-cardinality), it may be a fixed sensor reading or a configuration parameter.")
    lines.append("- If a column is mostly zeros, it may be a flag/channel not used in this measurement setup.")
    lines.append("- Definitive physical mapping should be done by comparing with device documentation and checking expected units/ranges.")
    lines.append("")

    return "\n".join(lines)


# ----------------------------
# Save outputs
# ----------------------------
def ensure_dirs(paths: Paths) -> None:
    paths.processed_dir.mkdir(parents=True, exist_ok=True)
    paths.reports_dir.mkdir(parents=True, exist_ok=True)


def save_clean_csv(df: pd.DataFrame, out_path: Path) -> None:
    df.to_csv(out_path, index=False)


def save_report(text: str, out_path: Path) -> None:
    out_path.write_text(text, encoding="utf-8")


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    paths = get_paths()
    ensure_dirs(paths)

    print("BASE_DIR:", paths.base_dir)
    print("RAW_PATH:", paths.raw_path)
    print("Exists:", paths.raw_path.exists())

    df_raw = load_munra_raw(paths.raw_path)
    df = basic_structural_clean(df_raw)

    print("Parsed shape:", df.shape)
    print(df.head())

    # Save processed dataset
    save_clean_csv(df, paths.processed_csv)
    print("Saved clean CSV to:", paths.processed_csv)

    # Save schema report
    report = build_schema_report(df)
    save_report(report, paths.schema_report_md)
    print("Saved schema report to:", paths.schema_report_md)


if __name__ == "__main__":
    main()
