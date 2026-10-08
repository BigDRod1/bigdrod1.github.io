# Risk article: reproducibility
1. `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`
2. `python download_data.py`  (refreshes data/ from Yahoo Finance; the article uses data cut at 2026-09-30)
3. `python analysis.py`       (about 5 min; writes charts/, results/, results.csv)
4. `python make_formula.py && python build_pdf.py`  (formula image; article.pdf via headless Chrome)
