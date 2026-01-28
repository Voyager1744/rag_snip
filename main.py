from pathlib import Path

from ingest.parser import parse_snip
from ingest.postprocess import postprocess
import json


def main():
    path_pdf: Path = (Path(__file__).parent / "SP-47-13330-2016.pdf").resolve()
    result = parse_snip(path_pdf)
    result = postprocess(result)
    print(
        json.dumps([p.model_dump() for p in result[:50]], ensure_ascii=False, indent=2)
    )
    print([(p.paragraph, p.page) for p in result])


if __name__ == "__main__":
    main()
