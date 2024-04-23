import ROOT
from collections import OrderedDict

from shift_paths import luminosity, crossSections, nGenEvents, base_path, processes, skim


def main():
    ROOT.gROOT.SetBatch(True)

    for process in processes:
        input_path = f"{base_path}/{process}/merged_{skim}.root"
        print(f"Analyzing file: {input_path}")

        scale = luminosity*crossSections[process]
        scale /= nGenEvents[process]

        file = ROOT.TFile(input_path, "READ")
        dir = file.Get("CutFlow")
        keys = dir.GetListOfKeys()
        hist_dict = OrderedDict()

        for key in keys:
            hist = dir.Get(key.GetName())
            hist_dict[key.GetName()] = hist.GetBinContent(1)

        hist_dict = OrderedDict(
            sorted(hist_dict.items(), key=lambda x: int(x[0].split("_")[0])))

        print("CutFlow:")
        for key, value in hist_dict.items():
            print(f"{key:30}: {value:10}\t\t{value*scale:.4f}")


if __name__ == "__main__":
    main()
