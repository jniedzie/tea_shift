import ROOT
import numpy as np

from Logger import info, warn, error, fatal

from shift_paths import crossSections, base_lumi, collider_cross_section_scale
from shift_paths import signalCrossSectionFixedTargetDP, signalCrossSectionColliderDP
from shift_paths import signalCrossSectionFixedTargetDP_smallCoupling, signalCrossSectionColliderDP_smallCoupling
from shift_paths import signalCrossSectionFixedTargetHV, signalCrossSectionColliderHV

useSmallCoupling = True

histogram_name = "MuonsHittingDetectorPair_mass"
# histogram_name = "PtMuonsHittingDetectorPair_mass"
# histogram_name = "MuonsHittingDetectorPair_massCtauGt1cm"
# histogram_name = "MuonsHittingDetectorSameVertexPair_mass"

scenario = "HV"
# scenario = "DP"

variable = "ctau"
# variable = "mDarkPhoton"

# variable = "2d"
# mode = "shift160"
mode = "cms"
doTheoryOverLimit = True

# variable = "distance"


# variable = "mZprime"
# variable = "mDH"
# variable = "mDQ"

y_title = {
    "DP": "#sigma_{pp #rightarrow A' #rightarrow #mu #mu} [pb]",
    "HV": "#sigma_{pp #rightarrow Z' #rightarrow DH #rightarrow #mu #mu} [pb]",
}

suffix = ""

interpolation_precision = 100
special_legend = None

if variable == "ctau":
    x_min = 1e-2
    x_max = 1e3
    
    if scenario == "DP":
        y_min = 1e-5
        y_max = 1e3
    elif scenario == "HV":
        y_min = 1e-9
        y_max = 1e2
    
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
    y_min = 1e-5
    y_max = 1e5
    
    if "CtauGt1cm" in histogram_name:
        y_min = 1e-8
    
    log_x = False
    log_y = True
    log_z = False
    x_title = "m_{A'} [GeV]"
elif variable == "2d":
    # ctau:
    x_min = -2
    x_max = 3
    
    # mass:
    y_min = 10
    y_max = 70
    
    # cross section:
    z_min = 1e-5 if doTheoryOverLimit else -6
    z_max = 1e2 if doTheoryOverLimit else 1
    
    log_x = False
    log_y = False
    log_z = doTheoryOverLimit
    
    x_title = "log_{10}(c#tau [m])"
    y_title = "m_{A'} [GeV]"
elif variable == "distance":
    x_min = 30
    x_max = 300
    y_min = 9e-6
    y_max = 1e-1
    
    log_x = False
    log_y = True
    log_z = False
    x_title = "d_{SHIFT} [m]"

legend_pos = (0.165, 0.70, 0.45, 0.88)

alpha = 0.5
show_error_bands = True
show_2sigma = False

cms_label = f"CMS ({base_lumi*1e-6:.0f} fb^{{-1}}, #sqrt{{s}} = 13.6 TeV)"
lhcb_label = f"LHCb ({0.01*base_lumi/25.0*1e-3:.0f} pb^{{-1}})"
shift_label = f"SHIFT ({0.01*base_lumi*1e-6:.2f} fb^{{-1}}, #sqrt{{s}} = 113 GeV)"

# nice colors: #F23374, #55699D, #517354 #33F244 #F2BC33 #3366F2

if scenario == "HV":
    variants = {
        # HV: 60/X/1/X
        #                                                   ms  ls band color
        "cms_pythiaCollider_mZprime-60_mDH-5_mDQ-1_ctau-X": (-1, 1, True, ROOT.kGray, f"m_{{DH}} = 5 GeV, {cms_label}"),
        "cms_pythiaCollider_mZprime-60_mDH-20_mDQ-1_tau-X": (-1, 1, True, ROOT.kBlack, f"m_{{DH}} = 20 GeV, {cms_label}"),
        
        "shift160m_pythia_mZprime-60_mDH-5_mDQ-1_ctau-X": (-1, 1, True, ROOT.kMagenta+1, f"m_{{DH}} = 5 GeV, {shift_label}"),
        "shift160m_pythia_mZprime-60_mDH-20_mDQ-1_tau-X": (-1, 1, True, ROOT.kRed, f"m_{{DH}} = 20 GeV, {shift_label}"),
    }
    top_title = "m_{Z'} = 60 GeV, m_{DQ} = 1 GeV"

