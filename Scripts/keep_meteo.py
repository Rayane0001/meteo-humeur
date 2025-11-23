#!/usr/bin/env python3
"""
keep_meteo.py

Allège un ou plusieurs fichiers CSV en ne conservant que les colonnes
contenant certaines sous-chaînes (insensible à la casse).

Usage (exemples) :
  - Traiter un seul fichier (défaut) :
        python keep_meteo.py
    (par défaut lit CSVs/meteo_filtered.csv et écrit CSVs/meteo_filtered_light/meteo_filtered_light.csv)

  - Traiter un fichier donné et écrire un fichier de sortie :
        python keep_meteo.py --input path/to/meteo_filtered.csv --output path/to/out.csv

  - Traiter tous les CSV d'un dossier :
        python keep_meteo.py --input path/to/csv_folder --output path/to/output_folder

Comportement :
  - Si --input est un fichier .csv, le script produit un fichier unique (par défaut dans
    <même_dossier>/_light.csv ou là où --output pointe).
  - Si --input est un dossier, le script parcourt tous les .csv et écrit les versions "light"
    dans un dossier de sortie (par défaut CSVs/meteo_filtered_light).
"""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Tokens à rechercher (insensible à la casse)
TOKENS = [
    "date",
    "start_time",
    "end_time",
    "location",
    "weather_category",
    "precip_mm",
    "humidity_pct",
    "app_temp_c",     # app_temp_C sera matché grâce à lower()
    "visibility_m",
    "wind_speed_kmh",
    "gusts_kmh",
    "cloud_pct",
    "special_event",
]


def find_and_order_columns(columns, tokens):
    """
    Retourne la liste des colonnes à garder, ordonnées selon l'ordre des tokens.
    Pour chaque token, on ajoute les colonnes qui contiennent ce token (insensible à la casse),
    en préservant l'ordre d'apparition dans le CSV et en évitant les doublons.
    """
    cols = list(columns)
    kept = []
    cols_lower = [c.lower() for c in cols]

    for token in tokens:
        t = token.lower()
        for idx, col_lower in enumerate(cols_lower):
            if t in col_lower and cols[idx] not in kept:
                kept.append(cols[idx])
    return kept


def read_csv_robust(path: Path):
    """Essaie utf-8 puis latin1."""
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1", low_memory=False)


def process_single_file(src_path: Path, dst_path: Path):
    df = read_csv_robust(src_path)

    if df.empty:
        print(f"[SKIP] {src_path.name} — fichier vide")
        return

    kept_cols = find_and_order_columns(df.columns, TOKENS)
    if not kept_cols:
        print(f"[SKIP] {src_path.name} — aucune colonne correspondante trouvée.")
        return

    out_df = df.loc[:, kept_cols]

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(dst_path, index=False, encoding="utf-8")
    missing_tokens = [t for t in TOKENS if not any(t.lower() in c.lower() for c in kept_cols)]
    print(f"[OK]   {src_path.name} -> {dst_path.name} ; colonnes conservées: {len(kept_cols)}"
          + (f" ; tokens manquants: {', '.join(missing_tokens)}" if missing_tokens else ""))


def process_folder(src_dir: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    csv_files = sorted([p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() == ".csv"])
    if not csv_files:
        print(f"Aucun fichier .csv trouvé dans {src_dir}")
        return
    for f in csv_files:
        out_path = dst_dir / f"{f.stem}_light{f.suffix}"
        process_single_file(f, out_path)


def main(args):
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    # Comportement par défaut si l'utilisateur n'a rien fourni :
    # - input par défaut : CSVs/meteo_filtered.csv
    # - output par défaut pour un fichier : same_folder/<stem>_light.csv
    # - output par défaut pour un dossier : CSVs/meteo_filtered_light
    if not input_path.exists():
        # attempt relatif depuis le répertoire courant — laisse l'erreur claire
        raise SystemExit(f"Chemin d'entrée invalide: {input_path}")

    if input_path.is_file():
        # déterminer output file
        if output_path:
            # si output donné et est un dossier -> placer dedans avec nom modifié
            if output_path.exists() and output_path.is_dir():
                out_file = output_path / f"{input_path.stem}_light{input_path.suffix}"
            else:
                # si output semble être un chemin fichier (ou non existant mais contenant .csv) on l'utilise tel quel
                if output_path.suffix.lower() == ".csv":
                    out_file = output_path
                else:
                    # output_path n'a pas d'extension -> traité comme dossier cible
                    out_file = output_path / f"{input_path.stem}_light{input_path.suffix}"
        else:
            # output non fourni -> écrire dans le même dossier avec suffixe _light
            out_file = input_path.parent / f"{input_path.stem}_light{input_path.suffix}"

        process_single_file(input_path, out_file)
    elif input_path.is_dir():
        # input est dossier
        if output_path:
            if output_path.suffix.lower() == ".csv":
                raise SystemExit("Quand --input est un dossier, --output doit être un dossier (pas un fichier .csv).")
            out_dir = output_path
        else:
            # output par défaut pour dossier
            out_dir = Path("CSVs/meteo_filtered_light")
        process_folder(input_path, out_dir)
    else:
        raise SystemExit(f"Chemin d'entrée non pris en charge: {input_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Alléger CSV météo en conservant un sous-ensemble de colonnes identifiables par tokens."
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path("CSVs/meteo_filtered.csv"),
        help="Fichier CSV ou dossier contenant CSVs (par défaut CSVs/meteo_filtered.csv)."
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Fichier de sortie (.csv) ou dossier de sortie. Si absent, comportement par défaut expliqué dans la docstring."
    )

    args = parser.parse_args()
    try:
        main(args)
    except SystemExit as e:
        print(e)
        sys.exit(1)
