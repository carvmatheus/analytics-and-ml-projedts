import unittest
import os
from xml.dom import minidom

from XMLParser import XmlParser


class TestXmlParser(unittest.TestCase):

    def setUp(self):
        self.input_path = './test_files/'
        self.output_path = './test_output/'
        self.file = 'test_file.xml'

        # Create test input file
        with open(os.path.join(self.input_path, self.file), 'w') as f:
            f.write('<ROOT><AUTHOR>John Doe</AUTHOR><AUTHOR>Jane Smith</AUTHOR><TITLE>Example Title</TITLE></ROOT>')

    def test_parse_element_authors(self):
        parser = XmlParser(input_path=self.input_path, output_path=self.output_path, file=self.file)
        parser.parse_element('autores')

        # Verify output file contents
        expected_output = '<FILE><AUTHOR>John Doe</AUTHOR><AUTHOR>Jane Smith</AUTHOR></FILE>'
        with open(os.path.join(self.output_path, 'autores.xml'), 'r') as f:
            output_contents = f.read()

        self.assertEqual(expected_output, output_contents)

    def test_parse_element_titles(self):
        parser = XmlParser(input_path=self.input_path, output_path=self.output_path, file=self.file)
        parser.parse_element('titulos')

        # Verify output file contents
        expected_output = '<FILE><TITLE>Example Title</TITLE></FILE>'
        with open(os.path.join(self.output_path, 'titulos.xml'), 'r') as f:
            output_contents = f.read()

        self.assertEqual(expected_output, output_contents)

    def tearDown(self):
        # Clean up test files
        os.remove(os.path.join(self.input_path, self.file))
        os.remove(os.path.join(self.output_path, 'autores.xml'))
        os.remove(os.path.join(self.output_path, 'titulos.xml'))


if __name__ == '__main__':
    unittest.main()