#!/usr/bin/env python
#
# Copyright (C)     2018 Dennis Wijngaarden
#                    2018 Freek van Tienen <freek.v.tienen@gmail.com>
#               
#
# This file is part of paparazzi.
#
# paparazzi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# paparazzi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with paparazzi; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.
#

from os import path, getenv
import sys

import numpy as np
import shapely.geometry as geometry

# if PAPARAZZI_SRC or PAPARAZZI_HOME not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")
sys.path.append(PPRZ_HOME + "/var/lib/python") # pprzlink

from pprzlink.message import PprzMessage
from pprzlink.ivy import IvyMessagesInterface
from pprz_math import geodetic

import traffic_scenario

class RealtimeResolution(object):
    def __init__(self, circular_zones, ltp_def):
        self.realtime_scenario = traffic_scenario.TrafficScenario(circular_zones, ltp_def)
        
    def init_realtime(self):
        """
        Initialize the real time resolutions
        """
        self.realtime_scenario.init_SSD_plot()
        
    def run_realtime(self, tla, wind, detection_margin, airspeed, aircraft, traffic_events):
        """
        run the realtime_resolutions
        """
        self.realtime_scenario.update_traffic_scenario(aircraft, traffic_events)
        
        if self.realtime_scenario.Traffic.ntraf > 1:
#            try:
            self.realtime_scenario.detect_conflicts(tla, wind, detection_margin, airspeed)
            self.realtime_scenario.plot_SSD() 
#            except: # All errors to overcome pyclipper error UnboundLocalError: # When simulated aircraft are too far
#                pass # Do nothing
                
class ResolutionFinder(object):
    def __init__(self, circular_zones, ref_utm_i, ltp_def):
        self.extrapolated_scenario = traffic_scenario.ExtrapolatedScenario(circular_zones, ref_utm_i, ltp_def)
        self.conflict_counter = 0
    
