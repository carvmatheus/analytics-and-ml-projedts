from XMLParser import XmlParser

xml_parser = XmlParser(input_path='./files/', output_path='./output/', file='cf79.xml')
xml_parser.parse_element('autores')
xml_parser.parse_element('titulos')