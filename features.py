import os
import os.path
import sys

subdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Cornichon')
sys.path.insert(0, subdir)
import cornichon


header = "// Copyright (c) 2019 ...\n\n"

for filename in os.listdir('Examples/tests'):
    inFileName = os.path.join('Examples/tests', filename)
    stub, ext = os.path.splitext(filename)
    if ext == '.feature':
        # Read the Gherkin DSL
        print(filename)
        f = open(inFileName, "r")
        gherkin = f.readlines()
        f.close()

        # Only need to call Settings for the test framework as it builds
        # on those settings for the helpers
        settings = cornichon.Settings("cpp/cppunittest")
        settings["gherkin"] = gherkin
        settings["stub"] = stub
        settings["rootnamespace"] = "Cornichon::"
        settings["helpers"] = "../helpers/"
        cornichon.PrintSettings(settings)

        # Generate the tests
        ofilename = 'Examples/output/cppunittest/' + stub + ".cpp"
        if os.path.exists(ofilename):
            ofilename = 'Examples/output/cppunittest/' + stub + ".fpp"
        fp = open(ofilename, "w")
        fp.write(cornichon.Generate(settings, "cpp/cppunittest"))
        fp.close()

        # Generate the test helpers
        ofilename = 'Examples/output/cpphelpers/' + stub + ".h"
        if os.path.exists(ofilename):
            ofilename = 'Examples/output/cpphelpers/' + stub + ".f"
        fp = open(ofilename, "w")
        fp.write(header + cornichon.Generate(settings, "cpp/cpphelpers"))
        fp.close()