elif scenario == "DP" and variable == "ctau":
    variants = {
        # DP: 15/X
        #                                              ms  ls band color
        # "lhcb_pythia_mDarkPhoton-15_ctau-X"         : (-1, 1, True, ROOT.Green+1, lhcb_label),
        "cms_pythiaCollider_mDarkPhoton-15_ctau-X"  : (-1, 1, True, ROOT.kGray      , cms_label),
        "shift160m_pythia_mDarkPhoton-15_ctau-X"    : (-1, 1, True, ROOT.kMagenta+1 , shift_label),
    }
    top_title = "m_{A'} = 15 GeV"
    
    legend_pos = (0.2, 0.75, 0.45, 0.88)
    special_legend = ROOT.TLegend(0.2, 0.69, 0.45, 0.75)
    special_legend.SetBorderSize(0)
    special_legend.SetFillStyle(0)
    special_legend.SetTextFont(42)
    special_legend.SetTextSize(0.04)
    
    dummy_graph_dashed = ROOT.TGraph()
    dummy_graph_dashed.SetLineColor(ROOT.kBlack)
    dummy_graph_dashed.SetLineWidth(4)
    dummy_graph_dashed.SetLineStyle(2)
    
    special_legend.AddEntry(dummy_graph_dashed, "Theory prediction", "L")
    
elif scenario == "DP" and variable == "mDarkPhoton":
    variants = {
        # DP: X/1e1
        #                                                  ms  ls band color
        # "lhcb_pythia_mDarkPhoton-X_ctau-1e1"            : (-1, 1, True, ROOT.kGreen+1, lhcb_label),
        # "cmsPT_pythiaCollider_mDarkPhoton-X_ctau-1e1"   : (-1, 1, True, ROOT.kGreen+1, cms_label),
        
        # "cms_pythiaCollider_mDarkPhoton-X_ctau-1e1"     : (-1, 1, True, ROOT.kGray, cms_label),
        # "shift160m_pythia_mDarkPhoton-X_ctau-1e1"       : (-1, 1, True, ROOT.kMagenta+1, shift_label),
        
        "cms_pythiaCollider_mDarkPhoton-X_ctau-1e2"     : (-1, 1, True, ROOT.kGray, cms_label),
        "shift160m_pythia_mDarkPhoton-X_ctau-1e2"       : (-1, 1, True, ROOT.kMagenta+1, shift_label),
    }
    top_title = "c#tau = 10 m"
    
    legend_pos = (0.3, 0.75, 0.45, 0.88)
    special_legend = ROOT.TLegend(0.3, 0.69, 0.45, 0.75)
    special_legend.SetBorderSize(0)
    special_legend.SetFillStyle(0)
    special_legend.SetTextFont(42)
    special_legend.SetTextSize(0.04)
    
    dummy_graph_dashed = ROOT.TGraph()
    dummy_graph_dashed.SetLineColor(ROOT.kBlack)
    dummy_graph_dashed.SetLineWidth(4)
    dummy_graph_dashed.SetLineStyle(2)
    
    special_legend.AddEntry(dummy_graph_dashed, "Theory prediction", "L")
    
elif scenario == "DP" and variable == "2d":
    if mode == "shift160":
        variants = {"shift160m_2d": (-1, -1, -1, "")}
        top_title = shift_label
        suffix = "_shift160"
    elif mode == "cms":
        variants = {"cms_2d": (-1, -1, -1, "")}
        top_title = cms_label
        suffix = "_cms"
