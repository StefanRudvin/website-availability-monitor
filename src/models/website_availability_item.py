

class WebsiteAvailabilityItem:
    def __init__(self, website_url, status_code, response_time, regex_pattern_matches):
        self.website_url = website_url
        self.status_code = status_code
        self.response_time = response_time
        self.regex_pattern_matches = regex_pattern_matches
