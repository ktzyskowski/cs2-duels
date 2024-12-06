import os
import tempfile

import patoolib
import stealth_requests as requests
from tqdm import tqdm

from src.parser.demo_parser import DemoFileParser

BASE_URL = "https://www.hltv.org/download/demo/"


def load_demo_hrefs(path: str):
    hrefs = []
    with open(path, "r") as f:
        for line in f:
            idx, href = line.strip().split(" ")
            hrefs.append(href)
    return hrefs


def download_demo(demo_id: str, outpath: str):
    url = BASE_URL + demo_id

    with tempfile.TemporaryDirectory() as tmpdir:
        # download demo into a temporary file
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with tempfile.NamedTemporaryFile(dir=tmpdir, suffix=".rar") as tmp:
            with open(tmp.name, "wb") as f:
                for chunk in tqdm(r.iter_content(), desc=f"downloading demo {demo_id}"):
                    f.write(chunk)

            # extract RAR archive from temp file
            patoolib.extract_archive(tmp.name, outdir=tmpdir, verbosity=-1)

        # should only be one file inside tmp directory now
        archive = os.path.join(tmpdir, os.listdir(tmpdir)[0])

        # if archive is a directory, it contains multiple demo files
        if os.path.isdir(archive):
            for demo_file in os.listdir(archive):
                parser = DemoFileParser(os.path.join(archive, demo_file))
                if parser.get_map() == "de_dust2":
                    samples = parser.parse()
                    samples.to_csv(os.path.join(outpath, demo_id + ".csv"), index=False)
                    break
        # otherwise, if it is a single demo file, we can parse it
        elif not os.path.isdir(archive):
            parser = DemoFileParser(os.path.join(archive, archive))
            if parser.get_map() == "de_dust2":
                samples = parser.parse()
                samples.to_csv(os.path.join(outpath, demo_id + ".csv"), index=False)


def main():
    # load in IDs of files already saved
    samples_path = "res/samples"
    saved_files = os.listdir(samples_path)
    saved_ids = [filename[:-4] for filename in saved_files]

    # load in IDs of files to download
    demo_hrefs = load_demo_hrefs("res/demos.txt")
    demo_ids = [href.split("/")[-1] for href in demo_hrefs]
    demo_ids = [demo_id for demo_id in demo_ids if demo_id not in saved_ids]

    # set up a temporary directory to hold raw demo files
    for demo_id in demo_ids:
        try:
            download_demo(demo_id, outpath=samples_path)
        except Exception as e:
            print(repr(e))


if __name__ == "__main__":
    main()
