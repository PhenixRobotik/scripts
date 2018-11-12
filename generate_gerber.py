#!/bin/env python2

from __future__ import print_function
import sys
import os
import shutil
import pcbnew


def generate_gerber(name, output_dir):
    board = pcbnew.LoadBoard(name)
    pctl = pcbnew.PLOT_CONTROLLER(board)
    popt = pctl.GetPlotOptions()

    ###########################################################################
    # Output options
    plot_format = pcbnew.PLOT_FORMAT_GERBER
    popt.SetOutputDirectory(output_dir)

    ###########################################################################
    # Included Layers:
    layers = [
        {'layer': pcbnew.F_Cu, 'suffix': 'F.Cu'},
        {'layer': pcbnew.B_Cu, 'suffix': 'B.Cu'},

        {'layer': pcbnew.F_SilkS, 'suffix': 'F.SilkS'},
        {'layer': pcbnew.B_SilkS, 'suffix': 'B.SilkS'},

        {'layer': pcbnew.B_Paste, 'suffix': 'B.Paste'},
        {'layer': pcbnew.F_Paste, 'suffix': 'F.Paste'},

        {'layer': pcbnew.B_Mask, 'suffix': 'B.Mask'},
        {'layer': pcbnew.F_Mask, 'suffix': 'F.Mask'},

        {'layer': pcbnew.Edge_Cuts, 'suffix': 'Edge.Cuts'},
    ]

    ###########################################################################
    # General Options:
    popt.SetPlotFrameRef(False)
    popt.SetPlotValue(True)
    popt.SetPlotReference(True)
    # popt.SetPlotInvisibleText(False)
    # popt.SetPlotViaOnMaskLayer(False)
    popt.SetExcludeEdgeLayer(True)
    popt.SetPlotPadsOnSilkLayer(False)
    popt.SetUseAuxOrigin(False)

    # popt.SetMirror(False)
    # popt.SetNegative(False)

    ###########################################################################
    popt.SetDrillMarksType(popt.NO_DRILL_SHAPE)
    popt.SetAutoScale(False)
    popt.SetScale(1)
    popt.SetPlotMode(pcbnew.FILLED)
    popt.SetLineWidth(pcbnew.FromMM(0.1))

    ###########################################################################
    # Gerber Options:
    popt.SetUseGerberProtelExtensions(True)
    # popt.SetUseGerberAttributes(True)

    popt.SetCreateGerberJobFile(False)
    popt.SetSubtractMaskFromSilk(False)

    # popt.SetFormat()

    ###########################################################################
    # Generate files now

    for l in layers:
        pctl.SetLayer(l['layer'])
        # pctl.OpenPlotfile()
        pctl.OpenPlotfile(l['suffix'], pcbnew.PLOT_FORMAT_GERBER, l['layer'])
        print(l['suffix'])
        pctl.PlotLayer()

    pctl.ClosePlot()


def generate_drillmap(name, output_dir):
    board = pcbnew.LoadBoard(name)
    writer = pcbnew.EXCELLON_WRITER(board)

    writer.SetFormat(True)
    writer.SetOptions(
        aMirror=False,
        aMinimalHeader=False,
        aOffset=writer.GetOffset(),
        aMerge_PTH_NPTH=True
    )
    writer.CreateDrillandMapFilesSet(
        output_dir,
        aGenDrill=True,
        aGenMap=False,
        aReporter=None
    )


def archive_dir(dirname, filename):
    shutil.make_archive(filename, 'zip', root_dir=None, base_dir=dirname)


if __name__ == '__main__':
    files = []
    if len(sys.argv) == 1:
        import glob
        files = glob.glob("*.kicad_pcb")

    if len(sys.argv) >= 2:
        files = sys.argv[1:]

    for filename in files:
        project_dir = os.path.dirname(filename)
        gerber_dir = os.path.join(project_dir, 'gerber')
        print()
        print('Using', filename)

        generate_gerber(filename, 'gerber')
        generate_drillmap(filename, gerber_dir)

        zipname, ext = os.path.splitext(filename)
        archive_dir(gerber_dir, zipname)
