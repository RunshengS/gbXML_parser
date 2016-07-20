'''
Created on Jun 30, 2016

@author: t_songr
'''
import xml.etree.ElementTree as ET
from collections import OrderedDict
import csv

class gbXMLparser():
    def __init__(self, file_path):
        self._root = ET.parse(file_path).getroot()
        
        self.resutls_dict = OrderedDict()

        self.get_basic_info(self._root)
        self.get_surface_info(self._root)
    
    def get_basic_info(self, _root):
        '''
        Get the basic information of the building XML file:
        Unit, BuildingType, Latitude, Longitude, City and Country,
        designHeatWeathIdRef and designCoolWeathIdRef
        
        Input: Root, the root of the xml file
        Output: update the self.results_dict
        '''
        # getting sub-roots:
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _building = _campus.find('{http://www.gbxml.org/schema}Building')
        _location = _campus.find('{http://www.gbxml.org/schema}Location')
        
        # The unit that users used for the project
        Unit = _root.attrib['lengthUnit']
        if Unit == 'Feet':
            Unit = 'IP'
        elif Unit == 'Meters':
            Unit = 'SI'
        self.resutls_dict['Unit'] = Unit

            
        # Building Type:
        BuildingType = _building.attrib['buildingType']
        self.resutls_dict['BuildingType'] = BuildingType

        
        # Latitude and Longitude:
        Longitude = _location.find('{http://www.gbxml.org/schema}Longitude').text
        Latitude = _location.find('{http://www.gbxml.org/schema}Latitude').text
        self.resutls_dict['Longitude'] = Longitude
        self.resutls_dict['Latitude'] = Latitude

        
        # City and County:
        CityAndCountry = _location.find('{http://www.gbxml.org/schema}Name').text
        self.resutls_dict['CityAndCountry'] = CityAndCountry

        
        # Climate Zone:
        designHeatWeathIdRef = _campus.attrib['designHeatWeathIdRef']
        designCoolWeathIdRef = _campus.attrib['designCoolWeathIdRef']
        self.resutls_dict['designHeatWeathIdRef'] = designHeatWeathIdRef
        self.resutls_dict['designCoolWeathIdRef'] = designCoolWeathIdRef

        
    
    def get_surface_info(self, _root):
        '''
        Get the Information of Exterior Wall
        '''
        # Get the sub-roots:
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        TotalWallArea = 0 # Total Wall Area for the entire building
        TotalWindowArea = 0 # Total Window Area for the entire building
        TotalHightArea = 0 # The total area times the level of the floor
        for eachSurface in _surface_all:
            
            if eachSurface.attrib['surfaceType'] == 'ExteriorWall':

                this_total_area = 0 # Total Surface Area for this Surface 
                
                this_wall_area = 0 # Total Wall Area for this Surface
                this_window_area = 0    # Total Window Area for this Surface
                this_angle = 0  # The direction of this surface in degree
                
                this_RectangularGeometry_all = eachSurface.findall('{http://www.gbxml.org/schema}RectangularGeometry')
                this_window_all = eachSurface.findall('{http://www.gbxml.org/schema}Opening')

                for eachWall in this_RectangularGeometry_all:

                    this_wall_Azimuth = eachWall.find('{http://www.gbxml.org/schema}Azimuth').text
                    this_wall_Height = eachWall.find('{http://www.gbxml.org/schema}Height').text
                    this_wall_Width = eachWall.find('{http://www.gbxml.org/schema}Width').text

                    this_total_area = float(this_wall_Height) *  float(this_wall_Width)
                    this_angle  = float(this_wall_Azimuth) # only has one angle for one surface
                
                for eachWindow in this_window_all:
                   
                    this_geo = eachWindow.find('{http://www.gbxml.org/schema}RectangularGeometry').text
                    this_window_Height = this_geo.find('{http://www.gbxml.org/schema}Height').text
                    this_window_Width = this_geo.find('{http://www.gbxml.org/schema}Width').text
                    this_window_area = float(this_window_Height) * float(this_window_Width)
                
                this_wall_area = this_total_area - this_window_area
                TotalWallArea += this_wall_area
                TotalWindowArea += this_window_area
                
            self.resutls_dict['TotalWallArea'] = TotalWallArea
            self.resutls_dict['TotalWindowArea'] = TotalWindowArea
        

        
    def dump_to_csv(self, file_name):
        '''
        Save to file
        '''
        with open(file_name, 'wb') as myfile:
            thisWriter = csv.writer(myfile)
            thisWriter.writerow(self.resutls_dict.keys())
            thisWriter.writerow(self.resutls_dict.values())

if __name__ == '__main__':
    file = './data/gbXMLStandard.xml'
    thisParser = gbXMLparser(file)
    thisParser.dump_to_csv('test.csv')
   
    
    
    
    
    
    