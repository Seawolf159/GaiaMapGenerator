import wx
import wx.grid
from PIL import Image
import random
import copy
import math as m
import sys

# sys.stdout = open('my_stdout.log', 'w')
# sys.stderr = open('my_stderr.log', 'w')

default_map_path = "images/Gaia_map.png"
default_image_name = "Gaia_map"
background_path = "images/Tech_bg.png"
information_magenta_path = "images/Information_icon_magenta.png"
information_blue_path = "images/Information_icon_blue.png"
image_path = "images/"
image_format = ".png"

settings_path = "settings.txt"
default_settings_path = "default_settings.txt"

default_num_players = 2
default_num_iterations = 100
default_radius = 2
default_cluster_size = 5
default_min_neighbor_distance = 3
default_max_edge_planets = 2

default_terra_param = [1.0, 1.0, 0.0, 1.0]
default_gaia_param = 1.0
default_trans_param = 0.0
default_range_factor = [1.0, 1.0, 0.8, 0.05]

default_nearness_param = 0.0
default_density_param = 40
default_ratio_param = 7


TEC = ['TECore', 'TECcre', 'TECknw', 'TECpow', 'TECqic', 'TECpia', 'TECgai', 'TECtyp', 'TECvps']
ADV = ['ADVore', 'ADVknw', 'ADVqic', 'ADVgai', 'ADVtyp', 'ADVstp', 'ADVlab', 'ADVminV', 'ADVminB', 'ADVtrsV',
       'ADVtrsB', 'ADVsecV', 'ADVsecO', 'ADVfedV', 'ADVfedP']
BOO = ['BOOnav', 'BOOter', 'BOOmin', 'BOOtrs', 'BOOlab', 'BOOpia', 'BOOgai', 'BOOqic', 'BOOpwt', 'BOOknw']
RND = ['RNDter', 'RNDfed', 'RNDstp', 'RNDmin', 'RNDtrs3', 'RNDtrs4', 'RNDpia', 'RNDpia', 'RNDgai3', 'RNDgai4']
FIN = ['FINbld', 'FINfed', 'FINgai', 'FINsec', 'FINsat', 'FINtyp']
FED = ['FEDknw', 'FEDore', 'FEDcre', 'FEDqic', 'FEDpwt']

list_of_pieces = [FED[:], ADV[:], TEC[:], TEC[:], BOO[:], RND[:], FIN[:]]

"""
Planets = {"Em" : Empty(), "Ga" : Gaia(), "Tr" : Transdim(),
           "Br" : Brown(), "Bl" : Blue(), "Bk" : Black(),
           "Ye" : Yellow(), "Or" : Orange(), "Re" : Red(), "Wh" : White()}
"""

Sector_data = {
    "1": [["Em"],
          ["Em", "Bl", "Em", "Em", "Em", "Br"],
          ["Em", "Em", "Em", "Tr", "Em", "Or", "Re", "Em", "Em", "Ye", "Em", "Em"]],
    "2": [["Em"],
          ["Em", "Wh", "Em", "Em", "Br", "Em"],
          ["Bk", "Em", "Em", "Ye", "Em", "Tr", "Em", "Re", "Em", "Em", "Em", "Or"]],
    "3": [["Em"],
          ["Em", "Em", "Wh", "Em", "Em", "Ga"],
          ["Tr", "Em", "Em", "Bk", "Em", "Em", "Ye", "Bl", "Em", "Em", "Em", "Em"]],
    "4": [["Em"],
          ["Re", "Em", "Br", "Em", "Or", "Em"],
          ["Bk", "Em", "Em", "Em", "Bl", "Em", "Em", "Em", "Em", "Wh", "Em", "Em"]],
    "5": [["Em"],
          ["Em", "Em", "Em", "Em", "Em", "Ga"],
          ["Wh", "Em", "Tr", "Re", "Em", "Em", "Ye", "Or", "Em", "Em", "Em", "Em"]],
    "6": [["Em"],
          ["Em", "Bl", "Em", "Ga", "Em", "Br"],
          ["Em", "Tr", "Em", "Em", "Ye", "Tr", "Em", "Em", "Em", "Em", "Em", "Em"]],
    "7": [["Em"],
          ["Re", "Em", "Ga", "Em", "Ga", "Em"],
          ["Em", "Br", "Em", "Em", "Em", "Em", "Bk", "Em", "Em", "Em", "Tr", "Em"]],
    "8": [["Em"],
          ["Wh", "Em", "Bk", "Em", "Or", "Em"],
          ["Bl", "Em", "Tr", "Em", "Em", "Em", "Em", "Tr", "Em", "Em", "Em", "Em"]],
    "9": [["Em"],
          ["Em", "Em", "Ga", "Em", "Bk", "Em"],
          ["Em", "Tr", "Wh", "Em", "Em", "Em", "Em", "Em", "Br", "Em", "Em", "Or"]],
    "10": [["Em"],
           ["Em", "Em", "Ga", "Em", "Em", "Ye"],
           ["Em", "Tr", "Tr", "Em", "Em", "Em", "Em", "Re", "Bl", "Em", "Em", "Em"]],
    "5_": [["Em"],
           ["Em", "Em", "Em", "Em", "Em", "Ga"],
           ["Wh", "Em", "Tr", "Re", "Em", "Em", "Em", "Or", "Em", "Em", "Em", "Em"]],
    "6_": [["Em"],
           ["Em", "Bl", "Em", "Ga", "Em", "Em"],
           ["Em", "Tr", "Em", "Em", "Ye", "Tr", "Em", "Em", "Em", "Em", "Em", "Em"]],
    "7_": [["Em"],
           ["Ga", "Em", "Br", "Em", "Ga", "Em"],
           ["Em", "Em", "Em", "Em", "Em", "Em", "Bk", "Em", "Em", "Em", "Tr", "Em"]]
}

color_wheel = ["Bk", "Br", "Ye", "Or", "Re", "Bl", "Wh"]


'''
---------------------------------------------------------------
---------------------------------------------------------------
Helper functions:
---------------------------------------------------------------
---------------------------------------------------------------
'''


def get_hexes_at_radius(centre_col, centre_row, radius):
    """
    Function that get a list of all hexes at a certain radius from
    a centre hex
    """
    if radius == 0:
        hex_list = [[centre_col, centre_row]]
        return hex_list
    if radius == 1:
        hex_list = [[centre_col, centre_row - 2],
                    [centre_col + 1, centre_row - 1],
                    [centre_col + 1, centre_row + 1],
                    [centre_col, centre_row + 2],
                    [centre_col - 1, centre_row + 1],
                    [centre_col - 1, centre_row - 1]]
        return hex_list
    if radius == 2:
        hex_list = [[centre_col, centre_row - 4],
                    [centre_col + 1, centre_row - 3],
                    [centre_col + 2, centre_row - 2],
                    [centre_col + 2, centre_row],
                    [centre_col + 2, centre_row + 2],
                    [centre_col + 1, centre_row + 3],
                    [centre_col, centre_row + 4],
                    [centre_col - 1, centre_row + 3],
                    [centre_col - 2, centre_row + 2],
                    [centre_col - 2, centre_row],
                    [centre_col - 2, centre_row - 2],
                    [centre_col - 1, centre_row - 3]]
        return hex_list
    if radius == 3:
        hex_list = [[centre_col, centre_row - 6],
                    [centre_col + 1, centre_row - 5],
                    [centre_col + 2, centre_row - 4],
                    [centre_col + 3, centre_row - 3],
                    [centre_col + 3, centre_row - 1],
                    [centre_col + 3, centre_row + 1],
                    [centre_col + 3, centre_row + 3],
                    [centre_col + 2, centre_row + 4],
                    [centre_col + 1, centre_row + 5],
                    [centre_col, centre_row + 6],
                    [centre_col - 1, centre_row + 5],
                    [centre_col - 2, centre_row + 4],
                    [centre_col - 3, centre_row + 3],
                    [centre_col - 3, centre_row + 1],
                    [centre_col - 3, centre_row - 1],
                    [centre_col - 3, centre_row - 3],
                    [centre_col - 2, centre_row - 4],
                    [centre_col - 1, centre_row - 5]]
        return hex_list
    return []


def get_stats(values):
    """
      Function to calculate statistics from a list of values
      Returns a list of results as follows:
      0 - average
      1 - variance
      2 - min value
      3 - max value
      """
    avg = 0.0
    var = 0.0
    minv = 100000.0
    maxv = -100000.0
    n = len(values)
    if n < 1:
        return [avg, var, minv, maxv]
    if n < 2:
        return [values[0], var, values[0], values[0]]
    for val in values:
        avg = avg + val
        if val < minv:
            minv = val
        if val > maxv:
            maxv = val
    avg = avg / n
    for val in values:
        diff = val - avg
        var = var + diff * diff
    var = var / n
    return [avg, m.sqrt(var), minv, maxv]


def get_color_dist(planet1, planet2):
    """
    Function that finds the distance between two planets on the color wheel
    """
    if planet1 == planet2:
        return 0
    if planet1 == "Ga" or planet2 == "Ga":
        return 1
    if planet1 == "Tr" or planet2 == "Tr":
        return 3
    first = -1
    second = -1
    for i in range(7):
        if color_wheel[i] == planet1 or color_wheel[i] == planet2:
            if first == -1:
                first = i
            else:
                second = i
                break
    dist = second - first
    if dist > 3:
        dist = 7 - dist
    return dist


def calc_happiness(planet_type, hex_map, GP, TP, HP, max_range, RF):
    """
    Function that calculates happiness for a planet type
    It loops through the map and sums the happiness of each
    planet of that type
    Happiness is determined as follows:
    - Gaia planet at range R adds happiness GP/R
    - Transdim planet at range R adds happiness TP/R
    - Other planet at range R adds happiness CP[CD]/R,
      where CD is the color distance to that planet.
      Hence CP is a list with 4 elements [cp0,cp1,cp2,cp3],
      giving the happiness for planets at color distance 0-3
    - Only planets within max_range is included
    """
    happiness = 0.0
    n_cols = len(hex_map)
    if n_cols < 1:
        return happiness
    n_rows = len(hex_map[0])
    if n_rows < 1:
        return happiness
    n_data = 0
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] == planet_type:
                for R in range(1, max_range + 1):
                    coords = get_hexes_at_radius(col, row, R)
                    for coord in coords:
                        if coord[0] < 0 or coord[0] >= n_cols:
                            continue
                        if coord[1] < 0 or coord[1] >= n_rows:
                            continue
                        if hex_map[coord[0]][coord[1]] is None or hex_map[coord[0]][coord[1]] == "Em":
                            continue
                        if hex_map[coord[0]][coord[1]] == "Ga":
                            happiness += GP * RF[R]
                        elif hex_map[coord[0]][coord[1]] == "Tr":
                            happiness += TP * RF[R]
                        else:
                            color_dist = get_color_dist(hex_map[col][row], hex_map[coord[0]][coord[1]])
                            happiness += HP[color_dist] * RF[R]
                        n_data += 1
    return happiness  # / n_data #not sure if we shoul "normalize" value or not... (if it makes sense)


