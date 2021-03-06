"""Contains an interface to the freegeoip.net API.
Copyright 2018 - Bill Dengler <codeofdusk@gmail.com>. Licensed under MIT."""


from plugins.BasePlugin import BasePlugin
import requests
import json

configspec = (
    "# Geo",
    "# This plugin geolocates hostnames and IP addresses using the freegeoip.net API.",
    "# The requests package from PyPI is required.", "[[geo]]",
    "enabled=boolean(default=False)")


class GeoPlugin(BasePlugin):
    invocations = ("geo", )
    ad = "Type !geo <hostname or IP address> to geolocate a host using the freegeoip.net API."

    def lookup(self, ip=""):
        "Returns a dict containing an IP geolocation lookup from the freegeoip.net api. Optionally takes an IP address or hostname to lookup as argument, otherwise looks up the client's IP."
        r = requests.get("http://freegeoip.net/json/" + ip)
        if r.status_code != 200: return {"http_status_code": r.status_code}
        return json.loads(r.text)

    def as_string(self, r):
        "Parses an object in the form returned by lookup to a human-readable string."
        if 'http_status_code' in r:
            if r['http_status_code'] == 404: return "unknown"
            if r['http_status_code'] == 403:
                return "geolocation API rate limit exceeded."
        res = ""
        if 'city' in r and r['city'] != "": res += r['city'] + ", "
        if 'region_name' in r and r['region_name'] != "":
            res += r['region_name'] + ", "
        if 'country_name' in r and r['country_name'] != "":
            res += r['country_name'] + " "
        if 'ip' in r and r['ip'] != "": res += "(" + r['ip'] + " )"
        if res == "":
            return "Invalid response from the freegeoip.net API. The response was: " + str(
                r)
        else:
            return res

    def run(self, r):
        if len(r.content) <= 1:
            return "Usage: !geo <hostname or IP>"
        return self.as_string(self.lookup(r.content))
