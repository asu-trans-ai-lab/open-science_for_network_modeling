import osm2gmns as og

net = og.getNetFromOSMFile('./10_CMU_US/map.osm', network_type=('auto', 'bike', 'walk'), POIs=True, default_lanes=True, default_speed=True)
# og.outputNetToCSV(net)
# check and modify (if necessary) network files before complex intersection consolidation
# net = og.getNetFromCSV()
og.consolidateComplexIntersections(net)
og.outputNetToCSV(net, '10_CMU_US')