def get_cluster_size_list(hex_map, ignored_types=[None, "Em"]):
    """
    Method that iterates over the map and finds clusters of planets
    It returns a list containing the size of each cluster
    The length of that list is then the number of clusters
    A single planet with no neighbours is a cluster of size 1
    ignored_types is a list of hex content types that should not be part of a cluster,
    defaults to [None,"Em"]
    """
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    cluster_sizes = []
    n_clusters = 0
    visited = [[0 for i in range(n_rows)] for j in range(n_cols)]
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] in ignored_types:
                visited[col][row] = 1
                continue
            if visited[col][row] == 1:
                continue

            # at this point we are at a planet in a hex that has not already been visited
            # it is the start of a new cluster
            n_clusters += 1
            cluster_sizes.append(0)
            cluster_planets = [[col, row]]
            i = 0
            while i < len(cluster_planets):
                planet_col = cluster_planets[i][0]
                planet_row = cluster_planets[i][1]
                i += 1
                if visited[planet_col][planet_row] == 1:
                    # need to check this here since it might have been visited after it was added to cluster_planets
                    continue

                # at a new planet, cluster grows:
                cluster_sizes[n_clusters - 1] += 1
                visited[planet_col][planet_row] = 1

                # check outwards for neighbour planets:
                neighbour_hexes = get_hexes_at_radius(planet_col, planet_row, 1)
                for j in range(6):
                    neighbour_col = neighbour_hexes[j][0]
                    neighbour_row = neighbour_hexes[j][1]
                    if (visited[neighbour_col][neighbour_row] == 1) or (
                            hex_map[neighbour_col][neighbour_row] in ignored_types):
                        # ignore neighbour hex if it has been visited already or if it has an ignorable type of content
                        continue
                    cluster_planets.append(neighbour_hexes[j])

    return cluster_sizes


def number_factor(PD, SC=30.0, OD=0.32153):
    """
    PD - Planet density
    OD - Optimal density
    SC - a number used to scale how bad it is to differ from the
         optimal density. Lower number means less bad
    Returns a number between 0.0 and 1.0 indicating how good the
    density of planets is compared to the optimal density
    """
    diff_from_opt = OD - PD
    exponent = -SC * diff_from_opt * diff_from_opt
    return pow(2.718281828, exponent)


def type_factor(NT, NP, SC=30.0):
    """
    NT - Number of planet types in area
    NP - Number of planets in area
    SC - a number used to scale how bad it is to differ from the
         optimal number of planet types. Lower number means less bad
    Returns a number between 0.0 and 1.0 indicating how good the ratio
    of different planet types is compared to the optimal ratio
    The optimal is to have as many different planet types as possible
    """
    max_types = 9.0
    if NP < max_types:
        max_types = NP
    ratio = 0.0
    if max_types > 0.0:
        ratio = NT / max_types
    diff_from_opt = 1.0 - ratio
    exponent = -SC * diff_from_opt * diff_from_opt
    return pow(2.718281828, exponent)


def hex_happiness(col, row, hex_map, NW=0.5, PD_SC=30.0, TR_SC=30.0, radius=3):
    """
    col - column of centre hex
    row - row of centre hex
    hex_map - the map..
    NW - how much weight should be placed on planet density vs planet type
    PD_SC - Planet Density Dropoff Scale. Higher number means that happiness drops
         off faster as the planet density moves away from the ideal density
    TR_SC - Type Ratio Dropoff Scale. Higher number means that the happiness drops
         off faster as the ratio of different planet types moves away from maximum
         ratio = (number of different planet types)/(number of different planet types possible)
    radius - radius used for each hex when calculatin hex happiness

    Optimal density of planets is about 1/3 in the full map
    as there are 61 planets divided on 190 hexes (0.321053)
    This means that inside a sector of range R there should be about
     2 planets when  R = 1 ( 7 total hexes, density = 0.285714)
     6 planets when  R = 2 (19 total hexes, density = 0.315789)
     12 planets when R = 3 (37 total hexes, density = 0.324324)
    We want a nice distribution of planet types through the space,
    so that for any sector with R = 3 we want as many planet types
    as possible to exist inside that sector.
    Given these factors we define hex happiness as follows:
     H = NW*number_factor(PD) + (1-NW)*type_factor(NT,NP)
    where
     NP - number of planets inside max_range
     PD - planet density in area = NP/(number of hexes in area)
     NT - number of unique planet types inside range 3
     NW - how much weight should be placed on number of planets
          vs nymber of types. NW must be a number between 0.0 and 1.0
     number_factor() is a formula that returns a maximum value of 1.0
          for the optimal number of planets, and smaller values for
          number of planets further away from the optimum
     type_factor() is a  formula that returns a maximum value of 1.0
          for the optimal number of planet types, and smaller values for
          number of planet types further away from the optimum
    The resulting value should be a number between 0.0 and 1.0
    """
    planet_types = ["Bk", "Br", "Ye", "Or", "Re", "Bl", "Wh", "Ga", "Tr"]
    n_planet_types = len(planet_types)
    exists_in_range = [0.0 for i in range(n_planet_types)]
    NH = 0.0
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    for R in range(radius + 1):
        coords = get_hexes_at_radius(col, row, R)
        for coord in coords:
            if coord[0] < 0 or coord[0] >= n_cols:
                continue
            if coord[1] < 0 or coord[1] >= n_rows:
                continue
            PT = hex_map[coord[0]][coord[1]]
            if PT is not None:
                NH += 1.0
                for i in range(n_planet_types):
                    if planet_types[i] == PT:
                        exists_in_range[i] += 1.0
                        break
    NP = 0.0
    NT = 0.0
    for i in range(n_planet_types):
        if exists_in_range[i] > 0:
            NT += 1.0
            NP += exists_in_range[i]
    PD = NP / NH

    return NW * number_factor(PD, PD_SC) + (1.0 - NW) * type_factor(NT, NP, TR_SC)


def calc_map_happiness(hex_map, NW=0.5, PD_SC=30.0, TR_SC=5.0, radius=3):
    """
    hex_map - the map used in the calculation
    PD_SC - Planet Density Dropoff Scale. Higher number means that happiness drops
         off faster as the planet density moves away from the ideal density
    TR_SC - Type Ratio Dropoff Scale. Higher number means that the happiness drops
         off faster as the ratio of different planet types moves away from maximum
         ratio = (number of different planet types)/(number of different planet types possible)
    radius - radius used for each hex when calculatin hex happiness

    Iterates over the hex_map and calculates total happiness (sum of happiness for each hex)
    Returns a vector with the following data
     0 - happiness percentage
     1 - total happiness
     3 - number of hexes calculated for (changes depending on map size)
    """
    total_happiness = 0.0
    n_hexes = 0.0
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] is None:
                continue
            total_happiness += hex_happiness(col, row, hex_map, NW, PD_SC, TR_SC, radius)
            n_hexes += 1.0
    happiness_percentage = 100.0 * total_happiness / n_hexes
    return [happiness_percentage, total_happiness, n_hexes]


def check_equal_neighbour_and_edge_status(col, row, hex_map, no_equal_radius=2):
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    is_edgy = False
    has_equal_neighbour = False
    for R in range(1, no_equal_radius + 1):
        if R > 1 and hex_map[col][row] == "Ga":
            break
        neighbours = get_hexes_at_radius(col, row, R)
        for coords in neighbours:
            if coords[0] < 0 or coords[1] < 0:
                if R == 1:
                    is_edgy = True
                continue  # in case we are outside the map
            if coords[0] >= n_cols or coords[1] >= n_rows:
                if R == 1:
                    is_edgy = True
                continue  # in case we are at the end of a col/row
            if hex_map[col][row] == hex_map[coords[0]][coords[1]]:
                has_equal_neighbour = True
                break
            if R == 1 and hex_map[coords[0]][coords[1]] is None:
                is_edgy = True
            if has_equal_neighbour and is_edgy:
                return [has_equal_neighbour, is_edgy]
    return [has_equal_neighbour, is_edgy]


'''
---------------------------------------------------------------
---------------------------------------------------------------
Map Stuff:
---------------------------------------------------------------
---------------------------------------------------------------
'''


