# @author       Jiawei Lu (jiaweil9@asu.edu)
# @time         2022/1/6 16:59
# @desc         [script description]


import osm2gmns as og

map_folder = 'network'


def generateMovements():
    net = og.loadNetFromCSV(folder=map_folder,
                            node_file='node.csv', link_file='link.csv')

    og.consolidateComplexIntersections(net, auto_identify=False)

    og.generateMovements(net)

    og.buildMultiResolutionNets(net, auto_movement_generation=False)

    og.outputNetToCSV(net, output_folder=map_folder, prefix='updated')


if __name__ == '__main__':
    generateMovements()