elif scenario == "DP" and variable == "distance":
    variants = {
        
        # "_pythia_mDarkPhoton-30_ctau-1e3_distance": (-1, 1, ROOT.kBlue, "m_{DP} = 30 GeV, c#tau = 1 km"),
        
        "_pythia_mDarkPhoton-30_ctau-1em5_distance"             : (-1, 1, True , ROOT.kViolet, "m_{DP} = 30 GeV, c#tau = 10^{-5} m"),
        # "cms_pythiaCollider_mDarkPhoton-30_ctau-1em5_distance"  : (-1, 2, False, ROOT.kViolet, ""),
        
        "_pythia_mDarkPhoton-30_ctau-1e1_distance"              : (-1, 1, True , ROOT.kGreen+1, "m_{DP} = 30 GeV, c#tau = 10 m"),
        # "cms_pythiaCollider_mDarkPhoton-30_ctau-1e1_distance"   : (-1, 2, False, ROOT.kGreen+1, ""),
        
    }
    top_title = shift_label
    
    legend_pos = (0.3, 0.75, 0.45, 0.88)
    
    # special_legend = ROOT.TLegend(0.3, 0.62, 0.45, 0.75)
    # special_legend.SetBorderSize(0)
    # special_legend.SetFillStyle(0)
    # special_legend.SetTextFont(42)
    # special_legend.SetTextSize(0.04)
    
    # dummy_graph_solid = ROOT.TGraph()
    # dummy_graph_solid.SetLineColor(ROOT.kBlack)
    # dummy_graph_solid.SetLineWidth(2)
    # dummy_graph_solid.SetLineStyle(1)
    
    # dummy_graph_dashed = ROOT.TGraph()
    # dummy_graph_dashed.SetLineColor(ROOT.kBlack)
    # dummy_graph_dashed.SetLineWidth(4)
    # dummy_graph_dashed.SetLineStyle(2)
    
    # special_legend.AddEntry(dummy_graph_dashed, cms_label, "L")
    # special_legend.AddEntry(dummy_graph_solid, shift_label, "L")
    
else:
    fatal(f"Unsupported scenario: {scenario} and variable: {variable} combination.")
    exit()
    
    
def get_graph_set(values, colors, show_band, marker_style=-1, line_style=-1, lumi_scale = 1.0):
    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    
    if marker_style == -1:
        exp_graph.SetLineColor(colors[1] if show_band else colors[0])
        exp_graph.SetLineWidth(4 if line_style > 1 else 2)
        exp_graph.SetLineStyle(line_style)
        
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
        if "shift" in key or "cms" in key:
            key  = "_".join(key.split("_")[:-1])
        
        
        
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

def get_2d_graph(values, lumi_scale = 1.0, colliderMode=False):
    
    log_bins_10 = list(np.logspace(-5, 4, 10, base=10))
    hist = ROOT.TH2D("hist", "", len(log_bins_10)-1, np.array(log_bins_10), 7, 10, 80)
    
    graph = ROOT.TGraph2D()
    graph.SetMarkerSize(2.0)
    graph.SetMarkerStyle(20)
    
    theory_points = None
    
    if scenario == "DP" and useSmallCoupling:
        theory_points = signalCrossSectionColliderDP_smallCoupling if colliderMode else signalCrossSectionFixedTargetDP_smallCoupling
    elif scenario == "DP" and not useSmallCoupling:
        theory_points = signalCrossSectionColliderDP if colliderMode else signalCrossSectionFixedTargetDP
    elif scenario == "HV":
        theory_points = signalCrossSectionColliderHV if colliderMode else signalCrossSectionFixedTargetHV
    
    for i, (name, x_value, y_value) in enumerate(values):
        
        key = name if name in crossSections else name.replace("Collider", "")
        if "shift" in key or "cms" in key:
            key  = "_".join(key.split("_")[:-1])
        
        theory_cross_section = theory_points[y_value]
        
        scale = crossSections[key]
        limits = values[(name, x_value, y_value)]
        
        if len(limits) != 6:
            warn(f"Expected 6 values, got {len(limits)} for {name}")
            limits = [999999] * 6
        
        central_value = limits[3]*scale*lumi_scale
        if doTheoryOverLimit:
            central_value = theory_cross_section/central_value
        else:
            central_value = np.log10(central_value)
        
        # if central_value > z_max:
        #     central_value = z_max if doTheoryOverLimit else z_max*10
        
        graph.SetPoint(i, np.log10(x_value), y_value, central_value)
        hist.Fill(np.log10(x_value), y_value, central_value)

    return graph, hist

