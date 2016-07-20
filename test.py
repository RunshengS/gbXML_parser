'''
Created on Jun 30, 2016

@author: t_songr
'''
import xml.etree.ElementTree as ET


def gbxmlread(path):
    # Parse and store the gbXML file in tree
    _root = ET.parse(path).getroot()
    _campus = _root.find('{http://www.gbxml.org/schema}Campus')
    _building = _campus.find('{http://www.gbxml.org/schema}Building')
    _location = _campus.find('{http://www.gbxml.org/schema}Location')
    
#     designHeatWeathIdRef = root.attrib['designHeatWeathIdRef']
#     designCoolWeathIdRef = root.attrib['designCoolWeathIdRef']
#     Unit = _root.attrib['lengthUnit']
#     BuildingType = _building.attrib['buildingType']
    
#     Longitude = _location.find('{http://www.gbxml.org/schema}Longitude').text
#     Latitude = _location.find('{http://www.gbxml.org/schema}Latitude').text
#     CityAndCountry = location.attrib['Name']
#     CityAndCountry = _location.find('{http://www.gbxml.org/schema}Name').text
    
    _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
    for eachSurface in _surface_all:
        window = eachSurface.find('{http://www.gbxml.org/schema}PlanarGeometry')
        print window
        raw_input()

        
        
        
        
if __name__ == '__main__':
    file_path = './data/gbXMLStandard.xml'
    gbxmlread(file_path)