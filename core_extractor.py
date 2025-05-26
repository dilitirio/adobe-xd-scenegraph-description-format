import zipfile
import json
import os
import argparse
from pathlib import Path
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_xd_data(xd_path: str, output_dir: str) -> dict:
    """
    Extracts data from an .xd file.

    Args:
        xd_path (str): Path to the input .xd file.
        output_dir (str): Path to the output directory.

    Returns:
        dict: A dictionary with the status and result message.
    """
    xd_file = Path(xd_path)
    output_path = Path(output_dir)

    if not xd_file.is_file() or xd_file.suffix != '.xd':
        msg = f"Error: The specified path is not a valid .xd file: {xd_path}"
        logging.error(msg)
        return {"status": "error", "message": msg}

    try:
        output_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Output directory created: {output_path}")
    except OSError as e:
        msg = f"Error creating output directory: {e}"
        logging.error(msg)
        return {"status": "error", "message": msg}

    all_agc_data = {}
    extracted_files = []
    key_files_to_extract = ['manifest', 'interactions.json', 'metadata.xml', 'mimetype']

    logging.info(f"Starting extraction from {xd_file.name}")
    try:
        with zipfile.ZipFile(xd_file, 'r') as archive:
            for item in archive.infolist():
                # Find and consolidate all .agc files
                if item.filename.endswith('graphicContent.agc'):
                    logging.info(f"Found .agc file: {item.filename}")
                    try:
                        content = archive.read(item.filename)
                        all_agc_data[item.filename] = json.loads(content.decode('utf-8'))
                        extracted_files.append(item.filename)
                    except Exception as e:
                        logging.warning(f"Could not read or parse {item.filename}: {e}")

                # Extract other key files
                elif Path(item.filename).name in key_files_to_extract:
                    archive.extract(item, path=output_path)
                    extracted_files.append(item.filename)
                    logging.info(f"Extracted key file: {item.filename}")

        # Save the consolidated .agc data
        if all_agc_data:
            agc_output_file = output_path / 'all_graphic_content.json'
            with open(agc_output_file, 'w', encoding='utf-8') as f:
                json.dump(all_agc_data, f, indent=4)
            logging.info(f"All .agc data saved to: {agc_output_file}")
        else:
            logging.warning("No graphicContent.agc files were found in the archive.")

        # Save extraction metadata
        info = {
            "source_file": str(xd_file),
            "output_directory": str(output_path),
            "agc_files_found": list(all_agc_data.keys()),
            "other_files_extracted": [f for f in extracted_files if not f.endswith('.agc')]
        }
        info_output_file = output_path / '_extraction_info.json'
        with open(info_output_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4)

        msg = f"Extraction completed successfully. Files saved in {output_path}"
        logging.info(msg)
        return {"status": "success", "message": msg}

    except zipfile.BadZipFile:
        msg = "Error: File is corrupted or not a valid ZIP archive."
        logging.error(msg)
        return {"status": "error", "message": msg}
    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        logging.error(msg)
        return {"status": "error", "message": msg}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Adobe XD Scenegraph Extractor (CLI)")
    parser.add_argument("-i", "--input", required=True, help="Path to the input .xd file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory.")

    args = parser.parse_args()

    extract_xd_data(args.input, args.output)