canvas = ROOT.TCanvas("canvas", "", 800, 600)
canvas.SetLogx(log_x)
canvas.SetLogy(log_y)
canvas.SetLogz(log_z)

canvas_ratio = ROOT.TCanvas("canvas_ratio", "", 800, 600)
canvas_ratio.SetLogx(log_x)
canvas_ratio.SetLogy(log_y)
canvas_ratio.SetLogz(log_z)

def draw_graphs(graphs, first, show_band):
    canvas.cd()
    one_point = graphs[0].GetN() == 1
    
    if one_point:
        graphs[0].Draw("AP" if first else "Psame")
    elif show_band:
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
    canvas.cd()
    # graph.Draw("colz")
    graph.Draw("pcolz")

    graph.SetNpx(interpolation_precision)
    graph.SetNpy(interpolation_precision)


    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    # primitives = canvas.GetListOfPrimitives()
    # first_graph = primitives.At(0)
    
    graph.SetTitle("")
    
    graph.GetHistogram().GetXaxis().SetNdivisions(505)
    
    z_title = "log_{10}(#sigma_{pp #rightarrow A' #rightarrow #mu #mu} [pb])"
    if doTheoryOverLimit:
        z_title = "#sigma_{theory} / #sigma_{limit}"
    
    graph.GetHistogram().GetXaxis().SetTitle(x_title)
    graph.GetHistogram().GetYaxis().SetTitle(y_title)
    graph.GetHistogram().GetZaxis().SetTitle(z_title)
    
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
        isCmsDistance = False
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
                    
                    if var == "distance":
                        var = "shift"
                    
                    if var not in part and "cms" not in part:
                        continue
                    
                    if "cms" in part:
                        isCmsDistance = True
                        break
                    
                    x_value = float(part.replace(f"{var}-", "").replace(f"{var}", "").replace("em", "e-").replace("p", ".").replace("m", ""))
                    break
                
                if isCmsDistance:
                    limits[(name, x_min)] = values
                    limits[(name, x_max)] = values
                    return limits
                else:    
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

def get_theory_line(colliderMode=False, mass=None):
    graph = ROOT.TGraph()
    
    if scenario == "DP" and useSmallCoupling:
        points = signalCrossSectionColliderDP_smallCoupling if colliderMode else signalCrossSectionFixedTargetDP_smallCoupling
    elif scenario == "DP" and not useSmallCoupling:
        points = signalCrossSectionColliderDP if colliderMode else signalCrossSectionFixedTargetDP
    elif scenario == "HV":
        points = signalCrossSectionColliderHV if colliderMode else signalCrossSectionFixedTargetHV
    
    if mass:
        print(f"Setting theory value: {points[mass]}")
        graph.SetPoint(0, x_min, points[mass])
        graph.SetPoint(1, x_max, points[mass])
        return graph
    
    for i, (mass, cross_section) in enumerate(points.items()):
        graph.SetPoint(i, mass, cross_section)
    return graph

def get_mass_from_name(name, variable_name = "mDarkPhoton"):
    parts = name.split("_")
    for part in parts:
        if variable_name in part:
            return float(part.replace(f"{variable_name}-", "").replace("em", "e-").replace("p", "."))
    return None

