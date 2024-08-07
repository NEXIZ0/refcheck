# refcheck

Refleckt Cheaker (refcheck) verifies reflected parameters in web applications, detecting XSS, SSTI, and CSTI vulnerabilities. It tests a single URL with multiple parameters from a list or file, efficiently scanning for security flaws. Advanced crawling and headless browser support ensure thorough analysis across all website facets.

## Usage Parameters
```
python3 refcheck.py -h
```

This will display help for the tool. Here are all the switches it supports.
```
usage: test.py [-h] -u URL [-p PARAMS] [-r READFILE] [--http2]

Process URL and parameters.

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL
  -p PARAMS, --params PARAMS
                        Comma-separated parameters
  -r READFILE, --readfile READFILE
                        File containing parameters, one per line
  --http2               Use HTTP/2 prefix
```
### with list of parameters
```
python3 refcheck.py -u url -p test,look,p
```

### with file of parameter
```
python3 refcheck.py -u url -r parameter.txt
```
