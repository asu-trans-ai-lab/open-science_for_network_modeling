# @author       Xuesong Zhou (xzhou74@asu.edu)
# @time         2022/1/4 13:03
# @desc         [script description]


import osm2gmns as og
import signal4gmns as sg

import os


# NOTE: WHEN USING THIS SCRIPT, ONLY EXECUTE COMMANDS FOR THE STAGE THAT YOU ARE CURRENTLY WORKING ON.
#       COMMENT COMMANDS FOR OTHER SATGES IN THE MAIN FUNCTION.


map_folder = r'MRM'

def getInitialNet():
    # choose link_types from 'motorway', 'trunk','primary','secondary', 'tertiary', 'residential'. default: 'all'
    net = og.getNetFromFile(filename=os.path.join(map_folder, 'map.pbf',),
                            network_types=('auto', "bike", "walk"), 
#                           network_types=('auto'), 
                            link_types = ('motorway', 'trunk','primary','secondary', 'tertiary','footway','cycleway'),
                            default_lanes=True, default_speed=True, default_capacity=True, POI =True)

    og.consolidateComplexIntersections(net, auto_identify=True)
    og.generateNodeActivityInfo(net)
#    og.buildMultiResolutionNets(net)
    og.outputNetToCSV(net, output_folder=map_folder)


def generateSignalTiming():
    # Step 0 Preprocessing
    sg.set_map_folder(map_folder)
    sg.set_reference_cycle_length()
    sg.set_default_volume()
    # Step 1: load movement data and volume
    sg.load_movement_data_and_volume()
    # Step 2: Determine major approach for each signal node and output log files
    sg.determine_major_approach()
    # Step 3: Select left_turn treatment for each signal node and output log files
    sg.select_left_turn_treatment()
    # Step 4: Estimate signal timing for each signal node
    sg.estimate_signal_timing(input_preset_phase_mvmt_file=False)
    # Step 5: Output signal_timing_phase.csv and signal_timing_phase.csv Files
    sg.output_signal_phasing_files()
    # Step 6: Output timing.csv
    sg.output_signal_timing_file_and_modify_microLink_file()
    

def rePathFindingDTASimulation():
    pass
def regenerateNet_based_on_macroNet():
    net = og.loadNetFromCSV(folder=map_folder,
                            node_file='node.csv', link_file='link.csv')

    # The consolidation function is needed if we changed 'main_node_id' of some nodes in node.csv in Stage 2.
    og.consolidateComplexIntersections(net, auto_identify=False)

    og.buildMultiResolutionNets(net)

    og.outputNetToCSV(net, output_folder=map_folder)


if __name__ == '__main__':
    # Stage 1: get an initial network
    getInitialNet()
    #generateSignalTiming()
    # Stage 2: modify the initial network in CSV files

    # Stage 3: read the modified network from CSV and regenerate multiresolution networks
    #regenerateNet_based_on_macroNet()


