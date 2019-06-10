from bs4 import BeautifulSoup
import requests

def test(url):
    soup = get_data(url)
    bits_to_csv("test", collect_bits(soup, ExampleFormat))

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

def get_links(file):
    f = open(file)
    links = []
    for link in f:
        links.append(link)
    return links

def bits_to_csv(filename, bits):
    #Creates a new csv file and inputs the bits
    f = open(filename + ".csv", "w+")
    for bit in bits:
        for index in range(len(bit)):
            f.write(bit[index] + ("," if index < len(bit) - 1 else "\n"))
    f.close()

class BaseFormat:
    def __init__(self):
        self.element_type = None

    def verify(self, element):
        #verifies that an element is of this format
        raise NotImplementedError

    def container_to_bit(self, container):
        #creates a bit from the container
        raise NotImplementedError

class ExampleFormat(BaseFormat):
    def __init__(self):
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

if __name__ == "__main__":
    test("https://newenglandfacts.com/abc/1")
