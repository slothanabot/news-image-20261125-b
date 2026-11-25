[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/slothanabot/news-image-20261125-b/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/slothanabot/news-image-20261125-b/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World in One Day — Wednesday 25 November 2026

A make.fun entry for [news-image-20261125](https://make.fun/bounty/news-image-20261125): a program that writes one 1024x1024 image summing up Wednesday 25 November 2026 world news. A lead banner names the day's biggest story — Ukraine sinking a Russian warship off Libya — above a dotted world map with 35 numbered story markers, and the 35 stories grouped by region below: North America, Latin America, Europe, Africa, Middle East, Asia, and Oceania & Pacific.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies the committed `entry.png` to `out/entry.png` (1024x1024 PNG, 132,407 bytes, under the 1 MiB gate). The entrypoint uses only the Python standard library, makes no network calls, and writes byte-identical output on every run.

To redraw the image from scratch:

```sh
python3 render.py
```

`render.py` draws `entry.png` with Pillow and the DejaVu fonts.

## Stories covered

35 stories reported on 25 November 2026, including Ukraine sinking a Russian warship off Libya, Trump awarding Rudy Giuliani the Medal of Freedom and pardoning turkeys Freedom and Feathers, NATO planning early-warning aircraft in Poland, Houthi strikes on Riyadh's tallest tower, Israel killing Hamas's security chief in Gaza, the Sensex dropping 1,484 points, Real Madrid beating PSV 5-1, and England beating Australia in the second T20I.