def get_theory_over_limit(limit, theory, color, line_style):
    graph = ROOT.TGraph()
    graph.SetLineColor(color)
    graph.SetLineWidth(4)
    graph.SetLineStyle(line_style)
    
    for i in range(limit.GetN()):
        x = limit.GetX()[i]
        y = limit.GetY()[i]
        theory_y = theory.Eval(x)
        
        info(f"{x=}, {y=}, {theory_y=}")
        
        graph.SetPoint(i, x, theory_y/y)
    
    
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)
    graph.GetXaxis().SetLabelSize(0.04)
    graph.GetYaxis().SetLabelSize(0.04)
    graph.GetXaxis().SetTitleOffset(1.1)
    graph.GetYaxis().SetTitleOffset(1.1)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle("#sigma_{theory} / #sigma_{limit}")

    
    graph.GetXaxis().SetLimits(x_min, x_max)
    
    graph.SetMinimum(1e-2)
    graph.SetMaximum(1e2)
    
    return graph

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
    ratio_graphs = {}
    theory_lines = {}
    graph_2d = None
    hist_2d = None
    
    for variant, params in variants.items():
        colliderMode = "Collider" in variant
        lumi_scale = collider_cross_section_scale if colliderMode else 1.0
        
        if variable == "2d":
            limits = read_2d_limits(f"../datacards/limits_{histogram_name}_{variant}.txt")
            
            graph_2d, hist_2d = get_2d_graph(limits, lumi_scale, colliderMode)
            draw_2d_graphs(graph_2d)
            # draw_2d_graphs(hist_2d)
            continue
        
        marker_style, line_style, show_band, color, title = params
        
        if isinstance(color, str):
            colors = create_shaded_colors(color, 3, 0.3 if show_band else 1.0)
        else:
            color = ROOT.gROOT.GetColor(color)
            colors = [color.GetRed(), color.GetGreen(), color.GetBlue()]
            colors = "#{:02x}{:02x}{:02x}".format(int(colors[0]*255), int(colors[1]*255), int(colors[2]*255))
            colors = create_shaded_colors(colors, 3, 0.3 if show_band else 1.0)
        
        limits = read_limits(f"../datacards/limits_{histogram_name}_{variant}.txt")
        
        if not limits:
            continue

        

        graphs[variant] = get_graph_set(limits, colors, show_band, marker_style, line_style, lumi_scale)
        
        draw_graphs(graphs[variant], first, show_band)
        if title != "":
            legend.AddEntry(graphs[variant][1] if show_band else graphs[variant][0], title, "FL" if show_band else "L" if marker_style == -1 else "P")
        
        
        if variable == "mDarkPhoton":
            theory_lines[variant] = get_theory_line(colliderMode)
            canvas_ratio.cd()
            ratio_graphs[variant] = get_theory_over_limit(graphs[variant][0], theory_lines[variant], colors[1], line_style)
            ratio_graphs[variant].Draw("AL" if first else "Lsame")
        elif variable == "ctau" and scenario == "DP":
            mass = get_mass_from_name(variant, "mDarkPhoton")
            theory_lines[variant] = get_theory_line(colliderMode, mass)
        elif variable == "ctau" and scenario == "HV":
            mass = get_mass_from_name(variant, "mZprime")
            theory_lines[variant] = get_theory_line(colliderMode, mass)
            
        if variant in theory_lines:
            canvas.cd()
            theory_lines[variant].SetLineColor(colors[1])
            theory_lines[variant].SetLineWidth(4)
            theory_lines[variant].SetLineStyle(2)
            theory_lines[variant].Draw("Lsame")
        else:
            error(f"Couldn't get theory line for {variant}")
        
        first = False
    
    canvas.cd()
    # add a label on top of the pad
    label = ROOT.TLatex()
    label.SetNDC()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    # align to the right
    label.SetTextAlign(31)
    label.DrawLatex(0.90, 0.92, top_title)
    
    legend.Draw()
    
    if special_legend:
        special_legend.Draw()
    
    
    canvas_ratio.cd()
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    legend.Draw()
    
    canvas.Update()
    canvas_ratio.Update()
    output_path = f"../plots/limits_{histogram_name}/"
    ROOT.gSystem.Exec(f"mkdir -p {output_path}")
    
    canvas.SaveAs(f"{output_path}/limits_{scenario}_{variable}{suffix}.pdf")
    canvas_ratio.SaveAs(f"{output_path}/limitsRatio_{scenario}_{variable}{suffix}.pdf")
    
    if graph_2d:
        graph_2d.SaveAs(f"{output_path}/limits_{scenario}_{variable}{suffix}.root")
    
if __name__ == "__main__":
    main()
