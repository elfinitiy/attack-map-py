# Attack map
#### Description
Parses nginx style access logs, to make a map/bar of malicious requests.
#### Usage
`py main.py` with default settings
`py main.py -h ` for help

requires geolite country database from https://dev.maxmind.com/geoip/geoip2/geolite2/

#### Screenshots
![choropleth](docs/images/bad_request_country.png)


![bar](docs/images/bad_request_amount.png)