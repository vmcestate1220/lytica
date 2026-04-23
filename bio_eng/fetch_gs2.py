"""One-shot fetch for the GS2 structural template (UniProt P14639).

Downloads the SwissProt record via Bio.ExPASy and writes it as FASTA to
``bio_eng/gs2_template.fasta``. Run once to populate the template file.
"""

from __future__ import annotations

from pathlib import Path

from Bio import ExPASy, SeqIO

ACCESSION = "Q43127"
OUT_PATH = Path(__file__).parent / "gs2_template.fasta"


def main() -> None:
    with ExPASy.get_sprot_raw(ACCESSION) as handle:
        record = SeqIO.read(handle, "swiss")

    SeqIO.write([record], OUT_PATH, "fasta")
    print(f"Saved {record.id} ({len(record.seq)} aa) to {OUT_PATH}")
    print(f"  description: {record.description}")
    print(f"  organism:    {record.annotations.get('organism', '?')}")


if __name__ == "__main__":
    main()
