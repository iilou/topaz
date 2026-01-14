from decomp import split_and_convert
from clean import clean_markdown
from build_database import add_to_vector_database
from chunk import chunk_md
from pathlib import Path
import os

# TOPIC = "biochemistry"
TOPIC = "biochemistry"
NUM = 1
BASEDIR = Path(__file__).resolve().parent

path_raw = BASEDIR / f"../../data/raw/{TOPIC}_{NUM}.pdf"
path_md = BASEDIR / f"../../data/processed/markdown/{TOPIC}_{NUM}.md"
path_md_clean = BASEDIR / f"../../data/processed/markdown_clean/{TOPIC}_{NUM}.md"
path_json = BASEDIR / f"../../data/processed/chunked/{TOPIC}_{NUM}.json"

path_vector_db = BASEDIR / f"../../data/vector"

def run_pipeline():
    print("STEP 1: Decomposing PDF to Markdown...")
    split_and_convert(path_raw, path_md)

    print("STEP 2: Cleaning Markdown...")
    clean_markdown(path_md, path_md_clean)

    print("STEP 3: Chunking Markdown to JSON...")
    chunk_md(path_md_clean, path_json)

    print("STEP 4: Building Vector Database...")
    add_to_vector_database(path_json, path_vector_db, f"bio", f"bio-{TOPIC}")

    print("Pipeline completed successfully!")
    
# check if files exist
# if os.path.exists(path_raw) and os.path.exists(path_md) and os.path.exists(path_md_clean):
#     run_pipeline()
# else:
#     print("One or more input files are missing. Please check the paths and try again.")

run_pipeline()