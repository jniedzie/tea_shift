import ROOT

from Logger import info, warn, error

from shift_paths import crossSections

x_min = 1e-7
x_max = 1e5
y_min = 1e-6
y_max = 1

alpha = 0.5
show_error_bands = False

# nice colors: #F23374, #55699D, #517354 #33F244 #F2BC33 #3366F2

variants = {
    "cms": ("#F23374", "CMS (Collider Mode)"),
    # "shift80m": ("#55699D", "Shift (80 m)"),
    "shift120m": ("#33F244", "Shift (120 m)"),
    # "shift200m": ("#517354", "Shift (200 m)"),
    "shift250m": ("#000000", "Shift (250 m)"),
    # "shift300m": ("#F2BC33", "Shift (300 m)"),
    # "shift350m": ("#FF0000", "Shift (350 m)"),
    # "shift400m": ("#3366F2", "Shift (400 m)"),
    # "cmsFT": ("#3366F2", "FT@CMS (a.k.a. Shift 0 m)"),
    # "faser": ("#517354", "FASER (Collider Mode, d=480 m)"),
    
    "shift250mpythia_mZprime-100_mDH-20_mDQ-10_tau-1e1": ((20, ROOT.kBlack), "100/20/10 (250)"),
    "cmspythiaCollider_mZprime-100_mDH-20_mDQ-10_tau-1e1": ((20, ROOT.kRed), "100/20/10 (CMS)"),
    
    "shift120mpythia_mZprime-40_mDH-20_mDQ-1_tau-1em3": ((21, ROOT.kGreen), "40/20/1 (120)"),
    "cmspythiaCollider_mZprime-40_mDH-20_mDQ-1_tau-1em3": ((21, ROOT.kRed), "40/20/1 (CMS)"),
    # "shift300mpythia_mZprime-100_mDH-15_mDQ-1_tau-1e1": ((21, ROOT.kBlue), "m_{D} = 15 GeV"),
    # "shift300mpythia_mZprime-100_mDH-40_mDQ-1_tau-1e1": ((21, ROOT.kGreen+1), "m_{D} = 40 GeV"),
    # "shift300mpythia_mZprime-100_mDH-60_mDQ-1_tau-1e1": ((21, ROOT.kCyan), "m_{D} = 60 GeV"),
    # "shift300mpythia_mZprime-100_mDH-20_mDQ-2_tau-1e1": ((22, ROOT.kRed), "m_{q} = 2 GeV"),
    # "shift300mpythia_mZprime-100_mDH-20_mDQ-5_tau-1e1": ((22, ROOT.kOrange), "m_{q} = 5 GeV"),
}


def get_graph_set(values, colors, marker_style=-1, lumi_scale = 1.0):
    
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    
    if marker_style == -1:
        exp_graph.SetLineColor(colors[1] if show_error_bands else colors[0])
        exp_graph.SetLineWidth(2)
        exp_graph.SetLineStyle(1)
        
        exp_graph_1sigma.SetLineWidth(0)
        exp_graph_1sigma.SetFillColorAlpha(colors[2], alpha)

        exp_graph_2sigma.SetLineWidth(0)
        exp_graph_2sigma.SetFillColorAlpha(colors[1], alpha)
    else:
        exp_graph.SetMarkerStyle(marker_style)
        exp_graph.SetMarkerColor(colors)
        
    for i, (name, ctau) in enumerate(values):
        
        key = name if name in crossSections else name.replace("Collider", "")
        
        scale = crossSections[key]
        limits = values[(name, ctau)]
        
        limits = [limit*lumi_scale for limit in limits]
        
        if len(limits) != 6:
            warn(f"Expected 6 values, got {len(limits)} for {name}")
            limits = [999999] * 6
        
        central_value = limits[3]*scale
        
        exp_graph.SetPoint(i, ctau, central_value)

        if marker_style == -1:
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
    
    one_point = graphs[0].GetN() == 1
    
    if one_point:
        graphs[0].Draw("AP" if first else "Psame")
    elif show_error_bands:
        graphs[2].Draw("A3" if first else "3same")
        graphs[1].Draw("3same")
        graphs[0].Draw("Lsame")
    else:
        graphs[0].Draw("AL" if first else "Lsame")

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
    try:
        with open(path, "r") as limits_file:
            for line in limits_file:
                if not line.strip():
                    continue
                parts = line.split(":")
                name = parts[0].strip()
                values = parts[1].replace("[", "").replace("]", "").split(",")
                try:
                    values = [float(value.replace("\'", "")) for value in values]
                except ValueError:
                    warn(f"Couldn't convert some values for: {path}")
                    continue
                
                ctau = float(name.split("_")[-1].replace("tau-", "").replace("em", "e-"))
                limits[(name, ctau)] = values
    except FileNotFoundError:
        error(f"File {path} not found.")
    
    return limits

def main():
    ROOT.gROOT.SetBatch(True)
    
    legend = ROOT.TLegend(0.20, 0.45, 0.45, 0.85)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    
    first = True
    
    graphs = {}
    
    for variant, params in variants.items():
        
        try:
            color, title = params
            colors = create_shaded_colors(color, 3, 0.3 if show_error_bands else 1.0)
            marker_style = -1
        except ValueError:
            (marker_style, colors), title = params
        
        
        limits = read_limits(f"../datacards/limits_mass_{variant}.txt")
        
        if not limits:
            continue

        graphs[variant] = get_graph_set(limits, colors, marker_style)
        draw_graphs(graphs[variant], first=first)
        legend.AddEntry(graphs[variant][1] if show_error_bands else graphs[variant][0], title, "F" if show_error_bands else "L" if marker_style == -1 else "P")
        
        first = False
    
    legend.Draw()
    canvas.Update()
    canvas.SaveAs("../plots/limits_cross_section.pdf")
    canvas.SaveAs("../plots/limits_cross_section.C")
    

if __name__ == "__main__":
    main()
