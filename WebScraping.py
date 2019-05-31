from bs4 import BeautifulSoup
import requests

def test(url):
    soup = get_data(url)
    print(collect_bits(soup, ExampleFormat))

def get_data(url):
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    return soup

def collect_bits(soup, format):
    #Finds all the bits matching given format(s)
    #returns a list of bits
    bits = []
    mat = format()
    for element in soup.find_all(mat.element_type):
        if mat.verify(element):
            #print(element, "\n")
            bits.append(mat.container_to_bit(element))
    return bits

class BaseFormat:
    def __init__(self):
        self.element_type = None

    def verify(self, element):
        #verifies that an element is of this format
        pass

    def container_to_bit(self, container):
        #creates a bit from the container
        pass

class ExampleFormat(BaseFormat):
    def __init__(self):
        super().__init__()
        self.element_type = "div"

    def verify(self, element):
        #verifies that an element is of this format
        class_list = element.get("class")
        if class_list[0] == "small-24" and class_list[1] == "medium-8" and class_list[2] == "col":
            return True
        return False

    def container_to_bit(self, element):
        a = element.a
        location = a.span.decode_contents()
        bit = [a.get("href"), location]

        return bit
