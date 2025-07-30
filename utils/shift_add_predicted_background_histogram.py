import ROOT

from Logger import info, error
from shift_paths import base_path, processes, variant


def get_predicted_histogram(input_file):

  hist_initial = input_file.Get("GoodInitialMuonsPair_mass")
  hist_final = input_file.Get("MuonsHittingDetectorPair_mass")

  if hist_initial is None or type(hist_initial) is ROOT.TObject:
    error("Failed to open histogram GoodInitialMuonsPair_mass")
    return

  hist_total_efficiency = hist_final.Clone("hist_total_efficiency")
  hist_total_efficiency.Divide(hist_initial)

  fit_slope = ROOT.TF1("fit_slope", "[0] + [1] * x", 0, 100)
  fit_slope.SetParameter(0, 1e-5)
  fit_slope.FixParameter(1, 0)
  hist_total_efficiency.Fit(fit_slope, "R", "", 0, 100)

  hist_predicted = hist_initial.Clone("PredictedMuonsPair_mass")
  hist_predicted.SetTitle("PredictedMuonsPair_mass")
  hist_predicted.SetName("PredictedMuonsPair_mass")

  for bin in range(1, hist_predicted.GetNbinsX() + 1):
    x_val = hist_predicted.GetBinCenter(bin)
    hist_predicted.SetBinContent(
      bin,
      hist_initial.GetBinContent(bin) * fit_slope.Eval(x_val)
    )
    hist_predicted.SetBinError(
      bin,
      hist_initial.GetBinError(bin) * fit_slope.Eval(x_val)
    )

  return hist_predicted


def get_standard_mass_historam(input_file):
  hist = input_file.Get("MuonsHittingDetectorPair_mass")
  new_hist = hist.Clone("PredictedMuonsPair_mass")
  new_hist.SetTitle("PredictedMuonsPair_mass")
  new_hist.SetName("PredictedMuonsPair_mass")
  return new_hist


def limit_x_range(hist, x_min, x_max):
  for bin in range(1, hist.GetNbinsX() + 1):
    x_val = hist.GetBinCenter(bin)
    if x_val < x_min or x_val > x_max:
      hist.SetBinContent(bin, 0)
      hist.SetBinError(bin, 0)
  return hist


def update_cutflow_histogram(input_file, predicted_hist):
  hist = input_file.Get("cutFlow")
  sum_weights = predicted_hist.Integral()
  hist.SetBinContent(7, sum_weights)
  hist.Write()


def main():
  ROOT.gROOT.SetBatch(True)

  for process in processes:
    print("\n\n")
    file_path = f"{base_path}/{process}/merged_{variant}_histograms.root"
    print(f"Processing file: {file_path}")

    file = ROOT.TFile(file_path, "UPDATE")

    if "qcd" not in process:
      hist_predicted = get_standard_mass_historam(file)
    else:
      hist_predicted = get_predicted_histogram(file)

    hist_predicted = limit_x_range(hist_predicted, 11, 60)
    hist_predicted.Write()

    update_cutflow_histogram(file, hist_predicted)

    file.Close()

  print("\n\n")


if __name__ == "__main__":
  main()
