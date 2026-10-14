# Research GIS: Source in Git, static publication output in Drive

Version 1.0 — October 2026. For academic research visualizations (including Rupesh and Binay), **Colab is an execution option, not the sole authority**.

1. Preserve private research source in Google Drive with stable file IDs, source rows and provenance. Keep human-entered values unchanged.
2. Author reusable Python source `.py` for deterministic data processing, GIS analyses, QA and static Matplotlib/Cartopy/GeoPandas publication figures. Use `.ipynb` only when a step-by-step notebook, Earth Engine authentication, or researcher interactive exploration is genuinely beneficial.
3. Git is the code authority. Keep source, dependency versions, tests, manifests and image-figure generation recipe in each researcher's module. Use commits, branches and milestone tags per the R&D Git/Drive standard; avoid drive-file-name-only versioning.
4. Drive is the output authority: original source, full run logs, data tables, image PNG, optional vector SVG/PDF (when requested), and scientific approval. Every Git manifest must link its Drive output and input IDs and include unresolved QA.
5. QA: verify source hashes/row counts/CRS, source-vs-boundary assignment, figure dimensions and readable legends/labels, publication permissions, and at least one raster output visual inspection. Do not claim official/certified boundaries without official source evidence.
6. The same Python code may execute in an available managed Python runtime, a local workstation or Google Colab. No need to run Colab repeatedly for simple static maps. Google Earth Engine still requires its own credential/runtime when using its imagery products.
7. Do not put private GPS point coordinates, field data, personal data, or complete output-bearing notebooks with embedded private data into public Git. Keep only public-safe source and synthetic tests.
8. Freeze only approved milestones. Candidate figures are preview/review artifacts, even when render and automated tests pass. Do not increment A9 Local/Main sequences for routine Git code commits; retain Drive governance for scientific evidence and source originals.

Terminology: **map frame** (ArcGIS Pro map frame), **extent**, **map scale**, **buffer** (distance from geometry), **square bounding envelope/extent**, **definition query** (filter features), **graduated colors** (polygon symbology), **unique values** (category symbols), **labeling** (dynamic text), **annotation** (stored labels), **label expression**, **halo**, **callout**, **leader line**, **map surrounds** (legend, north arrow, scale bar), **layout**, **inset map**, **graticule/grid**, **feature-linked annotation**, **spatial join**, and **point-in-polygon**.
