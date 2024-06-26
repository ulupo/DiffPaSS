# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/msa_parsing.ipynb.

# %% auto 0
__all__ = ['SeqRecord', 'SeqRecords', 'deletekeys', 'translation', 'read_sequence', 'remove_insertions', 'read_msa']

# %% ../nbs/msa_parsing.ipynb 3
import string
import itertools

from Bio import SeqIO

SeqRecord = tuple[str, str]
SeqRecords = list[SeqRecord]

deletekeys = dict.fromkeys(string.ascii_lowercase)
deletekeys["."] = None
deletekeys["*"] = None
translation = str.maketrans(deletekeys)


def read_sequence(filename: str) -> SeqRecord:
    """Reads the first (reference) sequences from a fasta or MSA file."""
    record = next(SeqIO.parse(filename, "fasta"))
    return record.description, str(record.seq)


def remove_insertions(sequence: str) -> str:
    """Removes any insertions into the sequence. Needed to load aligned sequences in an MSA."""
    return sequence.translate(translation)


def read_msa(filename: str, nseq: int) -> SeqRecords:
    """Reads the first nseq sequences from an MSA file, automatically removes insertions."""
    if nseq == -1:
        nseq = len([elem.id for elem in SeqIO.parse(filename, "fasta")])
    return [
        (record.description, remove_insertions(str(record.seq)))
        for record in itertools.islice(SeqIO.parse(filename, "fasta"), nseq)
    ]
