"""명령줄 : python -m mx_host report <측정 CSV>"""
import argparse
import sys

from . import __version__
from .report import build_text_report, load_rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="mx_host", description=f"mx-host-tool {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("report", help="측정 CSV로 텍스트 리포트 만들기")
    rp.add_argument("csv_path")
    rp.add_argument("--out", help="저장할 파일 (없으면 화면 출력)")
    rp.add_argument("--batch", help="이 배치(lot)만 리포트")
    args = p.parse_args(argv)
    if args.cmd == "report":
        rows = load_rows(args.csv_path)
        if args.batch:
            rows = [r for r in rows if r.get("lot") == args.batch]
        text = build_text_report(rows)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            sys.stdout.write(text)
    return 0
