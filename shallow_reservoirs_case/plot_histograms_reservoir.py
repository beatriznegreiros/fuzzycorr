import plotter
from pathlib import Path

dir = Path.cwd()

# Input data
path_A = r"C:/Users/beatr/valitools/raw_data/diamond_experiment.csv"
path_B = r"C:/Users/beatr/valitools/raw_data/diamond_simulation.csv"

histA = plotter.DataPlotter(path_A, 'Histogram: Diamond-shaped', 'Measured bed level change [cm]')
histB = plotter.DataPlotter(path_B, 'Histogram: Diamond-shaped', 'Simulated bed level change [cm]')

outA = str(dir / "results/hist_diamond_raw_meas.png")
outB = str(dir / "results/hist_diamond_raw_sim.png")

histA.make_hist(outA)
histB.make_hist(outB)