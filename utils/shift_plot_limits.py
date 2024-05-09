import ROOT

from Logger import info, warn, error

from shift_paths import crossSections

# variable = "ctau"
# variable = "mZprime"
variable = "mDH"
# variable = "mDQ"

if variable == "ctau":
    x_min = 1e-7
    x_max = 1e5
    y_min = 1e-6
    y_max = 100
    log_x = True
elif variable == "mZprime":
    x_min = 10
    x_max = 110
    y_min = 1e-6
    y_max = 1
    log_x = False
elif variable == "mDH":
    x_min = 1
    x_max = 50
    y_min = 1e-6
    y_max = 1
    log_x = False
elif variable == "mDQ":
    x_min = 0.005
    x_max = 5
    y_min = 1e-6
    y_max = 1
    log_x = True

alpha = 0.5
show_error_bands = False

# nice colors: #F23374, #55699D, #517354 #33F244 #F2BC33 #3366F2

variants = {
    # 100/20/1/X
    # "cms_mZprime-100_mDH-20_mDQ-1": (-1, 1, ROOT.kRed, "CMS (100/20/1)"),
    # "shift120m_mZprime-100_mDH-20_mDQ-1": (-1, 1, ROOT.kGreen, "Shift@120 (100/20/1)"),
    # "shift250m_mZprime-100_mDH-20_mDQ-1": (-1, 1, ROOT.kBlue, "Shift@250 (100/20/1)"),
    
    # 100/20/10/X
    # "cms_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kRed, "CMS (100/20/10)"),
    # "shift120m_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kGreen+1, "Shift@120 (100/20/10)"),
    # "shift200m_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kBlack, "Shift@200 (100/20/10)"),
    # "shift250m_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kCyan, "Shift@250 (100/20/10)"),
    # "shift300m_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kMagenta, "Shift@300 (100/20/10)"),
    # "shift350m_mZprime-100_mDH-20_mDQ-10": (-1, 2, ROOT.kBlue, "Shift@350 (100/20/10)"),
    
    # 60/5/1/X
    # "cms_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kRed+1, "CMS (60/5/1/X)"),
    # "shift100m_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kBlue, "Shift@100 (60/5/1/X)"),
    # "shift120m_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kGreen, "Shift@120 (60/5/1/X)"),
    # "shift140m_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kGreen+1, "Shift@140 (60/5/1/X)"),
    # "shift160m_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kGreen+1, "Shift@160 (60/5/1/X)"),
    # "shift200m_mZprime-60_mDH-5_mDQ-1": (-1, 1, ROOT.kCyan, "Shift@200 (60/5/1/X)"),
    
    
    # X/20/10/1em1
    # "cms_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, ROOT.kRed, "CMS (100/20/10)"),
    # "shift120m_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, "#33F244", "Shift@120 (100/20/10)"),
    # "shift200m_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, "#55699D", "Shift@200 (100/20/10)"),
    # "shift290m_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, ROOT.kBlue, "Shift@290 (100/20/10)"),
    # "shift300m_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, ROOT.kCyan, "Shift@300 (100/20/10)"),
    # "shift310m_mZprime-100_mDH-20_mDQ-10_tau-1em1": (-1, 1, ROOT.kTeal, "Shift@310 (100/20/10)"),
    
    # X/20/1/1em1
    # "cms_mZprime-110_mDH-20_mDQ-1_tau-1em1": (-1, 1, ROOT.kRed, "CMS (X/20/1/1em1)"),
    # "shift120m_mZprime-110_mDH-20_mDQ-1_tau-1em1": (-1, 1, ROOT.kGreen, "Shift@120 (X/20/1/1em1)"),
    
    # 100/X/1/1em1
    "cms_mZprime-100_mDQ-1_tau-1em1": (-1, 1, ROOT.kRed, "CMS (100/X/1/1em1)"),
    "shift120m_mZprime-100_mDQ-1_tau-1em1": (-1, 1, ROOT.kGreen, "Shift@120 (100/X/1/1em1)"),
    
    # X/5/1/1em1
    # "cms_mDH-5_mDQ-1_ctau-1em1": (-1, 1, ROOT.kRed, "CMS (X/5/1/1em1)"),
    # "shift120m_mDH-5_mDQ-1_ctau-1em1": (-1, 1, ROOT.kGreen, "Shift@120 (X/5/1/1em1)"),
    
    # 60/5/X/1em1
    # "cms_mZprime-60_mDH-5_ctau-1em1": (-1, 1, ROOT.kRed, "CMS (60/5/X/1em1)"),
    # "shift120m_mZprime-60_mDH-5_ctau-1em1": (-1, 1, ROOT.kGreen, "Shift@120 (60/5/X/1em1)"),
}


