import json
import os
import re

import requests
from bs4 import BeautifulSoup

from src.models.website_availability_item import WebsiteAvailabilityItem


def website_availability_processor():
    input_website_json = get_input_website_json()

    if not input_website_json:
        print("Could not find any websites in 'website_availability_list.json'")
        exit(1)

    return list(map(lambda website_url:
                    WebsiteAvailabilityItem(
                        website_url,
                        *get_website_availability(website_url, input_website_json[website_url])
                    ), input_website_json))


def get_website_availability(website_url, regex_patterns):
    print("--> Checking website processing: " + website_url)
    response = requests.get(website_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    page_contents = soup.body.get_text()
    regex_pattern_statuses = {}

    for pattern in regex_patterns:
        if re.search(pattern, page_contents):
            # print("Found pattern: " + pattern)
            regex_pattern_statuses[pattern] = True
        else:
            # print("Did not find pattern: " + pattern)
            regex_pattern_statuses[pattern] = False

    return response.status_code, response.elapsed.microseconds, regex_pattern_statuses


def get_input_website_json():
    script_dir = os.path.dirname(__file__)
    website_list_relative_path = './../../website_availability_list.json'
    return json.load(open(os.path.join(script_dir, website_list_relative_path), ))