#    def resolution_on_leg(self, from_point_enu, to_point_enu, groundspeed, margin, aircraft, traffic_events, wind, altitude, geofence, zones, max_tla):
#        conflict_counter_th = 4 # loops     
#        avoidance_time_th = 30. # [s]
#        hdg_diff_th = 30.
#        avoid_dist_min = 1000. # [m]
#        max_iter_steps = 4
#        
#        dx = to_point_enu.x - from_point_enu.x
#        dy = to_point_enu.y - from_point_enu.y
#        hdg = np.rad2deg(np.arctan2(dx, dy)) % 360.            
#        
#        self.extrapolated_scenario.update_traffic_scenario(aircraft, traffic_events, hdg, 0.)
#        time_to_arrive_at_point = self.time_to_arrive_at_point(from_point_enu, to_point_enu, groundspeed)
#        resolutions = self.extrapolated_scenario.detect_conflicts(time_to_arrive_at_point, wind, margin)
#        
#        print(self.conflict_counter)        
#        sys.stdout.flush()
#        
#        if ((resolutions[0] == 'conflict') or (resolutions[0] == 'nosol')):
#            if ((self.conflict_counter < conflict_counter_th) or (resolutions[0] == 'nosol')):
#                self.conflict_counter = self.conflict_counter + 1
#                return 'free'
#        if (resolutions[0] == 'free'):
#            self.conflict_counter = 0
#            return 'free'
#        
#        if ((self.conflict_counter >= conflict_counter_th) and (resolutions[0] != 'nosol') and (time_to_arrive_at_point > avoidance_time_th)):
#            #find resolutions
#            resolution_points = []
#            distances = []
#            half_leg_distance = enu_distance(from_point_enu, to_point_enu) / 2.
#            avoid_dist = min(half_leg_distance, avoid_dist_min)
#            
#            for i in range(len(resolutions[1])):
#                # stop when not within thresholds
#                x_res = resolutions[1][i]
#                y_res = resolutions[2][i]
#                hdg_res = np.rad2deg(np.arctan2(x_res, y_res)) % 360.
#                hdg_diff = calc_absolute_hdg_diff(hdg, hdg_res)
#                if (hdg_diff > hdg_diff_th):
#                    print ("hdg diff to big: ", hdg_diff)
#                    sys.stdout.flush()
#                    return 'nosol'
#                
#                for j in range(max_iter_steps):
#                    resolution_dist = avoid_dist/max_iter_steps * (j + 1)
#                    dt = resolution_dist / groundspeed
#                    new_from_point_enu = geodetic.EnuCoor_f(from_point_enu.x + np.sin(np.deg2rad(hdg_res)) * resolution_dist, from_point_enu.y + np.cos(np.deg2rad(hdg_res)) * resolution_dist, altitude)
#                
#                    linestring_to = geometry.LineString([(from_point_enu.x, from_point_enu.y), (new_from_point_enu.x, new_from_point_enu.y)])
#                    linestring_from = geometry.LineString([(new_from_point_enu.x, new_from_point_enu.y), (to_point_enu.x, to_point_enu.y)])
#                    
#                    geofence_polygon = geometry.Polygon(enu_lst_to_polygon(geofence))
#                    
#                    if ((geofence_polygon.contains(linestring_to) == False) or (geofence_polygon.contains(linestring_from) == False)):
#                        # Non valid solution
#                        continue
#            
#                    for zone in zones:
#                        zone_polygon = geometry.Polygon(enu_lst_to_polygon(zone.enu_points))
#                        if (linestring_to.intersects(zone_polygon) or (linestring_from.intersects(zone_polygon))):
#                            # Non valid solution
#                            continue
#                    
#                    dx_target = to_point_enu.x - new_from_point_enu.x
#                    dy_target = to_point_enu.y - new_from_point_enu.y
#                    
#                    hdg_target = np.rad2deg(np.arctan2(dx_target, dy_target)) % 360.
#                    
#                    self.extrapolated_scenario.update_traffic_scenario(aircraft, traffic_events, hdg_target, dt)
#                    tla_target = min(self.time_to_arrive_at_point(new_from_point_enu, to_point_enu, groundspeed), max_tla)
#                
#                    conflict = self.extrapolated_scenario.detect_conflicts(tla_target, wind, margin) # mayve detection margin good as well
#                
#                    if (conflict[0] == 'free'):
#                        resolution_points.append(new_from_point_enu)
#                        distance = enu_distance(new_from_point_enu, from_point_enu) + enu_distance(new_from_point_enu, to_point_enu)
#                        distances.append(distance)
#                    
#            if len(resolution_points) > 0:
#                resolution_point = resolution_points[np.argmin(distances)]
#                self.conflict_counter = 0
#                print("resolution ooint")
#                sys.stdout.flush()
#                return resolution_point
#            else:
#                print("nosol")
#                sys.stdout.flush()
#                return 'nosol' 
#        else:
#            return 'free'
            
    def resolution_on_leg(self, from_point_enu, to_point_enu, groundspeed, margin, aircraft, traffic_events, wind, altitude, geofence, zones, max_tla):
        conflict_counter_th = 3 # loops     
        avoidance_time_th = 30. # [s]
        hdg_diff_th = 30.
        avoid_dist_min = 1000. # [m]

        
        dx = to_point_enu.x - from_point_enu.x
        dy = to_point_enu.y - from_point_enu.y
        hdg = np.rad2deg(np.arctan2(dx, dy)) % 360.            
        
        self.extrapolated_scenario.update_traffic_scenario(aircraft, traffic_events, hdg, 0.)
        time_to_arrive_at_point = self.time_to_arrive_at_point(from_point_enu, to_point_enu, groundspeed)
        resolutions = self.extrapolated_scenario.detect_conflicts(min(max_tla, time_to_arrive_at_point), wind, margin)
        
        print(self.conflict_counter)        
        sys.stdout.flush()
        
        if ((resolutions[0] == 'conflict') or (resolutions[0] == 'nosol')):
            if ((self.conflict_counter < conflict_counter_th) or (resolutions[0] == 'nosol')):
                self.conflict_counter = self.conflict_counter + 1
                return 'free'
        if (resolutions[0] == 'free'):
            self.conflict_counter = 0
            return 'free'
        
        if ((self.conflict_counter >= conflict_counter_th) and (resolutions[0] != 'nosol') and (time_to_arrive_at_point > avoidance_time_th)):
            #find resolutions
            resolution_points = []
            distances = []
            half_leg_distance = enu_distance(from_point_enu, to_point_enu) / 2.
            avoid_dist = min(half_leg_distance, avoid_dist_min)
            
            for i in range(len(resolutions[1])):
                # stop when not within thresholds
                x_res = resolutions[1][i]
                y_res = resolutions[2][i]
                hdg_res = np.rad2deg(np.arctan2(x_res, y_res)) % 360.
                hdg_diff = calc_absolute_hdg_diff(hdg, hdg_res)
                if (hdg_diff > hdg_diff_th):
                    print ("hdg diff to big: ", hdg_diff)
                    sys.stdout.flush()
                    break
                
                resolution_dist = avoid_dist
                dt = resolution_dist / groundspeed
                new_from_point_enu = geodetic.EnuCoor_f(from_point_enu.x + np.sin(np.deg2rad(hdg_res)) * resolution_dist, from_point_enu.y + np.cos(np.deg2rad(hdg_res)) * resolution_dist, altitude)
                
                linestring_to = geometry.LineString([(from_point_enu.x, from_point_enu.y), (new_from_point_enu.x, new_from_point_enu.y)])
                linestring_from = geometry.LineString([(new_from_point_enu.x, new_from_point_enu.y), (to_point_enu.x, to_point_enu.y)])
                    
                geofence_polygon = geometry.Polygon(enu_lst_to_polygon(geofence))
                    
                if ((geofence_polygon.contains(linestring_to) == False) or (geofence_polygon.contains(linestring_from) == False)):
                    # Non valid solution
                    continue
        
                for zone in zones:
                    zone_polygon = geometry.Polygon(enu_lst_to_polygon(zone.enu_points))
                    if (linestring_to.intersects(zone_polygon) or (linestring_from.intersects(zone_polygon))):
                        # Non valid solution
                        continue
                
                dx_target = to_point_enu.x - new_from_point_enu.x
                dy_target = to_point_enu.y - new_from_point_enu.y
                
                hdg_target = np.rad2deg(np.arctan2(dx_target, dy_target)) % 360.
                resolution_points.append(new_from_point_enu)
                distance = enu_distance(new_from_point_enu, from_point_enu) + enu_distance(new_from_point_enu, to_point_enu)
                distances.append(distance)
                    
            if len(resolution_points) > 0:
                resolution_point = resolution_points[-1]
                self.conflict_counter = 0
                print("resolution point")
                sys.stdout.flush()
                return resolution_point
            else:
                print("nosol")
                sys.stdout.flush()
                return 'nosol' 
        else:
            return 'free'
                    
    def time_to_arrive_at_point(self, from_point_enu, to_point_enu, groundspeed):
        dist = np.sqrt((from_point_enu.x - to_point_enu.x) ** 2 + (from_point_enu.y - to_point_enu.y) ** 2)
        V = groundspeed
        if V != 0:
            time = dist/V
        else:
            time = 5.*60.
        return time
        
def calc_absolute_hdg_diff(hdg1, hdg2):
    diff = abs(hdg1 - hdg2)
    diff = 180. - abs(180. - abs(hdg1 - hdg2) % 360.)
    return diff
        
def enu_distance(enu1, enu2):
    distance = np.sqrt((enu1.x - enu2.x) ** 2 + (enu1.y - enu2.y) ** 2)
    return distance
    
def enu_lst_to_polygon(enu_lst):
    coords = []
    for enu in enu_lst:
        coords.append((enu.x, enu.y))
    return coords