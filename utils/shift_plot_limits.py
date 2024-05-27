import ROOT
import numpy as np

from Logger import info, warn, error, fatal

from shift_paths import crossSections, base_lumi

histogram_name = "MuonsHittingDetectorPair_mass"
# histogram_name = "PtMuonsHittingDetectorPair_mass"
# histogram_name = "MuonsHittingDetectorPair_massCtauGt1cm"
# histogram_name = "MuonsHittingDetectorSameVertexPair_mass"

# scenario = "HV"
scenario = "DP"

# variable = "ctau"
# variable = "mDarkPhoton"

variable = "2d"
# mode = "shift160"
mode = "cms"

# variable = "mZprime"
# variable = "mDH"
# variable = "mDQ"

y_title = {
    "DP": "#sigma_{pp #rightarrow A' #rightarrow #mu #mu} [pb]",
    "HV": "#sigma_{pp #rightarrow Z' #rightarrow DH #rightarrow #mu #mu} [pb]",
}

suffix = ""

interpolation_precision = 50

if variable == "ctau":
    x_min = 1e-5
    x_max = 1e3
    y_min = 2e-6
    y_max = 1
    
    if "CtauGt1cm" in histogram_name:
        y_min = 1e-8
    
    log_x = True
    log_y = True
    log_z = False
    x_title = "c#tau [m]"
elif variable == "mZprime":
    x_min = 10
    x_max = 110
    y_min = 1e-6
    y_max = 1
    log_x = False
    log_y = True
    log_z = False
    x_title = "m_{Z'} [GeV]"
elif variable == "mDH":
    x_min = 1
    x_max = 50
    y_min = 1e-6
    y_max = 1
    log_x = False
    log_y = True
    log_z = False
    x_title = "m_{D} [GeV]"
elif variable == "mDQ":
    x_min = 0.005
    x_max = 5
    y_min = 1e-6
    y_max = 1
    log_x = True
    log_y = True
    log_z = False
    x_title = "m_{q} [GeV]"
elif variable == "mDarkPhoton":
    x_min = 10
    x_max = 70
    y_min = 5e-6
    y_max = 10
    
    if "CtauGt1cm" in histogram_name:
        y_min = 1e-8
    
    log_x = False
    log_y = True
    log_z = False
    x_title = "m_{A'} [GeV]"
elif variable == "2d":
    # ctau:
    # x_min = 1e-1
    # x_max = 1e3
    
    x_min = -2
    x_max = 3
    
    # mass:
    y_min = 11
    y_max = 70
    
    # cross section:
    # z_min = 2e-6
    # z_max = 1e1
    
    z_min = -6
    z_max = 1
    
    log_x = False
    log_y = False
    log_z = False
    
    x_title = "log_{10}(c#tau [m])"
    y_title = "m_{A'} [GeV]"

legend_pos = (0.165, 0.70, 0.45, 0.88)

alpha = 0.5
show_error_bands = True
show_2sigma = False

cms_label = f"CMS ({base_lumi*1e-6:.0f} fb^{{-1}})"
lhcb_label = f"LHCb ({0.01*base_lumi/25.0*1e-3:.0f} pb^{{-1}})"
shift_label = f"SHIFT ({0.01*base_lumi*1e-6:.2f} fb^{{-1}})"

# nice colors: #F23374, #55699D, #517354 #33F244 #F2BC33 #3366F2

if scenario == "HV":
    variants = {
        # HV: 60/X/1/X
        "cms_pythiaCollider_mZprime-60_mDH-5_mDQ-1_ctau-X": (-1, 1, ROOT.kGray, f"m_{{DH}} = 5 GeV, {cms_label}"),
        "cms_pythiaCollider_mZprime-60_mDH-20_mDQ-1_tau-X": (-1, 2, ROOT.kBlack, f"m_{{DH}} = 20 GeV, {cms_label}"),
        
        "shift160m_pythia_mZprime-60_mDH-5_mDQ-1_ctau-X": (-1, 1, ROOT.kMagenta+1, f"m_{{DH}} = 5 GeV, {shift_label}"),
        "shift160m_pythia_mZprime-60_mDH-20_mDQ-1_tau-X": (-1, 2, ROOT.kRed, f"m_{{DH}} = 20 GeV, {shift_label}"),
    }
    top_title = "m_{Z'} = 60 GeV, m_{DQ} = 1 GeV"

