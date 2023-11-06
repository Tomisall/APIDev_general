@echo off
python .\Scripts\setupScript.py
python .\Scripts\AutoHPLCOverlay.py
START overlayedHPLCtrace.png
python .\Scripts\AutoHTEHeatMap.py
@For %%A In (*_HeatMap.png
) Do @Start "" "%%A"
python .\Scripts\AutoHPLCTrendTool.py
@For %%A In (output_*
) Do @Start "" "%%A"
timeout /t 15 /nobreak>nul