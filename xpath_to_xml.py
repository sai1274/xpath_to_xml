from lxml import etree
import re

def build_xml_from_xpath(xpath, value, operation = None):
    xpath_parts = re.split(r"/(?![^[]*\])", xpath)
    namespaces = {}
    elements = []

    for part in xpath_parts:
        if ":" in part:
            namespace, element_name = part.split(":")
            if namespace not in namespaces:
                namespaces[namespace] = f"{namespace}"
            elements.append((namespaces[namespace], element_name))
        else:
            elements.append((None, part))

    # Initialize the XML tree with the root element
    root_namespace, root_element = elements[0]
    root_element = etree.Element(f"{{{root_namespace}}}{root_element}", nsmap={None : root_namespace})

    # Create a stack to keep track of the current element
    stack = [root_element]

    # Iterate through the remaining elements to construct the tree
    for namespace, element_name in elements[1:]:
        if "[" in element_name and "]" in element_name:
            element, conditions = re.split(r"\[|\]", element_name, maxsplit=1)
            if namespace:
                current_element = etree.SubElement(stack[-1], f"{{{namespace}}}{element}", nsmap={None : namespace})
            else:
                current_element = etree.SubElement(stack[-1], f"{element}")
            # Extract conditions and create sub-elements for each condition
            for condition in re.split(r"\]\[", conditions.rstrip("]")):
                key, key_value = condition.split("=")
                sub_element = etree.SubElement(current_element, key)
                sub_element.text = key_value
        else:
            if namespace:
                current_element = etree.SubElement(
                    stack[-1], f"{{{namespace}}}{element_name}", nsmap={None : namespace}
                )
            else:
                current_element = etree.SubElement(
                    stack[-1], f"{element_name}"
                )

        # Push the current element onto the stack
        stack.append(current_element)

    # Set the value for the last element
    if operation is not None:
        if value is True or value is False:
            value_element = etree.SubElement(current_element, str(value).lower())
            value_element.set("{urn:ietf:params:xml:ns:netconf:base:1.0}operation", operation)
        else:
            try:
                current_element.set("{urn:ietf:params:xml:ns:netconf:base:1.0}operation", operation)
                current_element.text = str(value) if value is not None else None
            except:
                root_element.set("{urn:ietf:params:xml:ns:netconf:base:1.0}operation", operation)
                root_element.text = str(value) if value is not None else None

    # Print the XML string
    xml_string = etree.tostring(
        root_element, pretty_print=True, xml_declaration=True, encoding="utf-8"
    ).decode("utf-8")
    print(xml_string)


# Example XPath expression and value
xpath_expression = "org1:b/c[k1=v1][k2=v2]/org2:d/e/org3:f/g[k3=v3][k4=v4][k5=v5]/z"
value = None
operation = "delete"
# Build XML from XPath
build_xml_from_xpath(xpath_expression, value, operation) 