elif scenario == "DP" and variable == "ctau":
    variants = {
        # DP: 30/X
        # "lhcb_pythia_mDarkPhoton-30_ctau-X": (-1, 1, ROOT.Green+1, lhcb_label),
        "cms_pythiaCollider_mDarkPhoton-30_ctau-X": (-1, 1, ROOT.kGray, cms_label),
        "shift160m_pythia_mDarkPhoton-30_ctau-X": (-1, 1, ROOT.kMagenta+1, shift_label),
    }
    top_title = "m_{A'} = 30 GeV"
    
elif scenario == "DP" and variable == "mDarkPhoton":
    variants = {
        # DP: X/1e1
        # "lhcb_pythia_mDarkPhoton-X_ctau-1e1": (-1, 1, ROOT.kGreen+1, lhcb_label),
        "cmsPT_pythiaCollider_mDarkPhoton-X_ctau-1e1": (-1, 1, ROOT.kGreen+1, cms_label),
        "cms_pythiaCollider_mDarkPhoton-X_ctau-1e1": (-1, 1, ROOT.kGray, cms_label),
        "shift160m_pythia_mDarkPhoton-X_ctau-1e1": (-1, 1, ROOT.kMagenta+1, shift_label),
    }
    top_title = "c#tau = 10 m"
elif scenario == "DP" and variable == "2d":
    if mode == "shift160":
        variants = {"shift160m_2d": (-1, -1, -1, "")}
        top_title = shift_label
        suffix = "_shift160"
    elif mode == "cms":
        variants = {"cms_2d": (-1, -1, -1, "")}
        top_title = cms_label
        suffix = "_cms"
    
else:
    fatal(f"Unsupported scenario: {scenario} and variable: {variable} combination.")
    exit()
    
    
def get_graph_set(values, colors, marker_style=-1, line_style=-1, lumi_scale = 1.0):
    
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    
    if marker_style == -1:
        exp_graph.SetLineColor(colors[1] if show_error_bands else colors[0])
        exp_graph.SetLineWidth(2)
        exp_graph.SetLineStyle(line_style)
        
        if show_error_bands:
            # exp_graph_1sigma.SetLineWidth(0)
            exp_graph_1sigma.SetLineStyle(line_style)
            exp_graph_1sigma.SetLineColor(colors[0])
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

def get_2d_graph(values):
    
    log_bins_10 = list(np.logspace(-5, 4, 10, base=10))
    hist = ROOT.TH2D("hist", "", len(log_bins_10)-1, np.array(log_bins_10), 7, 10, 80)
    
    graph = ROOT.TGraph2D()
    graph.SetMarkerSize(2.0)
    graph.SetMarkerStyle(20)
        
    for i, (name, x_value, y_value) in enumerate(values):
        
        key = name if name in crossSections else name.replace("Collider", "")
        
        scale = crossSections[key]
        limits = values[(name, x_value, y_value)]
        
        if len(limits) != 6:
            warn(f"Expected 6 values, got {len(limits)} for {name}")
            limits = [999999] * 6
        
        central_value = limits[3]*scale
        
        if central_value > z_max:
            central_value = z_max*10
        
        graph.SetPoint(i, np.log10(x_value), y_value, np.log10(central_value))
        hist.Fill(np.log10(x_value), y_value, np.log10(central_value))

    return graph, hist

canvas = ROOT.TCanvas("canvas", "", 800, 600)
canvas.cd()
canvas.SetLogx(log_x)
canvas.SetLogy(log_y)
canvas.SetLogz(log_z)

def draw_graphs(graphs, first):
    
    one_point = graphs[0].GetN() == 1
    
    if one_point:
        graphs[0].Draw("AP" if first else "Psame")
    elif show_error_bands:
        if show_2sigma:
            graphs[2].Draw("A3" if first else "3same")
            graphs[1].Draw("3same")
        else:
            graphs[1].Draw("A3" if first else "3same")
        
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
    first_graph.GetXaxis().SetTitle(x_title)
    first_graph.GetYaxis().SetTitle(y_title[scenario])

    first_graph.GetXaxis().SetLimits(x_min, x_max)
    
    first_graph.SetMinimum(y_min)
    first_graph.SetMaximum(y_max)
    

