# mapserverapi_python

[//]: # (automatically generated from https://github.com/metwork-framework/resources/blob/master/cookiecutter/%7B%7Bcookiecutter.repo%7D%7D/README.md)

## Status (master branch)
[![Drone CI](http://metwork-framework.org:8000/api/badges/metwork-framework/mapserverapi_python/status.svg)](http://metwork-framework.org:8000/metwork-framework/mapserverapi_python)
[![Maintenance](https://github.com/metwork-framework/resources/blob/master/badges/maintained.svg)]()

## What is it ?

This is a tiny python library to invoke [mapserver](http://www.mapserver.org) engine
as a simple library (with no daemon or CGI).

## Why ?

We don't want to run "mapserver" as CGI or even as FastCGI, we already have our python
workers and we want to invoke "mapserver" features from them directly in Python.

Moreover, we don't like the "mapscript" feature because there is always something you can't change with it.

## What is the point ?

The idea is to dynamically write two strings in your Python processes depending on the incoming request:

- the full content of the mapfile (from a jinja2 template for example)
- the "query string" for mapserver (which can be different from the incoming one)

With that, you can "invoke" mapserver from your Python code as a library and get the output as a Python buffer or redirect the output into a file (which avoid to load in memory the full mapserver output).

## Example

```python

# With your logic, generate a mapfile content and load it (as a string)
# into mapfile_content
mapfile_content = [...]

# With your logic, generate the query string for mapserver and put it into
# mapserver_qs variable (as a string)
mapserver_qs = "LAYERS=ocean&TRANSPARENT=true&FORMAT=image%2Fpng&SERVICE=WMS&" \
    "VERSION=1.1.1&REQUEST=GetMap&STYLES=&EXCEPTIONS=application%2Fvnd.ogc." \
    "se_xml&SRS=EPSG%3A4326&BBOX=-180.0,-90.0,180.0,90.0&WIDTH=500&HEIGHT=250"
# (just an example)

# Import the wrapper
import mapserverapi

# Invoke mapserver and get the output
buf, content_type = mapserverapi.invoke(mapfile_content, mapserver_qs)

# You have the content_type of the result and the output buffer (with probably
# a binary image inside)

[...]

# Same idea but using a file instead of memory
content_type = mapserverapi.invoke_to_file(mapfile_content, mapserver_qs,
                                           "/tmp/output.png")

# You have the content_type of the result in content_type and the raw result
# in the given filepath
```




## Contributing guide

See [CONTRIBUTING.md](CONTRIBUTING.md) file.



## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file.


