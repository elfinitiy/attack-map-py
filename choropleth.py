import geoip2.database
import geoip2.errors
import shared
import pprint
import re
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas
re_ip_only = re.compile("(.*) - -.*")


def buid_choropleth_map(geo_path):
    geo_ip_db = geoip2.database.Reader(geo_path)
    #pprint.pprint(shared.filtered_requests)
    #quit()

    ip_list = shared.extract_re(shared.filtered_requests, re_ip_only, 1)
    #pprint.pprint(badRequestList)
    #pprint.pprint(ipList)

    #sometimes its simply not there


    def map_ip_to_country(ip_str):
        try:
            return geo_ip_db.country(ip_str)
        except geoip2.errors.AddressNotFoundError:
            return None


    country_list_to_map = list(map(map_ip_to_country, ip_list))
    country_list_to_filter = list(filter(lambda geo_obj: geo_obj, country_list_to_map))
    country_list_iso2_to_filter = list(map(lambda geo_obj: geo_obj.country.iso_code, country_list_to_filter))
    country_list_iso2 = list(filter(lambda iso_code: iso_code, country_list_iso2_to_filter))
    country_list_iso3 = list(map(lambda iso_code: pycountry.countries.get(alpha_2=iso_code).alpha_3, country_list_iso2))
    #pprint.pprint(country_list_iso3)

    #quit()
    pandas.set_option('display.max_columns', None)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world_iso3 = world.iso_a3

    # Countries that don't exist in the list, they are replaced by -99 which skews the dict
    iter_for_lost_countries = iter(["CXR", "SMR", "KNA"])

    iso3_attack_count = {}
    total_world_iso3 = world_iso3.count()
    for world_iso3_key in range(total_world_iso3):
        iso3 = world_iso3[world_iso3_key]
        if iso3 == "-99":
            iso3 = next(iter_for_lost_countries)
        iso3_attack_count[iso3] = 0
    #pprint.pprint(iso3_attack_count)
    for iso3 in country_list_iso3:
        if iso3 in iso3_attack_count:
            iso3_attack_count[iso3] += 1
    #pprint.pprint(iso3_attack_count)

    attack_geo_list = []
    for attack_count in iso3_attack_count.values():
        attack_geo_list.append(attack_count)

    world["attack_count"] = attack_geo_list

    colors = 9
    cmap = 'Blues'
    world_plot = world.plot(column="attack_count", k=colors,
                            edgecolor="#333333", alpha=0.5, cmap=cmap, scheme="fisher_jenks", legend=True)
    world_plot.set_title("Attack count by countries")
    plt.style.use('dark_background')
    return plt

