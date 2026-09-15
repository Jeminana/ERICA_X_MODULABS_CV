"""preview.html → 슬라이드별 PNG (검수용).

사용법:
    python render_preview.py output/preview.html                # output/preview_png/slide01.png ...
    python render_preview.py output/preview.html --pages 3,7    # 일부 장만
    python render_preview.py output/preview.html --out shots --scale 1

필요: Edge 또는 Chrome, pypdfium2 (pip install pypdfium2)
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx_engine import find_browser  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="preview.html을 슬라이드별 PNG로 렌더링")
    ap.add_argument("preview", help="Deck.save()가 만든 preview.html 경로")
    ap.add_argument("--out", help="PNG 저장 폴더 (기본: preview.html 옆 preview_png)")
    ap.add_argument("--scale", type=float, default=0.75, help="1.0 = 1280x720")
    ap.add_argument("--pages", help="1부터 시작하는 장 번호, 쉼표 구분 (예: 1,3,5)")
    args = ap.parse_args()

    src = Path(args.preview).resolve()
    if not src.exists():
        sys.exit(f"파일이 없습니다: {src}")
    out = Path(args.out) if args.out else src.parent / "preview_png"
    out.mkdir(parents=True, exist_ok=True)

    browser = find_browser()
    if not browser:
        sys.exit("Edge/Chrome을 찾지 못했습니다. PPTX_BROWSER 환경변수로 브라우저 경로를 지정하세요.")
    try:
        import pypdfium2 as pdfium
    except ImportError:
        sys.exit("pypdfium2가 필요합니다: pip install pypdfium2")

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        pdf = Path(tmp) / "preview.pdf"
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-first-run",
                        f"--user-data-dir={Path(tmp) / 'profile'}", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", src.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        if not pdf.exists():
            sys.exit("PDF 생성에 실패했습니다.")
        doc = pdfium.PdfDocument(str(pdf))
        pages = [int(p) - 1 for p in args.pages.split(",")] if args.pages else range(len(doc))
        for i in pages:
            path = out / f"slide{i + 1:02d}.png"
            doc[i].render(scale=args.scale).to_pil().save(path)
            print(path)
        doc.close()


if __name__ == "__main__":
    main()
