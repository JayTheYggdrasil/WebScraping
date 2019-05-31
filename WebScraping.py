from bs4 import BeautifulSoup
import requests

def get_data(url):
    r  = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    return soup, data

def condition(bit):
    #Takes in a bit of data and determines if it is in the output
    #returns bool
    pass

def collect_bits(soup, format):
    #Finds all the bits matching given format(s)
    #returns a list of bits
    pass
