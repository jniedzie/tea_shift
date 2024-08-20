import ROOT

cms_graph_path = "../plots/limits_MuonsHittingDetectorPair_mass/limits_DP_2d_cms.root"
shift_graph_path = "../plots/limits_MuonsHittingDetectorPair_mass/limits_DP_2d_shift160.root"

def main():
    cms_file = ROOT.TFile(cms_graph_path, "READ")
    shift_file = ROOT.TFile(shift_graph_path, "READ")
    
    cms_graph = cms_file.Get("Graph2D")
    shift_graph = shift_file.Get("Graph2D")
    
    # create a new TGraph2D and fill it with the ratios of shift/cms
    shift_graph_ratio = ROOT.TGraph2D()
    shift_graph_ratio.SetName("Graph2D_ratio")
    
    
    shift_points = {}
    for i in range(shift_graph.GetN()):
        x = shift_graph.GetX()[i]
        y = shift_graph.GetY()[i]
        z = shift_graph.GetZ()[i]
        shift_points[(x, y)] = z
    
    max_ratio = 0
    max_ratio_x = 0
    max_ratio_y = 0
    
    for i in range(cms_graph.GetN()):
        
        x = cms_graph.GetX()[i]
        y = cms_graph.GetY()[i]
        z = cms_graph.GetZ()[i]
        
        if (x, y) in shift_points:
            shift_z = shift_points[(x, y)]
            ratio = shift_z / z
            
            print(f"ctau = 10^{x:.0f} m, mass = {y:.0f} GeV, CMS = {z:.1f}, SHIFT: {shift_z:.1f}, ratio: {ratio:.1f}")
            
            if ratio > max_ratio:
                max_ratio = ratio
                max_ratio_x = x
                max_ratio_y = y

            shift_graph_ratio.SetPoint(i, x, y, ratio)
        else:
            print(f"Warning: No matching point found in shift_graph for ({x}, {y})")
        

    print(f"Max ratio: {max_ratio:.1f} for ctau = 10^{max_ratio_x:.0f} m, mass = {max_ratio_y:.0f} GeV")
    
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    canvas.cd()
    
    shift_graph_ratio.SetNpx(100)
    shift_graph_ratio.SetNpy(100)
    
    shift_graph_ratio.Draw("colz")
    # shift_graph_ratio.GetHistogram().GetXaxis().SetLimits(-2, 3)
    
    
    # Define the contour level for z = 1.0
    contours = ROOT.TArrayD(1)
    contours[0] = 1.0    
    contour_hist = shift_graph_ratio.GetHistogram().Clone("contour_hist")
    contour_hist.SetContour(1, contours.GetArray())
    contour_hist.SetLineColor(ROOT.kViolet)
    contour_hist.SetLineWidth(3)
    contour_hist.Draw("cont3 same")  # 'cont3' draws the contour line without filling
    
    ROOT.gPad.SetLogz()
    
    shift_graph_ratio.SetMinimum(1e-2)
    shift_graph_ratio.SetMaximum(60)
    
    shift_graph_ratio.GetXaxis().SetTitle("log_{10}(c#tau [m])")
    shift_graph_ratio.GetYaxis().SetTitle("m_{A'} [GeV]")
    shift_graph_ratio.GetZaxis().SetTitle("#frac{#sigma^{SHIFT}_{benchmark}}{#sigma^{SHIFT}_{limit}} / #frac{#sigma^{CMS}_{benchmark}}{#sigma^{CMS}_{limit}}")
    
    shift_graph_ratio.GetXaxis().SetTitleSize(0.05)
    shift_graph_ratio.GetYaxis().SetTitleSize(0.05)
    shift_graph_ratio.GetZaxis().SetTitleSize(0.05)
    
    shift_graph_ratio.GetXaxis().SetLabelSize(0.04)
    shift_graph_ratio.GetYaxis().SetLabelSize(0.04)
    shift_graph_ratio.GetZaxis().SetLabelSize(0.04)
    
    shift_graph_ratio.GetXaxis().SetTitleOffset(1.1)
    shift_graph_ratio.GetYaxis().SetTitleOffset(1.1)
    shift_graph_ratio.GetZaxis().SetTitleOffset(1.5)
    
    ROOT.gPad.SetRightMargin(0.25)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    
    shift_graph_ratio.SetTitle("")
    shift_graph_ratio.GetHistogram().GetXaxis().SetRangeUser(-2, 3)
    shift_graph_ratio.GetHistogram().GetYaxis().SetRangeUser(11, 70)
    
    canvas.Update()
    canvas.SaveAs("../plots/limits_MuonsHittingDetectorPair_mass/limits_DP_2d_shiftOverCms.pdf")

if __name__ == "__main__":
    main()