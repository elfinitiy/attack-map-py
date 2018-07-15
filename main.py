import shared
import sys
import bar
import choropleth


import argparse

TYPE_BAR = "bar"
TYPE_CHOROPLETH = "choropleth"

parser = argparse.ArgumentParser(description="Build a bar/map of attacks using (nginx) logs")
parser.add_argument("-f", "--file", default="access.log", type=str, metavar="path",
                    help="path to log file", dest="path")
parser.add_argument("-t", "--type", default=TYPE_BAR, type=str, metavar="type",
                    help="render type", dest="type")
parser.add_argument("-g", "--geo", default="GeoLite2-Country.mmdb", type=str, metavar="geo",
                    help="country geo db", dest="geo_path")



args = parser.parse_args()
print(args)

shared.initialize_log_file(args.path)

plot_obj = None
if args.type == TYPE_CHOROPLETH:
    plot_obj = choropleth.buid_choropleth_map(args.geo_path)
else:
    plot_obj = bar.build_bar_chart()

plot_obj.show()