def draw_2d_graphs(graph):
    
    graph.Draw("colz")
    # graph.Draw("pcolz")

    graph.SetNpx(interpolation_precision)
    graph.SetNpy(interpolation_precision)


    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    # primitives = canvas.GetListOfPrimitives()
    # first_graph = primitives.At(0)
    
    graph.SetTitle("")
    
    graph.GetHistogram().GetXaxis().SetNdivisions(505)
    
    graph.GetHistogram().GetXaxis().SetTitle(x_title)
    graph.GetHistogram().GetYaxis().SetTitle(y_title)
    graph.GetHistogram().GetZaxis().SetTitle("log_{10}(#sigma_{pp #rightarrow A' #rightarrow #mu #mu} [pb])")
    
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)
    
    graph.GetXaxis().SetLabelSize(0.04)
    graph.GetYaxis().SetLabelSize(0.04)
    
    graph.GetXaxis().SetTitleOffset(1.1)
    graph.GetYaxis().SetTitleOffset(1.1)
    
    graph.GetHistogram().GetXaxis().SetLimits(x_min, x_max)
    graph.GetHistogram().GetYaxis().SetRangeUser(y_min, y_max)
    
    graph.SetMinimum(z_min)
    graph.SetMaximum(z_max)
    
    ROOT.gPad.SetTheta(90)
    ROOT.gPad.SetPhi(0)
    canvas.Modified()
    canvas.Update()

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
                
                parts = name.split("_")
                
                for part in parts:
                    var = variable
                    
                    if var == "ctau" and "ctau" not in part and "tau" in part:
                        var = "tau"
                    
                    if var not in part:
                        continue
                    
                    x_value = float(part.replace(f"{var}-", "").replace("em", "e-").replace("p", "."))
                    break
                limits[(name, x_value)] = values
    except FileNotFoundError:
        error(f"File {path} not found.")
    
    return limits

def read_2d_limits(path):
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
                
                parts = name.split("_")
                
                x_var = "ctau"
                y_var = "mDarkPhoton"
                
                for part in parts:
                    if "ctau" not in part and "tau" in part:
                        x_var = "tau"
                    
                    if x_var in part:
                        x_value = float(part.replace(f"{x_var}-", "").replace("em", "e-").replace("p", "."))
                    
                    if y_var in part:
                        y_value = float(part.replace(f"{y_var}-", "").replace("em", "e-").replace("p", "."))
                    
                    
                limits[(name, x_value, y_value)] = values
    except FileNotFoundError:
        error(f"File {path} not found.")
    
    return limits

def main():
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    
    legend = ROOT.TLegend(legend_pos[0], legend_pos[1], legend_pos[2], legend_pos[3])
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    
    first = True
    
    graphs = {}
    
    for variant, params in variants.items():
        if variable == "2d":
            limits = read_2d_limits(f"../datacards/limits_{histogram_name}_{variant}.txt")
            
            graph, hist = get_2d_graph(limits)
            draw_2d_graphs(graph)
            # draw_2d_graphs(hist)
            continue
        
        marker_style, line_style, color, title = params
        
        if isinstance(color, str):
            colors = create_shaded_colors(color, 3, 0.3 if show_error_bands else 1.0)
        else:
            color = ROOT.gROOT.GetColor(color)
            colors = [color.GetRed(), color.GetGreen(), color.GetBlue()]
            colors = "#{:02x}{:02x}{:02x}".format(int(colors[0]*255), int(colors[1]*255), int(colors[2]*255))
            colors = create_shaded_colors(colors, 3, 0.3 if show_error_bands else 1.0)
        
        limits = read_limits(f"../datacards/limits_{histogram_name}_{variant}.txt")
        
        if not limits:
            continue

        graphs[variant] = get_graph_set(limits, colors, marker_style, line_style)
        draw_graphs(graphs[variant], first=first)
        legend.AddEntry(graphs[variant][1] if show_error_bands else graphs[variant][0], title, "FL" if show_error_bands else "L" if marker_style == -1 else "P")
        
        first = False
    
    # add a label on top of the pad
    label = ROOT.TLatex()
    label.SetNDC()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    # align to the right
    label.SetTextAlign(31)
    label.DrawLatex(0.90, 0.92, top_title)
    
    legend.Draw()
    canvas.Update()
    output_path = f"../plots/limits_{histogram_name}/"
    ROOT.gSystem.Exec(f"mkdir -p {output_path}")
    
    canvas.SaveAs(f"{output_path}/limits_{scenario}_{variable}{suffix}.pdf")
    
if __name__ == "__main__":
    main()
