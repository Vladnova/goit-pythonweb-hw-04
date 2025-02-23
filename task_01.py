import argparse
import asyncio
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Async file sorter by extension.")
    parser.add_argument("source", type=str, nargs='?', help="Path to the source folder")
    parser.add_argument("output", type=str, nargs='?', help="Path to the output folder")
    return parser.parse_args()

async def copy_file(file_path: Path, output_folder: Path):
    ext = file_path.suffix.lstrip(".") or "unknown"
    dest_folder = output_folder / ext
    dest_folder.mkdir(parents=True, exist_ok=True)

    dest_file = dest_folder / file_path.name

    try:
        shutil.copy2(file_path, dest_file)
        logging.info(f"Copied {file_path} -> {dest_file}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for file_path in source_folder.rglob("*"):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))

    if tasks:
        await asyncio.gather(*tasks)

async def main():
    args = parse_args()

    source_path = args.source or input("Enter the path to the source folder: ")
    output_path = args.output or input("Enter the path to the output folder: ")

    source_folder = Path(source_path).resolve()
    output_folder = Path(output_path).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder does not exist or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
