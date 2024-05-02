import ROOT

from Logger import info, error

from shift_paths import crossSections

x_min = 1e-7
x_max = 1e5
y_min = 1e-6
y_max = 1

alpha = 0.5

# limits_300m = {
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (24.7813, 8.4111, 13.7723, 24.7500, 45.4675, 75.0284, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (24.8535, 8.4536, 13.8419, 24.8750, 45.6971, 75.4073, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (24.0740, 8.1987, 13.4245, 24.1250, 44.3193, 73.1337, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (0.2352, 0.0797, 0.1304, 0.2344, 0.4324, 0.7105, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (0.0791, 0.0266, 0.0438, 0.0791, 0.1453, 0.2398, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (0.0599, 0.0202, 0.0333, 0.0601, 0.1103, 0.1821, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", 1e3): (0.0669, 0.0225, 0.0370, 0.0669, 0.1245, 0.2028, ),
#     ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", 1e5): (0.3247, 0.0823, 0.1485, 0.3242, 0.6525, 0.9833, ),
# }

limits_cmsFT = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (2.3700, 0.7028, 1.2359, 2.3672, 4.4997, 7.1772,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (105.0325, 38.0991, 62.0967, 104.8750, 170.9247, 253.0101,  ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (2153.0055, 1157.9062, 1544.6616, 2148.0000, 3012.7639, 4043.7180,  ),
}

limits_atlasFT = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (0.0583, 0.0173, 0.0303, 0.0581, 0.1118, 0.1762, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (2.3700, 0.7028, 1.2359, 2.3672, 4.4997, 7.1772, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (105.0325, 38.0991, 62.0967, 104.8750, 170.9247, 253.0101,   ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (2153.0055, 1157.9062, 1544.6616, 2148.0000, 3012.7639, 4043.7180,   ),
}

limits_faserFT = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (2091.3732, 618.9844, 1088.5675, 2085.0000, 4029.7505, 6322.1304,   ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (1267.6198, 375.2500, 659.9277, 1264.0000, 2442.9758, 3832.6968,   ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (6271.5118, 1843.7500, 3258.7891, 4000.0000, 8049.8193, 12131.2783,   ),
}


limits_atlasCollider = {
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", 1e-7): (18.2027, 9.8752, 13.1872, 18.1875, 25.2921, 33.6162, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", 1e-3): (18.2314, 9.9092, 13.1673, 18.2500, 25.3063, 33.6791, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", 1e-1): (28.9119, 15.7122, 20.8783, 28.9375, 40.1261, 53.4021, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", 1e-0): (1.4978, 0.8123, 1.0794, 1.4961, 2.0746, 2.7609, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", 1e1): (1.3651, 0.7402, 0.9836, 1.3633, 1.9013, 2.5237, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", 1e2): (1.2926, 0.6919, 0.9220, 1.2930, 1.8238, 2.4908, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", 1e3): (1.6088, 0.7607, 1.0591, 1.6094, 2.7513, 4.8771, ),
    ("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", 1e5): (0.2952, 0.1302, 0.1855, 0.2949, 0.4901, 0.7411, ),
}







def get_graph_set(values, colors, lumi_scale = 1.0):
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph.SetLineColor(colors[0])
    exp_graph.SetLineWidth(2)
    exp_graph.SetLineStyle(1)

    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma.SetLineWidth(0)
    exp_graph_1sigma.SetFillColorAlpha(colors[2], alpha)

    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma.SetLineWidth(0)
    exp_graph_2sigma.SetFillColorAlpha(colors[1], alpha)

    for i, (name, ctau) in enumerate(values):
        
        scale = crossSections[name]
        limits = values[(name, ctau)]
        
        limits = [limit*lumi_scale for limit in limits]
        
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

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')  # Remove the "#" if present
    if len(hex_str) != 6:
        error("Hexadecimal string must be 6 characters long.")

    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return (r, g, b)

def create_shaded_colors(base_color, num_shades=3, min_scale=0.3):
    if isinstance(base_color, str):
        base_color = hex_to_rgb(base_color)

    r_base, g_base, b_base = base_color
    scales = [min_scale + i * (1 - min_scale) / (num_shades - 1) for i in range(num_shades)]

    color_indices = []
    for scale in scales:
        r, g, b = r_base * scale, g_base * scale, b_base * scale
        color_index = ROOT.TColor.GetColor(r, g, b)
        color_indices.append(color_index)

    return color_indices

def read_limits(path):
    limits = {}
    with open(path, "r") as limits_file:
        for line in limits_file:
            if not line.strip():
                continue
            parts = line.split(":")
            name = parts[0].strip()
            values = parts[1].replace("[", "").replace("]", "").split(",")
            values = [float(value.replace("\'", "")) for value in values]
            
            ctau = float(name.split("_")[-1].replace("tau-", "").replace("em", "e-"))
            limits[(name, ctau)] = values
    return limits

def main():
    ROOT.gROOT.SetBatch(True)
    
    # #F23374, #55699D, #517354
    
    colors_300m = create_shaded_colors("#33F244", 3, 0.5)
    # colors_cmsFT = create_shaded_colors("#F2BC33", 3, 0.5)
    # colors_faserFT = create_shaded_colors("#3366F2", 3, 0.5)
    # colors_atlasFT = create_shaded_colors("#F23374", 3, 0.5)
    colors_atlasCollider = create_shaded_colors("#55699D", 3, 0.5)
    
    limits_300m = read_limits("../datacards/limits_mass_shift300m.txt")
    
    graphs_300m = get_graph_set(limits_300m, colors_300m)
    # graphs_atlasFT = get_graph_set(limits_atlasFT, colors_atlasFT)
    # graphs_faserFT = get_graph_set(limits_faserFT, colors_faserFT)
    graphs_atlasCollider = get_graph_set(limits_atlasCollider, colors_atlasCollider)
    
    draw_graphs(graphs_300m, first=True)
    # draw_graphs(graphs_faserFT, first=False)
    # draw_graphs(graphs_atlasFT, first=False)
    draw_graphs(graphs_atlasCollider, first=False)
    
        
    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.AddEntry(graphs_300m[1], "SHIFT@300m", "F")
    # legend.AddEntry(graphs_faserFT[1], "FT-FASER", "F")
    # legend.AddEntry(graphs_atlasFT[1], "FT@ATLAS", "F")
    legend.AddEntry(graphs_atlasCollider[1], "Collider@ATLAS", "F")
    legend.Draw()

    canvas.Update()
    canvas.SaveAs("../plots/limits_cross_section.pdf")
    canvas.SaveAs("../plots/limits_cross_section.C")
    

if __name__ == "__main__":
    main()
