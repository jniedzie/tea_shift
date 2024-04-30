import ROOT

from Logger import info

from shift_paths import crossSections

x_min = 1e-7
x_max = 1e5
y_min = 1e-8
y_max = 1

limits_300m = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (0.7833, 0.3693, 0.5238, 0.7812, 1.1799, 1.7124, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (0.7850, 0.3711, 0.5264, 0.7852, 1.1826, 1.7145,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (0.7701, 0.3707, 0.5210, 0.7715, 1.1559, 1.6719,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (0.7706, 0.3857, 0.5304, 0.7715, 1.1436, 1.6414,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (2.6169, 1.3393, 1.8185, 2.6172, 3.8691, 5.5464,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (19.9356, 10.2024, 13.8531, 19.9375, 29.4741, 42.2517, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", 1e3): (219.6096, 110.7334, 150.7629, 219.7500, 330.1176, 484.6444, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", 1e5): (10681.1, 3757.3, 5814.7, 10687.5, 21508.1, 32413.3,  ),
}

limits_cmsFT = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (2.3700, 0.7028, 1.2359, 2.3672, 4.4997, 7.1772,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (105.0325, 38.0991, 62.0967, 104.8750, 170.9247, 253.0101,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (2153.0055, 1157.9062, 1544.6616, 2148.0000, 3012.7639, 4043.7180,  ),
}

limits_faser = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (2091.3732, 618.9844, 1088.5675, 2085.0000, 4029.7505, 6322.1304,   ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (1267.6198, 375.2500, 659.9277, 1264.0000, 2442.9758, 3832.6968,   ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (6271.5118, 1843.7500, 3258.7891, 4000.0000, 8049.8193, 12131.2783,   ),
}


def get_graph_set(values, colors):
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph.SetLineColor(colors[0])
    exp_graph.SetLineWidth(2)
    exp_graph.SetLineStyle(1)

    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma.SetLineWidth(0)
    exp_graph_1sigma.SetFillColorAlpha(colors[2], 1.0)

    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma.SetLineWidth(0)
    exp_graph_2sigma.SetFillColorAlpha(colors[1], 1.0)

    for i, (name, ctau) in enumerate(values):
        
        scale = crossSections[name]
        limits = values[(name, ctau)]
        
        central_value = limits[3]*scale
        
        exp_graph.SetPoint(i, ctau, central_value)

        exp_graph_1sigma.SetPoint(i, ctau, central_value)
        exp_graph_1sigma.SetPointError(i, 0, 0, (limits[3] - limits[2])*scale, (limits[4] - limits[3])*scale)

        exp_graph_2sigma.SetPoint(i, ctau, central_value)
        exp_graph_2sigma.SetPointError(i, 0, 0, (limits[3] - limits[1])*scale, (limits[5] - limits[3])*scale)


    return exp_graph, exp_graph_1sigma, exp_graph_2sigma

canvas = ROOT.TCanvas("canvas", "", 800, 600)
canvas.cd()
canvas.SetLogx()
canvas.SetLogy()

def draw_graphs(graphs, first):
    graphs[2].Draw("A3" if first else "3same")
    graphs[1].Draw("3same")
    graphs[0].Draw("Lsame")

    if not first:
        return

    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    primitives = canvas.GetListOfPrimitives()
    first_graph = primitives.At(0)
    
    first_graph.GetXaxis().SetTitleSize(0.05)
    first_graph.GetYaxis().SetTitleSize(0.05)
    first_graph.GetXaxis().SetLabelSize(0.04)
    first_graph.GetYaxis().SetLabelSize(0.04)
    first_graph.GetXaxis().SetTitleOffset(1.1)
    first_graph.GetYaxis().SetTitleOffset(1.1)
    first_graph.GetXaxis().SetTitle("c#tau [m]")
    first_graph.GetYaxis().SetTitle("#sigma_{pp #rightarrow Z' #rightarrow h_{D} #rightarrow #mu #mu} [pb]")

    first_graph.GetXaxis().SetLimits(x_min, x_max)
    
    first_graph.SetMinimum(y_min)
    first_graph.SetMaximum(y_max)
    
def create_shaded_colors(base_color, num_shades=3, min_scale=0.3):
    r_base, g_base, b_base = base_color
    scales = [min_scale + i * (1 - min_scale) / (num_shades - 1) for i in range(num_shades)]

    color_indices = []
    for scale in scales:
        r, g, b = r_base * scale, g_base * scale, b_base * scale
        
        info(f"Adding color: {r}, {g}, {b}")
        
        color_index = ROOT.TColor.GetColor(r, g, b)
        color_indices.append(color_index)

    return color_indices

def main():
    ROOT.gROOT.SetBatch(True)
    
    colors_300m = create_shaded_colors((0, 0, 1), 3, 0.5)
    colors_cmsFT = create_shaded_colors((1, 0, 0), 3, 0.5)
    colors_faser = create_shaded_colors((0, 1, 0), 3, 0.5)
    
    graphs_300m = get_graph_set(limits_300m, colors_300m)
    graphs_cmsFT = get_graph_set(limits_cmsFT, colors_cmsFT)
    graphs_faser = get_graph_set(limits_faser, colors_faser)

    draw_graphs(graphs_300m, first=True)
    draw_graphs(graphs_faser, first=False)
    draw_graphs(graphs_cmsFT, first=False)
    
    
    
    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.AddEntry(graphs_300m[1], "SHIFT@300m", "F")
    legend.AddEntry(graphs_cmsFT[1], "FT@CMS", "F")
    legend.AddEntry(graphs_faser[1], "FASER", "F")
    legend.Draw()

    canvas.Update()
    canvas.SaveAs("../plots/limits_cross_section.pdf")
    canvas.SaveAs("../plots/limits_cross_section.C")
    

if __name__ == "__main__":
    main()
