import unittest
import xml2json
import optparse
import json
import os

xmlstring = ""
options = None

class SimplisticTest(unittest.TestCase):

    def setUp(self):
        global xmlstring, options
        filename = os.path.join(os.path.dirname(__file__), 'xml_ns2.xml')
        xmlstring = open(filename).read()
        options = optparse.Values({"pretty": False})

    def test_default_namespace_attribute(self):
        strip_ns = 0
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        # check string
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}tr") != -1)
        self.assertTrue(json_string.find("@class") != -1)

        # check the simple name is not exist
        json_data = json.loads(json_string)
        self.assertFalse("table" in json_data["root"])

    def test_strip_namespace(self):
        strip_ns = 1
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        json_data = json.loads(json_string)

        # namespace is stripped
        self.assertFalse(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)

        # TODO , attribute shall be kept
        #self.assertTrue(json_string.find("@class") != -1)

        #print json_data["root"]["table"]
        #print json_data["root"]["table"][0]["tr"]
        self.assertTrue("table" in json_data["root"])
        self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])

    def test_json2xml(self):
        json_data = '{"e": { "@name": "value"}}' #3
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e name="value" />')

        json_data = '{"e": null}' #1
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e />')

        json_data = '{"e": { "#text": "text", "a": "text"}}' #7
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e>text<a>text</a></e>')

        json_data = '{"e": { "a": ["text", "text"]}}' #6
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e><a>text</a><a>text</a></e>')

        json_data = '{"e": { "a": "text", "b": "text"}}' #5
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e><a>text</a><b>text</b></e>')

    def test_json2xml3(self):
        json_data = '{"e": { "@name": "value", "#text": "text" }}' #4
        xml_string = xml2json.internal_to_elem
        #self.assertEqual(xml_string, '<e name="value">text</e>')


    def test_json2xml2(self):

        json_data = '{"e": null}' 
        xml_string = xml2json.json2elem(json_data)
        self.assertEqual(json_data, xml2json.elem2json(xml_string,options))

        json_data = '{"e": {"a": "text", "b": "text"}}' 
        xml_string = xml2json.json2elem(json_data)
        self.assertEqual(json_data, xml2json.elem2json(xml_string,options))

        json_data = '{"e": {"@": "1", "#tail": "2", "#text": "3", "q":["dnja","lknvdsl"]}}' #4
        xml_string = xml2json.json2xml(json_data)
        # self.assertEqual(xml_string, '<e @="1">tail</e>')

        json_data = '{"e": "text"}' #2
        xml_string = xml2json.json2xml(json_data)
        self.assertEqual(xml_string, '<e>text</e>')

        json_data = '{"e":"a","r":"d"}'
        with self.assertRaises(ValueError) as cm: xml2json.json2xml(json_data)

if __name__ == '__main__':
    unittest.main()
