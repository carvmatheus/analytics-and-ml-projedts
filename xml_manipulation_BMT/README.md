# XML Parser
The XML Parser is a Python module for parsing and transforming XML files. It uses the minidom and xml.etree.ElementTree libraries to parse and manipulate XML files.

## Usage
To use the module, create an instance of the XmlParser class, passing in the input path, output path, and file name:
```
from XMLParser import XmlParser

xml_parser = XmlParser(input_path='./input/', output_path='./output/', file='example.xml')
```

To parse an element from the XML file and write it to a new file, call the parse_element() method of the XmlParser instance and pass in the name of the element:
```
xml_parser.parse_element('AUTHOR')
```

This will parse all AUTHOR elements from the XML file and write them to a new file called AUTHOR.xml in the output directory.

## Customization
The module is customizable to parse different elements from the XML file. To parse a different element, modify the parse_element() method by changing the element parameter and the start and end tags for the element:

```
if element == 'TITLES': 
    start_element_tag = '<TITLE>'
    end_element_tag = '</TITLE>'
    element_name = 'TITLE'
```
## Requirements
* Python 3.5 or later
* minidom library
* xml.etree.ElementTree library