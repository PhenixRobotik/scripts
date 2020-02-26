#!/bin/env python3

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Salamandar <felix@piedallu.me> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Félix Piédallu
# ----------------------------------------------------------------------------

import sys
import os
import shutil
import pcbnew
import csv
import re

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
    print('Drill map')

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

def generate_position_csv(name, output_dir):
    board = pcbnew.LoadBoard(name)
    board_name, ext = os.path.splitext(name)
    print('Position file')

    with open(os.path.join(output_dir, board_name + '-top-pos.csv'), 'w', newline='') as out_top,\
         open(os.path.join(output_dir, board_name + '-bottom-pos.csv'), 'w', newline='') as out_bot:
            fieldnames = ['Ref','Val','Package','PosX','PosY','Rot','Side']
            csv_top = csv.DictWriter(out_top, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            csv_bot = csv.DictWriter(out_bot, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            csv_top.writeheader()
            csv_bot.writeheader()

            def sorted_nicely(l):
                convert = lambda text: int(text) if text.isdigit() else text
                alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key.GetReference())]
                return sorted(l, key = alphanum_key)

            sorted_modules = sorted_nicely(board.GetModules())

            aux_origin = board.GetAuxOrigin()

            for m in sorted_modules:
                is_cms = (m.GetAttributes() == pcbnew.MOD_CMS)
                is_top = not m.IsFlipped()
                is_bot = not is_top

                if not is_cms:
                    continue

                side =  'top'     if is_top \
                else    'bottom'  if is_bot \
                else    'none'

                values = {
                    'Ref': m.GetReference(),
                    'Val': m.GetValue(),
                    'Package': m.GetFPID().GetLibItemName(),
                    'PosX': pcbnew.ToMM(m.GetPosition().x - aux_origin.x),
                    'PosY': pcbnew.ToMM(aux_origin.y - m.GetPosition().y),
                    'Rot': m.GetOrientationDegrees(),
                    'Side': side,
                }

                if side == 'top':
                    csv_top.writerow(values)
                if side == 'bottom':
                    csv_bot.writerow(values)


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
        print('Using', filename)

        generate_gerber(filename, 'gerber')
        generate_drillmap(filename, gerber_dir)
        generate_position_csv(filename, 'gerber')

        zipname, ext = os.path.splitext(filename)
        archive_dir(gerber_dir, zipname)

