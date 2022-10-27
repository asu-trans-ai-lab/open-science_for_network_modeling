# @author       Xuesong Zhou (xzhou74@asu.edu)
# @time         2022/1/4 13:03
# @desc         [script description]


import osm2gmns as og
import signal4gmns as sg

import os


# NOTE: WHEN USING THIS SCRIPT, ONLY EXECUTE COMMANDS FOR THE STAGE THAT YOU ARE CURRENTLY WORKING ON.
#       COMMENT COMMANDS FOR OTHER SATGES IN THE MAIN FUNCTION.


map_folder = r''

def getInitialNet():
    # choose link_types from 'motorway', 'trunk','primary','secondary', 'tertiary', 'residential'. default: 'all'
    net = og.getNetFromFile(filename=os.path.join(map_folder, 'map.pbf'),
                            network_types=('auto'),
                            POI=True, POI_sampling_ratio= 0.01,
                            default_lanes=True, default_speed=True, default_capacity=True) 

    og.consolidateComplexIntersections(net, auto_identify=True)
    og.generateNodeActivityInfo(net)

    og.outputNetToCSV(net, output_folder=map_folder)


if __name__ == '__main__':
    # Stage 1: get an initial network
    getInitialNet()
    #generateSignalTiming()
    # Stage 2: modify the initial network in CSV files

    # Stage 3: read the modified network from CSV and regenerate multiresolution networks
    #regenerateNet_based_on_macroNet()