def get_graph_set(values, colors, marker_style=-1, line_style=-1, lumi_scale = 1.0):
    
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    
    if marker_style == -1:
        exp_graph.SetLineColor(colors[1] if show_error_bands else colors[0])
        exp_graph.SetLineWidth(2)
        exp_graph.SetLineStyle(line_style)
        
        if show_error_bands:
            exp_graph_1sigma.SetLineWidth(0)
            exp_graph_1sigma.SetFillColorAlpha(colors[2], alpha)

            exp_graph_2sigma.SetLineWidth(0)
            exp_graph_2sigma.SetFillColorAlpha(colors[1], alpha)
    else:
        exp_graph.SetMarkerStyle(marker_style)
        exp_graph.SetMarkerColor(colors[0])
        
    for i, (name, x_value) in enumerate(values):
        
        key = name if name in crossSections else name.replace("Collider", "")
        
        scale = crossSections[key]
        limits = values[(name, x_value)]
        
        limits = [limit*lumi_scale for limit in limits]
        
        if len(limits) != 6:
            warn(f"Expected 6 values, got {len(limits)} for {name}")
            limits = [999999] * 6
        
        central_value = limits[3]*scale
        
        exp_graph.SetPoint(i, x_value, central_value)

        if marker_style == -1:
            exp_graph_1sigma.SetPoint(i, x_value, central_value)
            exp_graph_1sigma.SetPointError(i, 0, 0, (limits[3] - limits[2])*scale, (limits[4] - limits[3])*scale)

            exp_graph_2sigma.SetPoint(i, x_value, central_value)
            exp_graph_2sigma.SetPointError(i, 0, 0, (limits[3] - limits[1])*scale, (limits[5] - limits[3])*scale)


    return exp_graph, exp_graph_1sigma, exp_graph_2sigma

canvas = ROOT.TCanvas("canvas", "", 800, 600)
canvas.cd()
canvas.SetLogx(log_x)
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
    
    x_titles = {
        "ctau": "c#tau [m]",
        "mZprime": "m_{Z'} [GeV]",
        "mDH": "m_{D} [GeV]",
        "mDQ": "m_{q} [GeV]",
    }
    
    first_graph.GetXaxis().SetTitleSize(0.05)
    first_graph.GetYaxis().SetTitleSize(0.05)
    first_graph.GetXaxis().SetLabelSize(0.04)
    first_graph.GetYaxis().SetLabelSize(0.04)
    first_graph.GetXaxis().SetTitleOffset(1.1)
    first_graph.GetYaxis().SetTitleOffset(1.1)
    first_graph.GetXaxis().SetTitle(x_titles[variable])
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
                
                if variable == "ctau":
                    x_value = float(name.split("_")[-1].replace("ctau-", "").replace("em", "e-"))
                elif variable == "mZprime":
                    x_value = float(name.split("_")[1].replace("mZprime-", ""))
                elif variable == "mDH":
                    x_value = float(name.split("_")[2].replace("mDH-", ""))
                elif variable == "mDQ":
                    x_value = float(name.split("_")[3].replace("mDQ-", "").replace("p", "."))
                limits[(name, x_value)] = values
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
        
        marker_style, line_style, color, title = params
        
        if isinstance(color, str):
            colors = create_shaded_colors(color, 3, 0.3 if show_error_bands else 1.0)
        else:
            colors = [color]
        
        limits = read_limits(f"../datacards/limits_mass_{variant}.txt")
        
        if not limits:
            continue

        graphs[variant] = get_graph_set(limits, colors, marker_style, line_style)
        draw_graphs(graphs[variant], first=first)
        legend.AddEntry(graphs[variant][1] if show_error_bands else graphs[variant][0], title, "F" if show_error_bands else "L" if marker_style == -1 else "P")
        
        first = False
    
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(f"../plots/limits_cross_section_{variable}.pdf")
    canvas.SaveAs(f"../plots/limits_cross_section_{variable}.C")
    

if __name__ == "__main__":
    main()
