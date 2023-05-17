from xml.dom import minidom
import os
import xml.etree.ElementTree as ET

class XmlParser:
    def __init__(self, input_path, output_path, file='cf79.xml'):
        self.input_path = input_path
        self.output_path = output_path
        self.file = file

    def parse_element(self, element):
        # Parse file to minidom object
        xmldoc = minidom.parse(os.path.join(self.input_path, self.file))
        if element == 'autores': 
            start_element_tag = '<AUTHOR>'
            end_element_tag = '</AUTHOR>'
            element_name = 'AUTHOR'
        elif element == 'titulos' :
            start_element_tag = '<TITLE>'
            end_element_tag = '</TITLE>'
            element_name = 'TITLE'

        # Get all tags
        element_obj_list = xmldoc.getElementsByTagName(element_name)
        treated_elements = [f'{start_element_tag}{element.firstChild.nodeValue}{end_element_tag}' for element in element_obj_list \
            if element.firstChild.nodeType == element.TEXT_NODE]

        # Create FILE element and append treated elements to it
        file_element = ET.Element('FILE')

        # Populate file_element
        [file_element.append(ET.fromstring(element_text)) for element_text in treated_elements]

        # Write the final XML to a file
        ET.ElementTree(file_element).write(os.path.join(self.output_path, f'{element}.xml'))

if __name__ == '__main__':
    parser = XmlParser(input_path='input', output_path='output')
    parser.parse_element('autores')