class Map(object):
    def __init__(self, num_players, random_map=True, keep_core_sectors=False, disable_6_as_centre_in_2p=False,
                 layout_type_2p=0, layout_type_3p=0):
        """
        2-player layout options: (option: 6_ not in centre)
          type 0: sectors 1, 2, 3, 4, 5_, 6_, 7_
          type 1: sectors 1, 2, 3, 5_, 6, 7, 8
          type 2: sectors 2, 4, 5, 6, 7_, 8, 10
          type 3: sectors 1, 3, 4, 5, 6_, 7, 9
          type 4: sectors 1, 3, 4, 5, 7_, 9, 10
          type 5: random between 0-4
          type 6: 2-2-2: 1, 2, 3, 4, 9, 10
        3-player:
          type 0: 3-4-4, hex 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
          type 1: 2-3-3, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 2: 3-2-3, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 3: 3-3-2, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 4: 3-3-3, hex 1, 2, 3, 4, 5_, 6_, 7_, 9, 10
          type 5: 3-3-3, hex 1, 2, 3, 5_, 6, 7, 8, 9, 10
          type 6: random between type 0-5
          type 7: random between type 1-3
          type 8: random between type 4-5
        4-player: 3-4-3, hex 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

        centre (x, y) - (hor, ver)

        self.map: Sector objects
        self.map_data: Tupple with sector number and rotation
        """

        self.num_players = num_players
        self.random = random_map
        self.width = 23
        self.height = 30
        self.keep_core_sectors = keep_core_sectors
        self.disable_6_as_centre_in_2p = disable_6_as_centre_in_2p
        self.layout_type_2p = layout_type_2p
        self.layout_type_3p = layout_type_3p
        self.max_rejected_rotations = 20000

        """
        2-player layout options:
          type 5: random between 0-4
        """
        if self.num_players == 2:
            if self.layout_type_2p == 5:
                self.layout_type_2p = random.randint(0, 4)
            if self.layout_type_2p in [1, 2, 3, 4, 6]:
                self.keep_core_sectors = False

        """
        3p layout options:
          type 6: random between type 0-5
          type 7: random between type 1-3
          type 8: random between type 4-5
        """
        if self.layout_type_3p == 6:
            self.layout_type_3p = random.randint(0, 5)
        elif self.layout_type_3p == 7:
            self.layout_type_3p = random.randint(1, 3)
        elif self.layout_type_3p == 8:
            self.layout_type_3p = random.randint(4, 5)

        self.image_location = "images/"
        self.image_name = "Gaia_map"
        self.image_format = ".png"

        self.map_picture = None
        self.sector_image_width = 650
        self.sector_image_height = 705

        self.clockwise = True
        self.method = 0

        self.debug_level = 0

        # parameters used to eliminate illegal maps after rotation,
        # if these requirements are not met the rotation will continue
        self.minimal_equal_range = 3  # minimum range between equal planets (except Gaia and Transdim)
        self.maximum_cluster_size = 5  # set to 10 to ignore cluster size
        self.maximum_edge_planets = 3  # max number of edge planets allowed for a planet type
        self.rejection_count_exceeded = False

        self.map = None
        self.full_map = [[None for i in range(self.height)] for j in range(self.width)]
        self.set_map()
        self.generate_full_map()

        # general parameters used in optimizations
        self.try_count = 100
        self.search_radius = 2
        self.best_balance = 0.0
        self.reset_best_map_value()
        self.best_map_data = self.get_printable_map_data()
        self.previous_valid_map = self.best_map_data
        self.has_valid_map = False
        self.rejected_maps = 0

        # parameters used in the happiness calculation v0:
        self.range_factor = [1.0, 1.0 / 6.0, 1.0 / 12.0, 1.0 / 18.0]
        self.terraform_param = [2.0, 1.0, 1.0, 1.0]
        self.gaia_param = 2.0
        self.trans_param = 1.0

        # parameters used in optimization v1:
        self.NW = 0.5  # 1.0: only planet density (PD), 0.0: only Type Ratio (TR)
        self.PD_SC = 40.0
        self.TR_SC = 7.0

    def set_map(self):
        index = 0
        # default_sector_rotation = 0
        print ("\n---------------------------------------------\n")

        if self.num_players == 2:
            if self.layout_type_2p == 6:
                """
                  type 6: 2-2-2: 1, 2, 3, 4, 9, 10
                """
                print ("Setting up 2-2-2 map for 2 players")
                smallest = ["9", "1", "2", "3", "4", "10"]
                self.map = [["A", "B"], ["C", "D"], ["E", "F"]]
                self.centre = [[(6, 6), (11, 7)],
                               [(8, 14), (13, 15)],
                               [(10, 22), (15, 23)]]
                if not self.keep_core_sectors:
                    random.shuffle(smallest)
                else:
                    switch = random.randint(0, 1)
                    if switch == 1:
                        smallest[0] = "10"
                        smallest[5] = "9"

                self.content = smallest
            else:
                """
                  type 0: sectors 1, 2, 3, 4, 5_, 6_, 7_
                  type 1: sectors 1, 2, 3, 5_, 6, 7, 8
                  type 2: sectors 2, 4, 5, 6, 7_, 8, 10
                  type 3: sectors 1, 3, 4, 5, 6_, 7, 9
                  type 4: sectors 1, 3, 4, 5, 7_, 9, 10
                """
                print ("Setting up 2-3-2 map for 2 players")
                small = ["1", "5_", "2", "3", "6_", "4", "7_"]
                reminding_sectors = ["5_", "6_", "7_"]
                if self.layout_type_2p == 1:
                    small = ["1", "5_", "2", "3", "6", "8", "7"]
                    # reminding_sectors = ["5_", "6", "7", "8"]
                elif self.layout_type_2p == 2:
                    small = ["5", "6", "2", "7_", "8", "4", "10"]
                    # reminding_sectors = ["5", "6", "7_", "8", "10"]
                elif self.layout_type_2p == 3:
                    small = ["1", "5", "6_", "3", "7", "4", "9"]
                    # reminding_sectors = ["5", "6_", "7", "9"]
                elif self.layout_type_2p == 4:
                    small = ["1", "5", "7_", "3", "9", "4", "10"]
                    # reminding_sectors = ["5", "7_", "9", "10"]
                self.map = [["A", "B"], ["C", "D", "E"], ["F", "G"]]
                self.centre = [[(6, 6), (11, 7)],
                               [(3, 13), (8, 14), (13, 15)],
                               [(5, 21), (10, 22)]]
                if self.random:
                    if self.layout_type_2p == 0:
                        if not self.keep_core_sectors:
                            random.shuffle(small)
                            if self.disable_6_as_centre_in_2p and small[3] == "6_":
                                centre = small[0]
                                small[0] = small[3]
                                small[3] = centre
                        else:
                            random.shuffle(reminding_sectors)
                            reminding_on_the_right = random.randint(0, 1)
                            if reminding_on_the_right == 1:
                                small[1] = reminding_sectors[0]
                                small[4] = reminding_sectors[1]
                                small[6] = reminding_sectors[2]
                            else:
                                # shift core sectors to the right
                                small[1] = small[0]
                                small[4] = small[3]
                                small[3] = small[2]
                                small[6] = small[5]
                                small[0] = reminding_sectors[0]
                                small[2] = reminding_sectors[1]
                                small[5] = reminding_sectors[2]
                    else:
                        random.shuffle(small)

                self.content = small

        elif self.num_players == 4 or self.layout_type_3p == 0:
            print ("Setting up 3-4-3 map for 3/4 players")
            Large = ["10", "1", "5", "9", "2", "3", "6", "8", "4", "7"]
            self.map = [["A", "B", "C"], ["D", "E", "F", "G"], ["H", "I", "J"]]
            self.centre = [[(6, 6), (11, 7), (16, 8)],
                           [(3, 13), (8, 14), (13, 15), (18, 16)],
                           [(5, 21), (10, 22), (15, 23)]]
            if self.random:
                if not self.keep_core_sectors:
                    random.shuffle(Large)
                else:
                    reminding_sectors = ["5", "6", "7", "8", "9", "10"]
                    random.shuffle(reminding_sectors)
                    Large[0] = reminding_sectors[0]
                    Large[2] = reminding_sectors[1]
                    Large[3] = reminding_sectors[2]
                    Large[6] = reminding_sectors[3]
                    Large[7] = reminding_sectors[4]
                    Large[9] = reminding_sectors[5]
            self.content = Large
        elif self.num_players == 3:
            if self.layout_type_3p in [1, 2, 3]:
                """
                  type 1: 2-3-3, hex 1, 2, 3, 4, 5, 6, 7, 8
                  type 2: 3-2-3, hex 1, 2, 3, 4, 5, 6, 7, 8
                  type 3: 3-3-2, hex 1, 2, 3, 4, 5, 6, 7, 8
                """
                Medium_123 = ["7", "1", "5", "2", "3", "8", "4", "6"]
                if self.layout_type_3p == 1:
                    print ("Setting up 2-3-3 map for 3 players")
                    self.map = [["A", "B"], ["C", "D", "E"], ["F", "G", "H"]]
                    self.centre = [[(6, 6), (11, 7)],
                                   [(3, 13), (8, 14), (13, 15)],
                                   [(5, 21), (10, 22), (15, 23)]]
                elif self.layout_type_3p == 2:
                    print ("Setting up 3-2-3 map for 3 players")
                    self.map = [["A", "B", "C"], ["D", "E"], ["F", "G", "H"]]
                    self.centre = [[(6, 6), (11, 7), (16, 8)],
                                   [(8, 14), (13, 15)],
                                   [(5, 21), (10, 22), (15, 23)]]
                else:
                    print ("Setting up 3-3-2 map for 3 players")
                    self.map = [["A", "B", "C"], ["D", "E", "F"], ["G", "H"]]
                    self.centre = [[(6, 6), (11, 7), (16, 8)],
                                   [(8, 14), (13, 15), (18, 16)],
                                   [(10, 22), (15, 23)]]
                if self.random:
                    if not self.keep_core_sectors:
                        random.shuffle(Medium_123)
                    else:
                        reminding_sectors = ["5", "6", "7", "8"]
                        random.shuffle(reminding_sectors)
                        Medium_123[0] = reminding_sectors[0]
                        Medium_123[2] = reminding_sectors[1]
                        Medium_123[5] = reminding_sectors[2]
                        Medium_123[7] = reminding_sectors[3]
                self.content = Medium_123
            elif self.layout_type_3p == 4:
                """
                  type 4: 3-3-3, hex 1, 2, 3, 4, 5_, 6_, 7_, 9, 10
                """
                print ("Setting up 3-3-3 map for 3 players")
                Medium_4 = ["7_", "1", "5_", "9", "2", "3", "10", "4", "6_"]
                self.map = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
                self.centre = [[(6, 6), (11, 7), (16, 8)],
                               [(3, 13), (8, 14), (13, 15)],
                               [(5, 21), (10, 22), (15, 23)]]
                if self.random:
                    if not self.keep_core_sectors:
                        random.shuffle(Medium_4)
                    else:
                        reminding_sectors = ["5_", "6_", "7_", "9", "10"]
                        random.shuffle(reminding_sectors)
                        Medium_4[0] = reminding_sectors[0]
                        Medium_4[2] = reminding_sectors[1]
                        Medium_4[3] = reminding_sectors[2]
                        Medium_4[6] = reminding_sectors[3]
                        Medium_4[8] = reminding_sectors[4]
                self.content = Medium_4
            elif self.layout_type_3p == 5:
                """
                  type 5: 3-3-3, hex 1, 2, 3, 5_, 6, 7, 8, 9, 10
                """
                print ("Setting up 3-3-3 map for 3 players")
                Medium_5 = ["5_", "1", "6", "7", "2", "3", "8", "9", "10"]
                self.map = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
                self.centre = [[(6, 6), (11, 7), (16, 8)],
                               [(3, 13), (8, 14), (13, 15)],
                               [(5, 21), (10, 22), (15, 23)]]
                if self.random:
                    if not self.keep_core_sectors:
                        random.shuffle(Medium_5)
                    else:
                        reminding_sectors = ["5_", "6", "7", "8", "9", "10"]
                        random.shuffle(reminding_sectors)
                        Medium_5[0] = reminding_sectors[0]
                        Medium_5[2] = reminding_sectors[1]
                        Medium_5[3] = reminding_sectors[2]
                        Medium_5[6] = reminding_sectors[3]
                        Medium_5[7] = reminding_sectors[4]
                        Medium_5[8] = reminding_sectors[5]
                self.content = Medium_5

        for j, row in enumerate(self.map):
            for i, item in enumerate(row):
                sector_number = self.content[index]
                sector_content = copy.deepcopy(Sector_data[sector_number])
                self.map[j][i] = Sector(sector_content, sector_number)
                index += 1

    def generate_full_map(self, print_stuff=False):
        """
        Resets the full map, then distributes the sectors
        """
        self.full_map = [[None for i in range(self.height)] for j in range(self.width)]
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                content = sector.get_content()
                position = self.centre[j][i]

                if print_stuff:
                    print ("generating full map, sector at col=" + str(j) + ", row=" + str(i) + " has content ", content)

                for radii, planet_list in enumerate(content):
                    planet_coord_list = get_hexes_at_radius(position[0], position[1], radii)
                    for number, hexagon in enumerate(planet_list):
                        self.full_map[planet_coord_list[number][0]][planet_coord_list[number][1]] = hexagon

    def get_printable_map_data(self):
        """
        returns map data that is easy for image creation
        """
        map_data = copy.deepcopy(self.map)
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                sector_rotation = sector.get_rotation_deg()
                sector_number = sector.get_id()
                map_data[j][i] = [sector_number, sector_rotation]
        return map_data

    def get_full_map(self):
        return self.full_map

    def set_map_by_map_data(self, map_data, print_stuff=False):
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                sector_rotation = map_data[j][i][1]
                sector.set_ID(map_data[j][i][0])
                while sector.get_rotation_deg() != sector_rotation:
                    sector.rotate_sector_once()
        self.generate_full_map(print_stuff)

    def print_map(self):
        print ("---------------------")
        n_col = len(self.full_map)
        n_row = len(self.full_map[0])
        for row in range(n_row):
            cont = []
            for col in range(n_col):
                cont.append(self.full_map[col][row])
            print (cont)
        print ("---------------------")

    def make_image_map(self, clockwise=True):
        """
        sector list = [(sector, rotation)]
        """
        sector_list = self.get_printable_map_data()
        # print (sector_list)


        max_row_width = len(sector_list[0])
        for i in range(1, 3):
            if len(sector_list[i]) > max_row_width:
                max_row_width = len(sector_list[i])

        map_image_width = int(self.sector_image_width * max_row_width * 4.82 / 5.0)
        if self.num_players == 2 and self.layout_type_2p == 6:
            map_image_width = int(self.sector_image_width * max_row_width * 1.5)
        if self.num_players == 3:
            if self.layout_type_3p == 1:
                map_image_width = int(self.sector_image_width * max_row_width * 1.10)
            elif self.layout_type_3p == 2:
                map_image_width = int(self.sector_image_width * max_row_width * 1.04)
            elif self.layout_type_3p == 3:
                map_image_width = int(self.sector_image_width * max_row_width * 1.15)
            elif self.layout_type_3p == 4:
                map_image_width = int(self.sector_image_width * max_row_width * 1.15)
            elif self.layout_type_3p == 5:
                map_image_width = int(self.sector_image_width * max_row_width * 1.15)
        map_image_height = int(self.sector_image_height * 2.8)

        self.map_picture = Image.new("RGB", (map_image_width, map_image_height), (255, 255, 255))

        height_adjustment = int(self.sector_image_height * 0.1)
        v_scale = 0.71
        h_scale = 0.945

        sector_start_horizontal = int(self.sector_image_width * 0.56)
        sector_start_vertical = 0

        v_offsets = [0, 0, int(self.sector_image_height * 0.1)]
        h_offsets = [sector_start_horizontal, 0, sector_start_horizontal - int(self.sector_image_width * 0.18)]

        if self.num_players == 2 and self.layout_type_2p == 6:
            h_offsets = [self.sector_image_width * 0.18,
                         sector_start_horizontal,
                         self.sector_image_width * 0.94]
            v_offsets = [0,
                         int(self.sector_image_height * 0.1),
                         int(self.sector_image_height * 0.2)]
        if self.num_players == 3:
            if self.layout_type_3p == 2:
                h_offsets = [self.sector_image_width * 0.18,
                             sector_start_horizontal,
                             0.0]
                v_offsets = [0,
                             int(self.sector_image_height * 0.1),
                             int(self.sector_image_height * 0.1)]
            elif self.layout_type_3p == 3:
                h_offsets = [self.sector_image_width * 0.18,
                             sector_start_horizontal,
                             self.sector_image_width * 0.94]
                v_offsets = [0,
                             int(self.sector_image_height * 0.1),
                             int(self.sector_image_height * 0.2)]

        for j, row in enumerate(sector_list):
            for i, (sector_number, sector_rotation) in enumerate(row):
                filename = self.image_location + sector_number + self.image_format
                hor = int(h_offsets[j]) + int(self.sector_image_width * h_scale * i)
                ver = int(v_offsets[j]) + (int(self.sector_image_height * v_scale * j)) + int(
                    sector_start_vertical + height_adjustment * i)
                image = Image.open(filename)
                image = image.rotate(-sector_rotation)
                self.map_picture.paste(image, (hor, ver), image)

    def get_has_valid_map(self):
        return self.has_valid_map

    def show_image_map(self):
        self.make_image_map(self.clockwise)
        self.map_picture.show()

    def set_image_name(self, image_name_without_type):
        self.image_name = image_name_without_type

    def save_image_map(self):
        self.make_image_map(self.clockwise)
        address = self.image_location + self.image_name + self.image_format
        self.map_picture.save(address)

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def set_method(self, method):
        self.method = method
        self.reset_best_map_value()

    def set_try_count(self, try_count):
        self.try_count = try_count

    def set_search_radius(self, search_radius):
        self.search_radius = search_radius

    def set_minimum_equal_range(self, min_equal_range):
        self.minimal_equal_range = min_equal_range

    def set_max_cluster_size(self, cluster_size):
        self.maximum_cluster_size = cluster_size

    def set_max_edge_planets(self, max_edge_planets):
        self.maximum_edge_planets = max_edge_planets

    def set_method_0_params(self, terraform_param, gaia_param, trans_param, range_factor):
        self.range_factor = range_factor
        self.terraform_param = terraform_param
        self.gaia_param = gaia_param
        self.trans_param = trans_param

    def set_method_1_params(self, NW, PD_SC, TR_SC):
        self.NW = NW
        self.PD_SC = PD_SC
        self.TR_SC = TR_SC

    def rotate_map_randomly(self):
        keep_looking = True
        n_iter = 0
        core_sectors = ["1", "2", "3", "4"]
        while keep_looking:
            for row in self.map:
                for sector in row:
                    if self.keep_core_sectors and sector.get_id() in core_sectors:
                        continue
                    n_rot = random.randint(0, 5)
                    sector.rotate_sector(n_rot)
            self.generate_full_map()
            map_valid = self.is_valid_map()
            if map_valid:
                self.has_valid_map = True
                self.previous_valid_map = self.get_printable_map_data()
                keep_looking = False
            else:
                n_iter += 1
                if n_iter >= self.max_rejected_rotations:
                    keep_looking = False
                    self.rejection_count_exceeded = True
        #if self.debug_level == 1:
        #    print (n_iter)
        self.rejected_maps += n_iter

    def is_valid_map(self):
        """
        Function that checks various validity parameters for a map
        This is a merged version of other such functions that was defined earlier
        Merged them so that we have to iterate through the map fewer times
        """
        planet_type_edge_count = {"Br": 0,
                                  "Bk": 0,
                                  "Ye": 0,
                                  "Re": 0,
                                  "Or": 0,
                                  "Bl": 0,
                                  "Wh": 0}

        n_cols = len(self.full_map)
        if n_cols < 1:
            return False
        n_rows = len(self.full_map[0])
        if n_rows < 1:
            return False
        ignored_types = [None, "Em"]
        cluster_sizes = []
        n_clusters = 0
        n_planets = 0
        visited = [[0 for x in range(n_rows)] for y in range(n_cols)]
        for col in range(n_cols):
            for row in range(n_rows):
                if self.full_map[col][row] in ignored_types:
                    visited[col][row] = 1
                    continue
                if visited[col][row] == 1:
                    continue

                # at this point we are at a planet in a hex that has not already been visited
                # it is the start of a new cluster
                n_clusters += 1
                cluster_sizes.append(0)
                cluster_planets = [[col, row]]
                planet_index = 0
                while planet_index < len(cluster_planets):
                    planet_col = cluster_planets[planet_index][0]
                    planet_row = cluster_planets[planet_index][1]
                    planet_index += 1
                    if visited[planet_col][planet_row] == 1:
                        # need to check this here since it might have been visited after it was added to cluster_planets
                        continue

                    # at a new planet, cluster grows:
                    cluster_sizes[n_clusters - 1] += 1
                    visited[planet_col][planet_row] = 1
                    n_planets += 1

                    if cluster_sizes[n_clusters - 1] > self.maximum_cluster_size:
                        #if self.debug_level == 2:
                        #    print ("invalid map, cluster size >= ", self.maximum_cluster_size + 1)
                        #    print (self.get_printable_map_data())
                        return False

                    # check if planet has equal neighbour inside max range, or is an edge planet:
                    if self.full_map[planet_col][planet_row] != "Tr":
                        planet_data = check_equal_neighbour_and_edge_status(planet_col,
                                                                            planet_row,
                                                                            self.full_map,
                                                                            self.minimal_equal_range - 1)
                        if planet_data[0]:  # it has equal neighbour
                            #if self.debug_level == 2:
                            #    print ("invalid map, has equal neighbour ", self.full_map[planet_col][planet_row])
                            #    print (self.get_printable_map_data())
                            return False
                        if planet_data[1]:  # it is an edge planet
                            planet_type = self.full_map[planet_col][planet_row]
                            planet_type_edge_count[planet_type] += 1
                            if planet_type_edge_count[planet_type] > self.maximum_edge_planets:
                                #if self.debug_level == 2:
                                #    print ("invalid map, edge planets ", planet_type, planet_type_edge_count)
                                #    print (self.get_printable_map_data())
                                return False

                    # check outwards for neighbour planets:
                    neighbour_hexes = get_hexes_at_radius(planet_col, planet_row, 1)
                    for hex_id in range(6):
                        neighbour_col = neighbour_hexes[hex_id][0]
                        neighbour_row = neighbour_hexes[hex_id][1]
                        if neighbour_col < 0 or neighbour_row < 0:
                            continue  # in case we are outside the map
                        if neighbour_col >= n_cols or neighbour_col >= n_rows:
                            continue  # in case we are at the end of a col/row
                        if (visited[neighbour_col][neighbour_row] == 1) \
                                or (self.full_map[neighbour_col][neighbour_row] in ignored_types):
                            # ignore neighbour hex if it has been visited already or if it has an ignorable type of content
                            continue
                        cluster_planets.append(neighbour_hexes[hex_id])
        #if self.debug_level >= 2:
        #    print ("VALID MAP! n_clusters =", n_clusters, ", n_planets = ", n_planets)
        #    print (self.get_printable_map_data())
        return True

    def calculate_balance(self, print_happiness=0):
        if self.method == 0:
            '''Optimize for Each planet type to have neighbours it likes'''
            planet_happiness = [0.0] * 7
            for i in range(7):
                planet_happiness[i] = calc_happiness(color_wheel[i],
                                                     self.full_map,
                                                     self.gaia_param,
                                                     self.trans_param,
                                                     self.terraform_param,
                                                     self.search_radius,
                                                     self.range_factor)
            stats = get_stats(planet_happiness)
            if print_happiness != 0:
                print ("Color Happiness:")
                for i in range(7):
                    if color_wheel[i] == "Bk":
                        print (" Grey   - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Br":
                        print (" Brown  - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Ye":
                        print (" Yellow - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Or":
                        print (" Orange - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Re":
                        print (" Red    - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Bl":
                        print (" Blue   - {:04.2f}".format(planet_happiness[i]))
                    if color_wheel[i] == "Wh":
                        print (" White  - {:04.2f}".format(planet_happiness[i]))
                stat_string = "Stats: "
                for i in range(4):
                    if i == 0:
                        stat_string += "Avg = {:04.2f}".format(stats[i])
                    if i == 1:
                        stat_string += ", Var = {:04.3f}".format(stats[i])
                    if i == 2:
                        stat_string += ", Min = {:04.2f}".format(stats[i])
                    if i == 3:
                        stat_string += ", Max = {:04.2f}".format(stats[i])
                print (stat_string)
            return stats[1]
        if self.method == 1:
            '''Optimize for even distribution of planets/planet types'''
            hp = calc_map_happiness(self.full_map, self.NW, self.PD_SC, self.TR_SC, self.search_radius)[0]
            if print_happiness != 0:
                print ("Happiness = {:04.2f}".format(hp))
            return hp
        if self.method == 2:
            '''Optimize for big clusters!'''
            cluster_sizes = get_cluster_size_list(self.full_map)
            stats = get_stats(cluster_sizes)
            avg_size = stats[0]
            if print_happiness != 0:
                print (cluster_sizes)
                print (stats)
            return avg_size
        if self.method == 3:
            '''Optimize for bigger largest cluster'''
            cluster_sizes = get_cluster_size_list(self.full_map)
            stats = get_stats(cluster_sizes)
            largest_size = stats[3]
            if print_happiness != 0:
                print (cluster_sizes)
                print (stats)
            return largest_size

    def is_better_balance(self, balance):
        '''
        For the various optimization methods this tells if bigger or smaller is better
        '''
        smaller_is_better = [0]
        bigger_is_better = [1, 2, 3]
        if self.method in smaller_is_better:
            return balance < self.best_balance
        elif self.method in bigger_is_better:
            return balance > self.best_balance

    def balance_map(self, print_progress_func=None, break_received_func=None):
        print ("Starting new search for map! Parameters:")
        print ("n_players = ", self.num_players)
        print ("n_iterations = ", self.try_count)
        print ("max_cluster_size = ", self.maximum_cluster_size)
        print ("max_edge_planets = ", self.maximum_edge_planets)
        print ("min_equal_dist   = ", self.minimal_equal_range)
        if self.method == 0:
            print ("method        = Planet Happiness")
            print ("search radius = ", self.search_radius)
            print ("terra_param   = ", self.terraform_param)
            print ("gaia_param    = ", self.gaia_param)
            print ("trans_param   = ", self.trans_param)
            print ("range_factor  = ", self.range_factor)
        elif self.method == 1:
            print ("method        = Planet Type Distribution")
            print ("search radius = ", self.search_radius)
            print ("type_weight   = ", self.NW)
            print ("dens dropoff  = ", self.PD_SC)
            print ("type dropoff  = ", self.TR_SC)
        elif self.method == 2:
            print ("method = Larger Avarage Cluster Size")
        self.reset_best_map_value()
        self.best_map_data = self.get_printable_map_data()
        progress = 0
        progress_jump = 100
        if self.try_count >= 10:
            progress_jump = 10
        if self.try_count >= 100:
            progress_jump = 1
        print_progress_func(progress, self.best_balance, self.rejected_maps)
        for try_no in range(self.try_count):
            self.rotate_map_randomly()
            if self.has_valid_map:
                self.set_map_by_map_data(self.previous_valid_map)
                balance = self.calculate_balance()
                if self.is_better_balance(balance):
                    self.best_balance = balance
                    self.best_map_data = self.get_printable_map_data()
                    self.set_map_by_map_data(self.best_map_data)
                    print ("new best map: ", self.best_map_data)
                    print ("score: ", self.best_balance)
                    # print ("it is valid: ", self.is_valid_map())
                    # print ("Full Map:")
                    # self.print_map()
            if self.rejection_count_exceeded:
                if print_progress_func is not None:
                    print_progress_func(100, self.best_balance, self.rejected_maps)
                break
            if try_no % (self.try_count / (int(100 / progress_jump))) == 0:
                progress += progress_jump
                if print_progress_func is not None:
                    print_progress_func(progress, self.best_balance, self.rejected_maps)
            if break_received_func is not None:
                do_break = break_received_func()
                if do_break:
                    if print_progress_func is not None:
                        print_progress_func(100, self.best_balance, self.rejected_maps)
                    break

    def get_best_map_data(self):
        return self.best_map_data

    def set_to_balanced_map(self):
        # print ("set to best map A: ", self.best_map_data)
        self.set_map_by_map_data(self.best_map_data)
        # print ("set to best map B: ", self.get_printable_map_data())

    def reset_best_map_value(self):
        if self.is_better_balance(-1.0):
            self.best_balance = 1000000.0
        else:
            self.best_balance = 0.0
        self.rejected_maps = 0


class Sector(object):
    def __init__(self, content, ID):
        """
            2.11    2.12    2.01
        2.10    1.6     1.1     2.02
    2.09    1.5     0.0     1.2     2.03
        2.08    1.4     1.3     2.04
            2.07    2.06    2.05

        content =  [[0.0],
                    [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
                    [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11, 2.12]]

        """

        self.content = content
        self.rotation = 0
        self.ID = ID

        self.relative_coordinates = [
            [(0, 0)],
            [(0, +2), (+1, -1), (+1, +1), (+0, -2), (-1, +1), (-1, -1)],
            [(-0, -4), (+1, -3), (+2, -2), (+2, -0), (+2, +2), (+1, +3),
            (0, +4), (-1, +3), (-2, +2), (-2, 0), (-2, -2), (-1, -3)]
        ]

    def rotate_sector(self, num_rotations):
        for i in range(num_rotations):
            self.rotate_sector_once()

    def rotate_sector_once(self):
        original_sector = copy.deepcopy(self.content)
        for i in [1, 2]:
            if i == 1:
                self.content[i] = self.content[i][-1:] + self.content[i][:-1]
            if i == 2:
                self.content[i] = self.content[i][-2:] + self.content[i][:-2]

        self.rotation += 1
        if self.rotation == 6:
            self.rotation = 0

    def set_ID(self, ID):
        self.ID = ID
        self.content = copy.deepcopy(Sector_data[ID])
        self.rotation = 0

    def get_content(self):
        data = copy.deepcopy(self.content)
        return data

    def get_relative_coord(self):
        return self.relative_coordinates

    def get_rotation_deg(self):
        return self.rotation * 60

    def get_id(self):
        return self.ID


'''
---------------------------------------------------------------
---------------------------------------------------------------
GUI Stuff:
---------------------------------------------------------------
---------------------------------------------------------------
'''


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Gaia Map Generator", size=(800, 800))
        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bold_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.make_menu()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        self.abort = False
        self.SetBackgroundColour(wx.WHITE)
        self.quality_description = ""

        ico = wx.Icon('images/gaia_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        path = information_magenta_path
        img_info = wx.Image(path, wx.BITMAP_TYPE_ANY)
        W = img_info.GetWidth()
        H = img_info.GetHeight()
        img_info = img_info.Scale(int(W * 0.15), int(H * 0.15))

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer_main = wx.BoxSizer(wx.HORIZONTAL)
        # vsizer_player_info = wx.BoxSizer(wx.VERTICAL)

        self.import_settings()

        self.num_players_options = ["2", "3", "4"]
        self.num_player_box = wx.RadioBox(self, label="Number of players", choices=self.num_players_options)
        self.num_player_box.SetSelection(self.num_players-2)

        btn_make_map = wx.Button(self, wx.ID_ADD, label="Generate map", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_make_map, btn_make_map)
        btn_randomize = wx.Button(self, wx.ID_PAGE_SETUP, label="Randomize setup", size=(140, 40))
        self.Bind(wx.EVT_BUTTON, self.on_randomize, btn_randomize)
        self.progress = wx.StaticText(self, 0, str("Map progress: 0%"))
        self.balance = wx.StaticText(self, 0, str(""))
        self.rejected = wx.StaticText(self, 0, str(""))
        self.btn_abort = wx.Button(self, wx.ID_ABORT, label="Stop", size=(80, 40))
        self.Bind(wx.EVT_BUTTON, self.on_abort, self.btn_abort)

        self.enable_abort_btn(False)

        vsizer_progress = wx.BoxSizer(wx.VERTICAL)
        vsizer_progress.Add(self.progress, 1, wx.EXPAND | wx.ALL)
        vsizer_progress.Add(self.rejected, 1, wx.EXPAND | wx.ALL)
        vsizer_progress.Add(self.balance, 1, wx.EXPAND | wx.ALL)

        hsizer_main.Add(self.num_player_box, 1, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_make_map, 2, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_randomize, 2, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(vsizer_progress, 1, wx.EXPAND | wx.ALL, 20)
        hsizer_main.Add(self.btn_abort, 1, wx.EXPAND | wx.ALL, 10)

        vsizer.Add(hsizer_main, 0, wx.EXPAND)

        # Setup
        hsizer_setup = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_setup = wx.BoxSizer(wx.VERTICAL)
        vsizer_setup_2 = wx.BoxSizer(wx.VERTICAL)
        vsizer_info = wx.BoxSizer(wx.VERTICAL)

        hsizer_method = wx.BoxSizer(wx.HORIZONTAL)
        methods = ["Neighbour Quality", "Distribution", "Big Clusters"]
        self.method_box = wx.RadioBox(self, label="Optimization method", choices=methods)
        hsizer_method.Add(self.method_box, -1, wx.EXPAND | wx.ALL, 10)

        img_info_method = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_method.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_method)
        hsizer_method.Add(img_info_method, 0, wx.CENTRE)

        vsizer_setup.Add(hsizer_method, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_name = wx.BoxSizer(wx.HORIZONTAL)
        name_txt = wx.StaticText(self, 0, "Image name")
        self.image_name = wx.TextCtrl(self, value=default_image_name)

        hsizer_name.Add(name_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_name.Add(self.image_name, 1)
        img_info_name = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_name.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_name)
        hsizer_name.Add(img_info_name, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_name, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_iterations = wx.BoxSizer(wx.HORIZONTAL)
        num_iterations_txt = wx.StaticText(self, 0, "Number of maps to evaluate")
        hsizer_iterations.Add(num_iterations_txt, 4, wx.EXPAND | wx.ALL, 5)

        self.num_iterations_opt = [10, 100, 1000, 10000]
        self.num_iterations_btn = []
        for i, value in enumerate(self.num_iterations_opt):
            if i == 0:
                btn = wx.RadioButton(self, label=str(value), style=wx.RB_GROUP)
            else:
                btn = wx.RadioButton(self, label=str(value))
            self.num_iterations_btn.append(btn)
            hsizer_iterations.Add(btn, 1)
            if value == self.num_iterations:
                btn.SetValue(True)

        vsizer_setup.Add(hsizer_iterations, 1, wx.EXPAND | wx.ALL, 5)

        img_info_iter = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_iter.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_num_maps)
        hsizer_iterations.Add(img_info_iter, 0, wx.BOTTOM)

        hsizer_cluster = wx.BoxSizer(wx.HORIZONTAL)
        cluster_txt = wx.StaticText(self, 0, "Maximum cluster size")
        hsizer_cluster.Add(cluster_txt, 4, wx.EXPAND | wx.ALL, 5)

        self.cluster_size_opt = [4, 5, 6, 100]
        self.cluster_size_btn = []
        for i, value in enumerate(self.cluster_size_opt):
            if value == 100:
                str_value = "7+"
            else:
                str_value = str(value)

            if i == 0:
                btn = wx.RadioButton(self, label=str_value, style=wx.RB_GROUP)
            else:
                btn = wx.RadioButton(self, label=str_value)
            self.cluster_size_btn.append(btn)
            hsizer_cluster.Add(btn, 1)
            if value == self.cluster_size:
                btn.SetValue(True)

        img_info_cluster = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_cluster.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_clusters)
        hsizer_cluster.Add(img_info_cluster, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_cluster, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_neighbor = wx.BoxSizer(wx.HORIZONTAL)
        neighbor_txt = wx.StaticText(self, 0, "Minimum distance between equal planets")
        hsizer_neighbor.Add(neighbor_txt, 5, wx.EXPAND | wx.ALL, 5)

        self.min_neighbor_distance_opt = [2, 3, 4]
        self.min_neighbor_distance_btn = []
        for i, value in enumerate(self.min_neighbor_distance_opt):
            if i == 0:
                btn = wx.RadioButton(self, label=str(value), style=wx.RB_GROUP)
            else:
                btn = wx.RadioButton(self, label=str(value))
            self.min_neighbor_distance_btn.append(btn)
            hsizer_neighbor.Add(btn, 1)
            if value == self.min_neighbor_distance:
                btn.SetValue(True)

        img_info_neighbor = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_neighbor.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_min_distance)
        hsizer_neighbor.Add(img_info_neighbor, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_neighbor, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_edge = wx.BoxSizer(wx.HORIZONTAL)
        edge_txt = wx.StaticText(self, 0, "Maximum edge planets")
        hsizer_edge.Add(edge_txt, 5, wx.EXPAND | wx.ALL, 5)

        self.max_edge_planets_opt = [1, 2, 3]
        self.max_edge_planets_btn = []
        for i, value in enumerate(self.max_edge_planets_opt):
            if i == 0:
                btn = wx.RadioButton(self, label=str(value), style=wx.RB_GROUP)
            else:
                btn = wx.RadioButton(self, label=str(value))
            self.max_edge_planets_btn.append(btn)
            hsizer_edge.Add(btn, 1)
            if value == self.max_edge_planets:
                btn.SetValue(True)

        img_info_edge = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_edge.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_max_edge)
        hsizer_edge.Add(img_info_edge, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_edge, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_core = wx.BoxSizer(wx.HORIZONTAL)
        core_txt = wx.StaticText(self, 0, "Keep core sectors")
        self.rb_core_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_core_no = wx.RadioButton(self, label="No")
        if self.keep_core:
            self.rb_core_yes.SetValue(True)
        else:
            rb_core_no.SetValue(True)

        hsizer_core.Add(core_txt, 6, wx.EXPAND | wx.ALL, 5)
        hsizer_core.Add(self.rb_core_yes, 1)
        hsizer_core.Add(rb_core_no, 1)

        img_info_core = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_core.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_core_sectors)
        hsizer_core.Add(img_info_core, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_core, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_center = wx.BoxSizer(wx.HORIZONTAL)
        center_txt = wx.StaticText(self, 0, "2-player: Disable sector 6b in centre")
        self.rb_center_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_center_no = wx.RadioButton(self, label="No")
        if self.disable_six_in_centre:
            self.rb_center_yes.SetValue(True)
        else:
            rb_center_no.SetValue(True)

        hsizer_center.Add(center_txt, 6, wx.EXPAND | wx.ALL, 5)
        hsizer_center.Add(self.rb_center_yes, 1)
        hsizer_center.Add(rb_center_no, 1)

        img_info_center = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_center.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_disable_6)
        hsizer_center.Add(img_info_center, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_center, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_2p_type = wx.BoxSizer(wx.HORIZONTAL)
        rb_2p_type_txt = wx.StaticText(self, 0, "2 player sectors")
        hsizer_2p_type.Add(rb_2p_type_txt, 1, wx.EXPAND | wx.ALL, 5)

        """
        2-player layout options:
          type 0: sectors 1, 2, 3, 4, 5_, 6_, 7_
          type 1: sectors 1, 2, 3, 5_, 6, 7, 8
          type 2: sectors 2, 4, 5, 6, 7_, 8, 10
          type 3: sectors 1, 3, 4, 5, 6_, 7, 9
          type 4: sectors 1, 3, 4, 5, 7_, 9, 10
          type 5: random between 0-4
          type 6: 2-2-2: 1, 2, 3, 4, 9, 10
        """
        self.layout_type_2p_options = ["1) 7 sectors: 1, 2, 3, 4, 5b, 6b, 7b",
                                       "2) 7 sectors: 1, 2, 3, 5b, 6a, 7a, 8",
                                       "3) 7 sectors: 2, 4, 5a, 6a, 7b, 8, 10",
                                       "4) 7 sectors: 1, 3, 4, 5a, 6b, 7a, 9",
                                       "5) 7 sectors: 1, 3, 4, 5a, 7b, 9, 10",
                                       "6) 7 sectors: Random of options 1-5",
                                       "7) 6 sectors: 1, 2, 3, 4, 9, 10"]
        self.layout_type_2p_opt_id = [0,
                                      1,
                                      2,
                                      3,
                                      4,
                                      5,
                                      6]
        self.layout_type_2p_cb = wx.ComboBox(self,
                                             style=wx.CB_READONLY,
                                             choices=self.layout_type_2p_options)
        self.layout_type_2p_cb.SetSelection(0)
        hsizer_2p_type.Add(self.layout_type_2p_cb, 1)

        img_info_2p = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_2p.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_sectors)
        hsizer_2p_type.Add(img_info_2p, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_2p_type, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_3p_type = wx.BoxSizer(wx.HORIZONTAL)
        rb_3p_type_txt = wx.StaticText(self, 0, "3 player sectors")
        hsizer_3p_type.Add(rb_3p_type_txt, 1, wx.EXPAND | wx.ALL, 5)

        """
        3-player layout options:
          type 0: 3-4-3, hex 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
          type 1: 2-3-3, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 2: 3-2-3, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 3: 3-3-2, hex 1, 2, 3, 4, 5, 6, 7, 8
          type 4: 3-3-3, hex 1, 2, 3, 4, 5_, 6_, 7_, 9, 10
          type 5: 3-3-3, hex 1, 2, 3, 5_, 6, 7, 8, 9, 10
          type 6: random between type 0-5
          type 7: random between type 1-3
          type 8: random between type 4-5
        """
        self.layout_type_3p_options = ["1) 10 sectors: 1, 2, 3, 4, 5a, 6a, 7a, 8, 9, 10",
                                       "2) 9 sectors: 1, 2, 3, 4, 5b, 6b, 7b, 9, 10",
                                       "3) 9 sectors: 1, 2, 3, 5b, 6a, 7a, 8, 9, 10",
                                       "4) 9 sectors: Random of option 2 and 3",
                                       "5) 8 sectors: 2-3-3 : 1, 2, 3, 4, 5a, 6a, 7a, 8",
                                       "6) 8 sectors: 3-2-3 : 1, 2, 3, 4, 5a, 6a, 7a, 8",
                                       "7) 8 sectors: Random of option 5 and 6",
                                       "8) Random of all options"]
        self.layout_type_3p_opt_id = [0,
                                      4,
                                      5,
                                      8,
                                      1,
                                      2,
                                      7,
                                      6]
        self.layout_type_3p_cb = wx.ComboBox(self,
                                             style=wx.CB_READONLY,
                                             choices=self.layout_type_3p_options)
        self.layout_type_3p_cb.SetSelection(0)
        hsizer_3p_type.Add(self.layout_type_3p_cb, 1)

        img_info_3p = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_3p.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_sectors)
        hsizer_3p_type.Add(img_info_3p, 0, wx.BOTTOM)

        vsizer_setup.Add(hsizer_3p_type, 1, wx.EXPAND | wx.ALL, 5)

        btn_advanced = wx.Button(self, wx.ID_FILE, label="Advanced settings", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_advanced, btn_advanced)

        vsizer_setup.Add(btn_advanced, 1, wx.EXPAND | wx.ALL, 5)
        hsizer_setup.Add(vsizer_setup, 1, wx.EXPAND)

   #      info_padding = 5
   #
   #      header_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
   #      small_header_font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
   #      method_header = wx.StaticText(self, 1, "Methods")
   #      method_header.SetFont(header_font)
   #      vsizer_info.Add(method_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      methods_info = [["Neighbour Quality:",
   #                       """   Search for maps that has similar neighbour quality for all planet types.
   #  Quality is based on planet type and range to the neighbour.
   # (it looks for minimum variance of quality between the planet types)"""],
   #                      ["Distribution:", "   Search for maps with even spatial distribution of planet types."],
   #                      ["Big clusters:", "   Search for maps with large average cluster sizes"]]
   #
   #      for method, description in methods_info:
   #          small_header = wx.StaticText(self, 1, method)
   #          small_header.SetFont(small_header_font)
   #          vsizer_info.Add(small_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #          info_text = wx.StaticText(self, 1, description)
   #          vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      settings_header = wx.StaticText(self, 1, "Settings")
   #      settings_header.SetFont(header_font)
   #      vsizer_info.Add(settings_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      settings_info = [["Number of maps to evaluate:",
   #                        ["   How many legal maps to evaluate (Illegal maps are rejected during the search).",
   #                         "   A legal map follow all the limitations given by",
   #                         "    - Maximum cluster size allowed",
   #                         "    - Minimum distance between equal planets (not Gaia or Trans Dimentional)",
   #                         "    - Maximum number of edge planets allowed for a planet type",
   #                         """   NOTE: if you have too strong restrictions you might make an infinite loop where
   #  it is never able to find a legal map. It gives up after 20 000 illegal maps."""]],
   #                       ["Keep core sectors:",
   #                        "   Sectors 1, 2, 3 and 4 kept in the centre, only the remaining sectors are random"],
   #                       ["2-player: Disable sector 6b in centre", "   Since there are few planets in this sector"],
   #                       ["2- and 3-player sectors:",
   #                        """   Select sector count and types used in 2p or 3p"""]]
   #
   #      for i, (header, description) in enumerate(settings_info):
   #          small_header = wx.StaticText(self, 1, header)
   #          small_header.SetFont(small_header_font)
   #          vsizer_info.Add(small_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #          if i == 0:
   #              for text in description:
   #                  info_text = wx.StaticText(self, 1, text)
   #                  vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)
   #          else:
   #              info_text = wx.StaticText(self, 1, description)
   #              vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      hsizer_setup.Add(vsizer_info, 1, wx.EXPAND, 10)

        vsizer.Add(hsizer_setup, 1, wx.EXPAND)
        self.SetSizer(vsizer)
        self.Centre()
        self.Show()

    def onMouseOver_method(self, event):
        string = """"Neighbour Quality:
Search for maps that has similar neighbour quality for all planet types.
Quality is based on planet type and range to the neighbour.
(it looks for minimum variance of quality between the planet types)

Distribution:
Search for maps with even spatial distribution of planet types.

Big clusters:
Search for maps with large average cluster sizes"""
        event.GetEventObject().SetToolTip(string)


    def onMouseOver_name(self, event):
        string = """Image saved in "images" in program folder"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_num_maps(self, event):
        string = """How many legal maps to evaluate
(Illegal maps are rejected during the search).
A legal map follow all the limitations given by
    - Maximum cluster size allowed
    - Minimum distance between equal planets
      (not Gaia or Trans Dimentional)
    - Maximum number of edge planets allowed for a planet type
NOTE: if you have too strong restrictions you might make an infinite loop where it is never able to find a legal map.
It gives up after 20 000 illegal maps."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_clusters(self, event):
        string = """How many planets can be in one cluster
(directly in contact with each other)"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_min_distance(self, event):
        string = """How close each planet of one color can be to another one of the same color."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_max_edge(self, event):
        string = """How many edge planets each color can have."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_core_sectors(self, event):
        string = """Sectors 1, 2, 3 and 4 kept in the centre, only the remaining sectors are random."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_disable_6(self, event):
        string = """Since there are few planets in this sector."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_sectors(self, event):
        string = """How many of sectors to use, and which ones."""
        event.GetEventObject().SetToolTip(string)

    def read_settings(self):
        self.num_players = int(self.num_players_options[self.num_player_box.GetSelection()])

        self.keep_core = (True if self.rb_core_yes.GetValue() else False)
        self.disable_six_in_centre = (True if self.rb_center_yes.GetValue() else False)
        self.layout_type_2p_selected = self.layout_type_2p_cb.GetCurrentSelection()
        self.layout_type_2p = self.layout_type_2p_opt_id[self.layout_type_2p_selected]
        self.layout_type_3p_selected = self.layout_type_3p_cb.GetCurrentSelection()
        self.layout_type_3p = self.layout_type_3p_opt_id[self.layout_type_3p_selected]

        if self.disable_six_in_centre:
            if self.num_players == 2:
                self.disable_six_in_centre = True
            else:
                self.disable_six_in_centre = False

        self.num_iteration = 0
        for i, btn in enumerate(self.num_iterations_btn):
            if btn.GetValue() == True:
                self.num_iteration = self.num_iterations_opt[i]

        self.cluster_size = 0
        for i, btn in enumerate(self.cluster_size_btn):
            if btn.GetValue() == True:
                self.cluster_size = self.cluster_size_opt[i]

        self.min_neighbor_distance = 0
        for i, btn in enumerate(self.min_neighbor_distance_btn):
            if btn.GetValue() == True:
                self.min_neighbor_distance = self.min_neighbor_distance_opt[i]

        self.max_edge_planets = 0
        for i, btn in enumerate(self.max_edge_planets_btn):
            if btn.GetValue() == True:
                self.max_edge_planets = self.max_edge_planets_opt[i]

    def import_settings(self):
        settings_file = open(settings_path, "r")

        for line in settings_file:
            exec(line)

        settings_file.close()

    def save_settings(self):
        self.read_settings()
        settings_file = open(settings_path, "w")
        settings_file.write("self.num_players"+" = "+str(self.num_players)+"\n")
        settings_file.write("self.num_iterations" + " = " + str(self.num_iterations)+"\n")
        settings_file.write("self.cluster_size" + " = " + str(self.cluster_size)+"\n")
        settings_file.write("self.min_neighbor_distance" + " = " + str(self.min_neighbor_distance)+"\n")
        settings_file.write("self.max_edge_planets" + " = " + str(self.max_edge_planets)+"\n")
        settings_file.write("self.keep_core " + " = " + str(self.keep_core)+"\n")
        settings_file.write("self.disable_six_in_centre" + " = " + str(self.disable_six_in_centre)+"\n")
        settings_file.write("self.layout_3p_types" + " = " + str(self.layout_3p_types)+"\n")
        settings_file.write("self.radius" + " = " + str(self.radius) + "\n")
        settings_file.write("self.terra_param" + " = " + str(self.terra_param)+"\n")
        settings_file.write("self.gaia_param" + " = " + str(self.gaia_param)+"\n")
        settings_file.write("self.trans_param" + " = " + str(self.trans_param)+"\n")
        settings_file.write("self.range_factor" + " = " + str(self.range_factor)+"\n")
        settings_file.write("self.distribution_param" + " = " + str(self.distribution_param)+"\n")
        settings_file.write("self.density_param" + " = " + str(self.density_param)+"\n")
        settings_file.write("self.ratio_param" + " = " + str(self.ratio_param)+"\n")
        settings_file.close()

    def reset_settings(self):
        default_settings_file = open(default_settings_path, "r")
        settings_file = open(settings_path, "w")

        for line in default_settings_file:
            settings_file.write(line)

        default_settings_file.close()
        settings_file.close()

        self.Destroy()
        frame = MainFrame()
        frame.Show()

    def on_advanced(self, event):
        params = self.radius, self.terra_param, self.gaia_param, self.trans_param, self.range_factor, \
                 self.distribution_param, self.density_param, self.ratio_param
        advanced_settings = AdvancedSettings(self, params)
        advanced_settings.Show(True)

    def set_params(self, params):
        self.radius, self.terra_param, self.gaia_param, self.trans_param, self.range_factor, \
        self.distribution_param, self.density_param, self.ratio_param = params

    def on_randomize(self, event):
        n_players = int(self.num_players_options[self.num_player_box.GetSelection()])
        random_setup = RandomSetup(self, n_players)
        random_setup.Show(True)

    def on_make_map(self, event):
        self.read_settings()
        self.set_progress(0, 0, 0)

        map = Map(self.num_players,
                  True,
                  self.keep_core,
                  self.disable_six_in_centre,
                  self.layout_type_2p,
                  self.layout_type_3p)

        method = self.method_box.GetSelection()

        map.set_method(method)
        map.set_try_count(self.num_iteration)
        map.set_search_radius(self.radius)
        map.set_max_cluster_size(self.cluster_size)
        map.set_max_edge_planets(self.max_edge_planets)
        map.set_minimum_equal_range(self.min_neighbor_distance)

        if method == 0:
            #map.set_search_radius(2)
            map.set_method_0_params(self.terra_param, self.gaia_param, self.trans_param, self.range_factor)
            self.quality_description = "Variance"
        elif method == 1:
            #map.set_search_radius(3)
            map.set_method_1_params(self.distribution_param, self.density_param, self.ratio_param)
            self.quality_description = "Quality"
        elif method == 2:
            #map.set_search_radius(2)
            self.quality_description = "Av. size"

        self.enable_abort_btn(True)
        map.balance_map(self.set_progress, self.should_abort)
        if not map.get_has_valid_map():
            self.progress.SetLabel("Map progress: 100%")
            self.balance.SetLabel("NO VALID MAP FOUND")
            self.abort = False
            return
        map.set_to_balanced_map()
        map.calculate_balance(1)

        map.set_image_name(self.image_name.GetValue())
        map.save_image_map()
        full_image_name = image_path + self.image_name.GetValue() + image_format
        map_setup = MapSetup(self, full_image_name)
        map_setup.Show(True)

        #self.set_progress(0, 0, 0)
        self.abort = False

    def make_menu(self):
        pass

    def on_close(self, event):
        self.Destroy()

    def get_default_num_players(self):
        return self.default_num_players

    def set_progress(self, progress, balance, rejected):
        wx.Yield()
        self.quality_description
        if progress == 0:
            self.progress.SetLabel("Map progress: 0%")
            self.rejected.SetLabel("Rejected: 0")
            self.balance.SetLabel(self.quality_description + ": NA")
        elif progress < 100:
            self.progress.SetLabel("Map progress: " + str(progress) + "%")
            self.rejected.SetLabel("Rejected: " + str(rejected))
            self.balance.SetLabel(self.quality_description + ": {:06.4f}".format(balance))
        else:
            self.enable_abort_btn(False)
            self.progress.SetLabel("Creating image...")
            self.rejected.SetLabel("Rejected: " + str(rejected))
            self.balance.SetLabel(self.quality_description + ": {:06.4f}".format(balance))

    def enable_abort_btn(self, boolean):
        if boolean:
            self.btn_abort.SetBackgroundColour(wx.RED)
            self.btn_abort.Enable()
        else:
            self.btn_abort.SetBackgroundColour(None)
            self.btn_abort.Disable()

    def should_abort(self):
        return self.abort

    def on_abort(self, event=None):
        self.abort = True

    def on_error(self, error_message):
        PopupWindow(self, error_message, "WARNING", (300, 200))

class MapSetup(wx.Frame):
    def __init__(self, parent, image_path=default_map_path):
        super(MapSetup, self).__init__(parent, title="Generated Map", size=(1050, 850))

        ico = wx.Icon('images/hexagon_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        PhotoMaxHeight = 800
        self.SetBackgroundColour(wx.WHITE)

        # TODO: add save function to popup window with map

        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        NewH = PhotoMaxHeight
        NewW = PhotoMaxHeight * W / H

        img = img.Scale(NewW, NewH)
        imageMap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(imageMap, 0, wx.ALL, 5)

        self.SetSizer(hsizer)

        self.Centre()
        self.Show()


class RandomSetup(wx.Frame):
    def __init__(self, parent, num_players):
        super(RandomSetup, self).__init__(parent, title="Random Setup", size=(1200, 950))
        resize_factor = 0.8

        ico = wx.Icon('images/tech_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.SetBackgroundColour("#FFFFFF")

        hsizer_output = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_overall = wx.BoxSizer(wx.VERTICAL)

        vsizer_output = wx.BoxSizer(wx.VERTICAL)

        hsizer_tech_tracks = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_extra_tech = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_boosters = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_round_score = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_end_score = wx.BoxSizer(wx.VERTICAL)
        hsizer_round_and_end_score = wx.BoxSizer(wx.HORIZONTAL)

        for i, list in enumerate(list_of_pieces):
            random.shuffle(list)

        for i in range(6):
            if i == 0:  # Brown
                hsizer = wx.BoxSizer(wx.HORIZONTAL)
                brown_vsizer1 = wx.BoxSizer(wx.VERTICAL)
                brown_vsizer2 = wx.BoxSizer(wx.VERTICAL)

                path = image_path + list_of_pieces[0][0] + image_format
                brown_fed = wx.Image(path, wx.BITMAP_TYPE_ANY)

                W = brown_fed.GetWidth()
                H = brown_fed.GetHeight()
                local_factor = 0.8
                brown_fed = brown_fed.Scale(int(W * resize_factor * local_factor),
                                            int(H * resize_factor * local_factor))
                brown_fed_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(brown_fed))

                brown_vsizer1.Add(brown_fed_image, 1, wx.ALL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * resize_factor), int(H * resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * resize_factor), int(H * resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                brown_vsizer2.Add(img1_bm, 1, wx.ALL, 5)
                brown_vsizer2.Add(img2_bm, 1, wx.ALL, 5)

                hsizer.Add(brown_vsizer1, 1, wx.ALL)
                hsizer.Add(brown_vsizer2, 1, wx.ALL)

                hsizer_tech_tracks.Add(hsizer, 1, wx.EXPAND | wx.ALL, 0)
                hsizer_tech_tracks.AddSpacer(20)

            else: # all other tracks
                vsizer = wx.BoxSizer(wx.VERTICAL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * resize_factor), int(H * resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * resize_factor), int(H * resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                vsizer.Add(img1_bm, 1, wx.ALL, 5)
                vsizer.Add(img2_bm, 1, wx.ALL, 5)

                hsizer_tech_tracks.Add(vsizer, 1, wx.EXPAND | wx.ALL)

        vsizer_output.Add(hsizer_tech_tracks, 1, wx.EXPAND | wx.ALL, 5)

        # Extra tech tiles
        extra_tech = list_of_pieces[2][6:9]

        for i in range(len(extra_tech)):
            path = image_path + extra_tech[i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_extra_tech.Add(img_bm, 1, wx.ALL, 5)

        vsizer_output.Add(hsizer_extra_tech, 1, wx.EXPAND | wx.ALL, 5)

        # Boosters
        num_boosters = num_players + 3

        for i in range(num_boosters):
            path = image_path + list_of_pieces[4][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_boosters.Add(img_bm, 1, wx.ALL, 5)

        vsizer_output.Add(hsizer_boosters, 1, wx.EXPAND | wx.ALL, 5)

        # Round score
        for i in range(6):
            path = image_path + list_of_pieces[5][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_round_score.Add(img_bm, 1, wx.ALL, 5)

        # End game score
        for i in range(2):
            path = image_path + list_of_pieces[6][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            vsizer_end_score.Add(img_bm, 1, wx.ALL, 5)

        hsizer_round_and_end_score.Add(hsizer_round_score, 1, wx.ALL, 30)
        hsizer_round_and_end_score.Add(vsizer_end_score, 1, wx.ALL, 5)
        vsizer_output.Add(hsizer_round_and_end_score, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_output.Add(vsizer_output, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_overall.Add(hsizer_output, 0, wx.EXPAND)

        self.SetSizer(vsizer_overall)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Centre()
        self.Show()

    def OnEraseBackground(self, event):
        dc = event.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        bmp = wx.Bitmap(background_path)
        dc.DrawBitmap(bmp, 0, 0)

class AdvancedSettings(wx.Frame):
    def __init__(self, parent, params):
        super(AdvancedSettings, self).__init__(parent, title="Advanced Settings", size=(800, 970))
        self.parent = parent
        ico = wx.Icon('images/gear_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.SetBackgroundColour("#FFFFFF")

        path = information_blue_path
        img_info = wx.Image(path, wx.BITMAP_TYPE_ANY)
        W = img_info.GetWidth()
        H = img_info.GetHeight()
        img_info = img_info.Scale(int(W * 0.15), int(H * 0.15))

        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        header_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        small_header_font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        self.radius, self.terra_param, self.gaia_param, self.trans_param, self.range_factor, \
                 self.distribution_param, self.density_param, self.ratio_param = params

        hsizer_overall = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_settings = wx.BoxSizer(wx.VERTICAL)
        vsizer_info = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        radius_txt = wx.StaticText(self, 0, "Relevant neighbor radius")
        hsizer.Add(radius_txt, 4, wx.EXPAND | wx.ALL, 5)

        self.radius_opt = [1, 2, 3]
        self.radius_btn = []
        for i, value in enumerate(self.radius_opt):
            if i == 0:
                btn = wx.RadioButton(self, label=str(value), style=wx.RB_GROUP)
            else:
                btn = wx.RadioButton(self, label=str(value))
            self.radius_btn.append(btn)
            hsizer.Add(btn, 1)
            if value == self.radius:
                btn.SetValue(True)

        img_info_radius = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_radius.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_radius)
        hsizer.Add(img_info_radius, 0, wx.BOTTOM)

        vsizer_settings.Add(hsizer, 0, wx.EXPAND | wx.ALL, 10)

        happy_header = wx.StaticText(self, 1, "Neighbour Quality Settings")
        happy_header.SetFont(header_font)
        vsizer_settings.Add(happy_header, 0, wx.EXPAND | wx.ALL, 10)

        txt = """This method loops over the planets and sums up the
neighbour quality of each planet type. The goal is that each
planet type has a similar quality of its neighbours"""
        text = wx.StaticText(self, 0, txt)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(text, 1, wx.EXPAND | wx.ALL, 0)

        img_info_neighbor = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
        img_info_neighbor.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver_neighbor)
        hsizer.Add(img_info_neighbor, 0, wx.BOTTOM)

        vsizer_settings.Add(hsizer, 0, wx.EXPAND | wx.ALL, 10)

        vsizer_sliders = wx.BoxSizer(wx.VERTICAL)
        slider_padding = 0
        sliders = [["Terraform step 0 (Home):", 0, 100, self.terra_param[0], "onMouseOver_terraform_0"],
                   ["Terraform step 1:", 0, 100, self.terra_param[1],"onMouseOver_terraform_1"],
                   ["Terraform step 2:", 0, 100, self.terra_param[2], "onMouseOver_terraform_2"],
                   ["Terraform step 3:", 0, 100, self.terra_param[3], "onMouseOver_terraform_3"],
                   ["Gaia planet:", 0, 100, self.gaia_param, "onMouseOver_gaia"],
                   ["Trans-Dim planet:", 0, 100, self.trans_param, "onMouseOver_transdim"],
                   ["Neighbor range 1:", 0, 100, self.range_factor[1], "onMouseOver_range_1"],
                   ["Neighbor range 2:", 0, 100, self.range_factor[2], "onMouseOver_range_2"],
                   ["Neighbor range 3:", 0, 100, self.range_factor[3], "onMouseOver_range_3"]]

        self.happy_sliders = []

        for txt, min, max, default, mouse_funk in sliders:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)

            text = wx.StaticText(self, 0, txt)
            slider = wx.Slider(self, value=default, minValue=float(min), maxValue=float(max),
                               style=wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL)
            self.happy_sliders.append(slider)
            hsizer.Add(text, 1, wx.EXPAND | wx.ALL)
            hsizer.Add(slider, 1, wx.EXPAND | wx.ALL)

            img_info_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
            img_info_bm.Bind(wx.EVT_ENTER_WINDOW, getattr(self, mouse_funk))
            hsizer.Add(img_info_bm, 0, wx.BOTTOM)

            vsizer_sliders.Add(hsizer, 0, wx.EXPAND | wx.ALL, slider_padding)

        vsizer_settings.Add(vsizer_sliders, 0, wx.EXPAND | wx.ALL, 10)

        dist_header = wx.StaticText(self, 1, "Distribution Settings")
        dist_header.SetFont(header_font)
        vsizer_settings.Add(dist_header, 0, wx.EXPAND | wx.ALL, 10)

        txt = """This method tries to get an equal distribution of planets,
based on planet density, planet type or both."""
        text = wx.StaticText(self, 0, txt)
        vsizer_settings.Add(text, 0, wx.EXPAND | wx.ALL, 10)

        vsizer_sliders = wx.BoxSizer(wx.VERTICAL)
        sliders = [["Distribution Type Weight:", 0, 100, self.distribution_param, "onMouseOver_distribution"],
                   ["Planet Density Dropoff Scale:", 0, 100, self.density_param, "onMouseOver_density"],
                   ["Type Ratio Dropoff Scale:", 0, 100, self.ratio_param, "onMouseOver_type"]]

        self.density_sliders = []

        for txt, min, max, default, mouse_funk in sliders:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)

            text = wx.StaticText(self, 0, txt)
            slider = wx.Slider(self, value=default, minValue=float(min), maxValue=float(max),
                               style=wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL)
            self.density_sliders.append(slider)
            hsizer.Add(text, 1, wx.EXPAND | wx.ALL)
            hsizer.Add(slider, 1, wx.EXPAND | wx.ALL)

            img_info_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img_info))
            img_info_bm.Bind(wx.EVT_ENTER_WINDOW, getattr(self, mouse_funk))
            hsizer.Add(img_info_bm, 0, wx.BOTTOM)

            vsizer_sliders.Add(hsizer, 0, wx.EXPAND | wx.ALL, slider_padding)

        vsizer_settings.Add(vsizer_sliders, 0, wx.EXPAND | wx.ALL, 10)

        btn_apply = wx.Button(self, wx.ID_APPLY, label="Apply", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_apply, btn_apply)

        hsizer = wx.BoxSizer(wx.HORIZONTAL  )
        btn_save = wx.Button(self, wx.ID_SAVE, label="Save settings", size=(60, 40))
        self.Bind(wx.EVT_BUTTON, self.on_save_settings, btn_save)
        btn_reset = wx.Button(self, wx.ID_RESET, label="Reset settings", size=(60, 40))
        self.Bind(wx.EVT_BUTTON, self.on_reset_settings, btn_reset)
        hsizer.Add(btn_save, 1, wx.EXPAND | wx.ALL, 0)
        hsizer.Add(btn_reset, 1, wx.EXPAND | wx.ALL, 0)

        vsizer_settings.Add(btn_apply, 0, wx.EXPAND | wx.ALL, 10)
        vsizer_settings.Add(hsizer, 0, wx.EXPAND | wx.ALL, 10)

   #      # Information text
   #      info_padding = 5
   #
   #      settings_header = wx.StaticText(self, 1, "General settings")
   #      settings_header.SetFont(header_font)
   #      vsizer_info.Add(settings_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      info = [["Relevant neighbor radius:", "   Used in the two first methods to define area of influence"]]
   #
   #      for method, description in info:
   #          small_header = wx.StaticText(self, 1, method)
   #          small_header.SetFont(small_header_font)
   #          vsizer_info.Add(small_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #          info_text = wx.StaticText(self, 1, description)
   #          vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      settings_header = wx.StaticText(self, 1, "Neighbour Quality Settings")
   #      settings_header.SetFont(header_font)
   #      vsizer_info.Add(settings_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      info = [["Terraform:",
   #               """   The quality of a neighbour based on how much it costs to terraform"""],
   #              ["Gaia:",
   #               """   The quality of a Gaia planet"""],
   #              ["Trans-Dim:",
   #               """   The quality of a Trans-Dim planet"""],
   #              ["Range Factor:",
   #               """   How the range to a neighbour effects the quality.
   # Quality value for each neighbour is multiplied by the range factor
   # for the given distance"""]]
   #
   #      for method, description in info:
   #          small_header = wx.StaticText(self, 1, method)
   #          small_header.SetFont(small_header_font)
   #          vsizer_info.Add(small_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #          info_text = wx.StaticText(self, 1, description)
   #          vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      settings_header = wx.StaticText(self, 1, "Distribution Settings")
   #      settings_header.SetFont(header_font)
   #      vsizer_info.Add(settings_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #
   #      info = [["Distribution Type:",
   #               """    - 100 will optimize for planet density
   #  - 0 will optimize for planet types.
   #  - A value in between will optimize for a mix"""],
   #              ["Planet Density and Type Ratio Dropoff Scale (0-100):",
   #               """   How bad it is to differ from optimal value. A lower number gives
   # a smaller punishement for having a value outside the optimal."""]]
   #
   #      for method, description in info:
   #          small_header = wx.StaticText(self, 1, method)
   #          small_header.SetFont(small_header_font)
   #          vsizer_info.Add(small_header, 0, wx.EXPAND | wx.ALL, info_padding)
   #          info_text = wx.StaticText(self, 1, description)
   #          vsizer_info.Add(info_text, 0, wx.EXPAND | wx.ALL, info_padding)

        hsizer_overall.Add(vsizer_settings, 1, wx.EXPAND, 40)
        # hsizer_overall.Add(vsizer_info, 1, wx.EXPAND, 20)
        self.SetSizer(hsizer_overall)

        self.Centre()
        self.Show()

    def onMouseOver_radius(self, event):
        string = """Used in the two first methods to define area of influence"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_neighbor(self, event):
        string = """Appreciation value for each neighbour is multiplied by the range appreciation for the given distance"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_terraform_0(self, event):
        string = """The appreciation of a home planet nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_terraform_1(self, event):
        string = """The appreciation of a planet a terraforming step 1 away nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_terraform_2(self, event):
        string = """The appreciation of a planet a terraforming step 2 away nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_terraform_3(self, event):
        string = """The appreciation of a planet a terraforming step 3 away nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_gaia(self, event):
        string = """The appreciation of a Gaia planet nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_transdim(self, event):
        string = """The appreciation of a Trans-Dim planet nearby."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_range_1(self, event):
        string = """The appreciation of a planet a distance 1 away"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_range_2(self, event):
        string = """The appreciation of a planet a distance 2 away"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_range_3(self, event):
        string = """The appreciation of a planet a distance 3 away"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_distribution(self, event):
        string = """- 100 will optimize for planet density
    - 0 will optimize for planet types.
    - A value in between will optimize for a mix"""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_density(self, event):
        string = """How bad it is to differ from optimal value. A lower number gives
   a smaller punishement for having a value outside the optimal."""
        event.GetEventObject().SetToolTip(string)

    def onMouseOver_type(self, event):
        string = """How bad it is to differ from optimal value. A lower number gives
   a smaller punishement for having a value outside the optimal."""
        event.GetEventObject().SetToolTip(string)

    def on_apply(self, event=None):
        radius_param = 0
        for i, btn in enumerate(self.radius_btn):
            if btn.GetValue() == True:
                radius_param = self.radius_opt[i]

        terra_param = [self.happy_sliders[0].GetValue(), self.happy_sliders[1].GetValue(),
                       self.happy_sliders[2].GetValue(), self.happy_sliders[3].GetValue()]
        gaia_param = self.happy_sliders[4].GetValue()
        trans_param = self.happy_sliders[5].GetValue()
        range_factor = [100, self.happy_sliders[6].GetValue(),
                        self.happy_sliders[7].GetValue(), self.happy_sliders[8].GetValue()]

        distribution_param = self.density_sliders[0].GetValue()/100.

        density_param = self.density_sliders[1].GetValue()

        ratio_param = self.density_sliders[2].GetValue()

        if ratio_param > 20:
            self.on_error("It is not reccomended with a Type Ratio Dropoff Scale of more than 20")

        params = radius_param, terra_param, gaia_param, trans_param, range_factor,\
                 distribution_param, density_param, ratio_param

        self.parent.set_params(params)
        self.on_close()

    def on_save_settings(self, event=None):
        self.on_apply()
        self.parent.save_settings()

    def on_reset_settings(self, event=None):
        self.parent.reset_settings()

    def on_error(self, error_message):
        PopupWindow(self, error_message, "WARNING", (300, 200))

    def on_close(self, event=None):
        self.Destroy()


class PopupWindow(wx.PopupWindow):
    def __init__(self, parent, message, header_txt = None, size=(500, 300)):
        wx.PopupWindow.__init__(self, parent, wx.SIMPLE_BORDER)

        default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetFont(default_font)

        self.SetSize(size)
        width = size[0]
        height = size[1]

        if header_txt:
            header_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
            header = wx.TextCtrl(self, -1, header_txt, pos=(20, 20), style=wx.TE_READONLY | wx.BORDER_NONE)
            header.SetFont(header_font)

            text = wx.TextCtrl(self, -1, message, size=(width - 40, height - 110), pos=(20, 50),
                               style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE)
        else:
            text = wx.TextCtrl(self, -1, message, size=(width - 40, height - 80), pos=(20, 20),
                               style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE)

        text.SetBackgroundColour("#f0f0f0")

        close_btn = wx.Button(self, wx.ID_CLOSE, label="Close", pos=(width - 120, height - 60), size=(100, 40))
        self.Bind(wx.EVT_BUTTON, self.on_close, close_btn)

        self.CenterOnParent(dir=wx.BOTH)
        self.Show()

    def on_close(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
