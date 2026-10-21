# Full-year test of an already saved model (config + data come from the model folder); run from smart-home-energy-trading-with-DRL/
# Usage: python ../ket_qua/run_test.py <name>   (loads saved_nets/<name>)
import os, sys, time
sys.path.insert(0, os.getcwd())
import matplotlib
matplotlib.use("Agg")
import torch
import HEMS

name = sys.argv[1]
torch.set_num_threads(1)
m = HEMS.HEMS(load=True, path="saved_nets/" + name)
print("PROPERTIES battery", m.battery, "max_en", m.max_en, "eff", m.eff, "price_coefs", m.price_coefs,
      "SMP levels", m.df["SMP"].nunique(), "epsilon", m.epsilon, flush=True)
t = time.time()
r = m.test()
print("TEST_SECONDS", round(time.time() - t, 1))
print("RAW results [sRL, baseline1_alt, baseline2_nobatt, no_pv_no_batt]:", [float(x) for x in r])
