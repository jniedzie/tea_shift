import ROOT
from shift_paths import crossSections


cross_section_limits = {
    # converting ctau to meters
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (0.7833, 0.3693, 0.5238, 0.7812, 1.1799, 1.7124, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (0.7850, 0.3711, 0.5264, 0.7852, 1.1826, 1.7145,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (0.7701, 0.3707, 0.5210, 0.7715, 1.1559, 1.6719,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (0.7706, 0.3857, 0.5304, 0.7715, 1.1436, 1.6414,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (2.6169, 1.3393, 1.8185, 2.6172, 3.8691, 5.5464,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (19.9356, 10.2024, 13.8531, 19.9375, 29.4741, 42.2517, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", 1e3): (219.6096, 110.7334, 150.7629, 219.7500, 330.1176, 484.6444, ),
}


def main():
    ROOT.gROOT.SetBatch(True)
    
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph.SetLineColor(ROOT.kBlack)
    exp_graph.SetLineWidth(2)
    exp_graph.SetLineStyle(2)

    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma.SetLineWidth(0)
    exp_graph_1sigma.SetFillColorAlpha(ROOT.kGreen+1, 1.0)

    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma.SetLineWidth(0)
    exp_graph_2sigma.SetFillColorAlpha(ROOT.kYellow+1, 1.0)

    for i, (name, ctau) in enumerate(cross_section_limits):
        
        scale = crossSections[name]
        limits = cross_section_limits[(name, ctau)]
        
        central_value = limits[3]*scale
        
        exp_graph.SetPoint(i, ctau, central_value)

        exp_graph_1sigma.SetPoint(i, ctau, central_value)
        exp_graph_1sigma.SetPointError(i, 0, 0, (limits[3] - limits[2])*scale, (limits[4] - limits[3])*scale)

        exp_graph_2sigma.SetPoint(i, ctau, central_value)
        exp_graph_2sigma.SetPointError(i, 0, 0, (limits[3] - limits[1])*scale, (limits[5] - limits[3])*scale)

    canvas = ROOT.TCanvas("canvas", "", 800, 600)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()


    exp_graph_2sigma.Draw("A3")
    exp_graph_1sigma.Draw("3same")
    exp_graph.Draw("Lsame")

    exp_graph_2sigma.GetXaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetYaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetXaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetYaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetXaxis().SetTitleOffset(1.1)
    exp_graph_2sigma.GetYaxis().SetTitleOffset(1.1)
    
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    exp_graph_2sigma.GetXaxis().SetTitle("c#tau [m]")
    exp_graph_2sigma.GetYaxis().SetTitle(
        "#sigma_{pp #rightarrow a #rightarrow #mu #mu} [pb]")

    # exp_graph_2sigma.GetXaxis().SetMoreLogLabels()

    # set x and y axes limits
    exp_graph_2sigma.GetXaxis().SetLimits(1e-8, 1e4)
    exp_graph_2sigma.SetMaximum(1)
    exp_graph_2sigma.SetMinimum(1e-8)

    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.AddEntry(exp_graph, "Expected", "L")
    legend.AddEntry(exp_graph_1sigma, "Expected #pm 1 #sigma", "F")
    legend.AddEntry(exp_graph_2sigma, "Expected #pm 2 #sigma", "F")
    legend.Draw()

    tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS} #it{Preliminary}")
    # tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.Draw()

    tex2 = ROOT.TLatex(0.60, 0.92, "#scale[0.8]{pp, 60 fb^{-1} (#sqrt{s_{NN}} = 13 TeV)}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    canvas.Update()
    canvas.SaveAs("../plots/limits_cross_section.pdf")
    canvas.SaveAs("../plots/limits_cross_section.C")
    

if __name__ == "__main__":
    main()
