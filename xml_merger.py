from lxml import etree
from itertools import zip_longest

def merge_xmls(xmls):
    xml_data = None

    for xml in xmls:
        data = etree.fromstring(xml)
        if xml_data is None:
            xml_data = data

        else:
            # Merge elements from the current XML to the root node
            for element in data:
                flag = 0
                existing_elements = xml_data.find(element.tag)
                if existing_elements is not None:
                    # If there are existing elements with the same tag, extend the first one
                    for child1,child2 in zip_longest(existing_elements.iter(),element.iter()):
                        if child2 is not None and child1 is not None:
                            if child1.tag != child2.tag:
                                # import pdb;pdb.set_trace()
                                parent = child1.getparent()
                                parent.append(child2)
                                flag = 1
                                break                            
                else:
                    # If there are no existing elements with the same tag, append the new element
                    xml_data.append(element)
                if flag == 1:
                    break

    # Convert the root node to an ElementTree object
    xml_data = etree.ElementTree(xml_data)

    return etree.tostring(xml_data, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8")

xml1 = '''
<config>
      <a><b>2</b></a>
</config>
'''

xml2 = '''
<config>
     <d>3</d> 
</config>
'''
xml3 = '''
<config>
  <a>
    <c>3</c>
  </a>
</config>
'''
# Merge the XMLs
merged_xml = merge_xmls([xml1, xml2, xml3])
print(merged_xml) 
