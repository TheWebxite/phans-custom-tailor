"""Shrink deck PDFs so clients can open them on a phone: recompress every image as JPEG at a sensible resolution.
Run: /Users/hengzhexin/anaconda3/bin/python3 pitch/shrink_pdf.py file1.pdf file2.pdf ...  (rewrites in place)"""
import os, sys, pymupdf
for f in sys.argv[1:]:
  before = os.path.getsize(f)
  d = pymupdf.open(f)
  d.rewrite_images(dpi_threshold=130, dpi_target=120, quality=72, lossy=True, lossless=True, bitonal=False, color=True, gray=True)
  tmp = f + '.tmp'; d.save(tmp, garbage=4, deflate=True, clean=True); d.close(); os.replace(tmp, f)
  print(f'{f}: {before/1e6:.1f} MB -> {os.path.getsize(f)/1e6:.2f} MB')
