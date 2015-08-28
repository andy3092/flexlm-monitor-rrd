#!/usr/bin/env python2

import re
import subprocess
import sys
import ipdb

lmutil = "/usr/local/bin/lmutil"



def get_licenses(server, feature):
    """
    Simple function that polls and parses a flexlm server
    from out put from lmutil.
    the second string for the computer can cause all sorts of issues
    e.g computer name hashes with leading spaces or any number of spaces half way through
    Makes it difficult to parse
    The output of lmutil is not always regular as it depends on the vendor.
    based on https://github.com/beaugunderson/flexlm-license-status
    usage: get_licenses("27000@example.com", "feature"))
    returns a dictionary with the following keys
    user computer computer2 version start and connection
    """

    licenses = []
    standard_spaces = 10 # normal number of spaces in lmutil license output line
    try:
        pass
        output = subprocess.check_output([lmutil, "lmstat", "-c", server,
                                          "-f", feature])
    except subprocess.CalledProcessError:
        return licenses
    
    for line in output.splitlines(True):
        if "start" in line:
            license = line.strip()
            # hack to get around extra spaces in the computer name
            num_extra_spaces = len(license.split(" ")) - standard_spaces
            subpattern = r' [^\s]+' * num_extra_spaces

            pattern = (r'(?P<user>[^\s]+) '
                       '(?P<computer>[^\s]+) '
                       '(?P<computer2>[^\s]*' + subpattern + ') '
                       '\((?P<version>[^\s]+)\) '
                       '\((?P<connection>[^,]+)\), '
                       'start (?P<start>.+)')

            license_re = re.compile(pattern)
            licenses.append(license_re.match(license).groupdict())

    return licenses

if __name__ == "__main__":
    print(get_licenses(sys.argv[1], sys.argv[2]))

    
