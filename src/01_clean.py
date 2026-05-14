# src/01_clean.py
import ssl
import urllib.request
from pathlib import Path

from Bio import PDB

# Disable SSL verification for urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context

# Add User-Agent header to avoid 403 Forbidden
opener = urllib.request.build_opener()
opener.addheaders = [("User-agent", "Mozilla/5.0")]
urllib.request.install_opener(opener)

Path("structures").mkdir(exist_ok=True)

# Download
print("Downloading 7T8C.pdb...")
urllib.request.urlretrieve("https://files.rcsb.org/download/7T8C.pdb", "structures/7T8C.pdb")

# Extract 6 chains (A-F) = hexamer, remove HETATM
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("twinkle", "structures/7T8C.pdb")


class HexamerSelect(PDB.Select):
    def accept_chain(self, chain):
        return chain.id in list("ABCDEF")

    def accept_residue(self, residue):
        return residue.id[0] == " "  # exclude HETATM


io = PDB.PDBIO()
io.set_structure(structure)
io.save("structures/twinkle_hex.pdb", HexamerSelect())
print("twinkle_hex.pdb saved.")
