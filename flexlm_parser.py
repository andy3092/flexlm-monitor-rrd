#!/usr/bin/env python2

import re
import subprocess
import sys
import ipdb

lmutil = "/usr/local/bin/lmutil"

def parse_license_line(line):
    """
    Parses a single line from the license output put in a seprate function as it 
    is easier to test. t
    The second string for the computer name can cause all sorts of issues
    e.g computer names with leading spaces or any number of spaces half way through
    makes it difficult to parse The output of lmutil is not always regular as it 
    depends on the vendor. The regular expression may need tweaking depending on the output
    based on https://github.com/beaugunderson/flexlm-license-status


    returns a dictionary with the following keys
    user computer computer2 version start and connection
    """
    license = line.strip()
    # a bit of a hack to get around extra spaces in the 2nd computer name 
    standard_spaces = 10 # normal number of spaces in lmutil license output line
    num_extra_spaces = len(license.split(" ")) - standard_spaces
    subpattern = r' [^\s]*' * num_extra_spaces
    pattern = (r'(?P<user>[^\s]+) '
               '(?P<computer>[^\s]+) '
               '(?P<computer2>[^\s]*' + subpattern + ') '
               '\((?P<version>[^\s]+)\) '
               '\((?P<connection>[^,]+)\), '
               'start (?P<start>.+)')

    license_re = re.compile(pattern)
    return license_re.match(license).groupdict()

def get_licenses(server, feature):
    """
    Simple function that polls a flexlm server
    feeds it to the parse license
    from out put from lmutil.
    usage: get_licenses("port@example.com", "feature"))
    """

    licenses = []
    try:
        pass
        output = subprocess.check_output([lmutil, "lmstat", "-c", server,
                                          "-f", feature])
    except subprocess.CalledProcessError:
        return licenses
    
    for line in output.splitlines(True):
        if "start" in line:
            licenses.append(parse_license_line(line))
    return licenses

if __name__ == "__main__":
    # So you can run it from the commandline
    print(get_licenses(sys.argv[1], sys.argv[2]))

    
