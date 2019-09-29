import unittest

import os, os.path, sys
subdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Cornichon')
sys.path.insert(0, subdir)
import cornichon

class Helpers(unittest.TestCase):
    def GivenAFeatureFileCalled(self, name):
        self.name = name

    def ThenTheGeneratedTestIsTheSameAsTheSaved(self):
        self.settings["stub"] = self.name
        inFileName = os.path.join('../Examples/tests', self.name + '.feature')
        f = open(inFileName, "r")
        self.settings["gherkin"] = f.readlines()
        f.close()
        contents = self.header + cornichon.Generate(self.settings, self.output)
        self.DiffHelper(contents, '../Examples/%s/%s%s' % (self.folder, self.name, self.ext))

    def ThenTheGeneratedTestIsTheSameAsTheSaved(self):
        self.settings["stub"] = self.name
        inFileName = os.path.join('../Examples/tests', self.name + '.feature')
        f = open(inFileName, "r")
        self.settings["gherkin"] = f.readlines()
        f.close()
        contents = self.header + cornichon.Generate(self.settings, self.output)
        self.DiffHelper(contents, '../Examples/%s/%s%s' % (self.folder, self.name, self.ext))

    def DiffHelper(self, contents, filename):
        newlines = contents.split('\n')
        oldlines = []
        if os.path.isfile(filename):
            fp = open(filename, "r")
            oldlines = fp.readlines()
            fp.close()
        else:
            fp = open(filename, "w")
            fp.write(contents)
            fp.close()
            self.fail("Writing test output to file")
        num = len(newlines)
        num2 = len(oldlines)
        diffs = abs(num - num2)
        if num2 < num:
            num = num2
        for i in range(num):
            self.assertEqual(oldlines[i].rstrip(), newlines[i])

class CppunittestHelper(Helpers):
    def WhenTheGeneratorIsCppunittest(self):
        self.output = "cppunittest"
        self.folder = "cppunittest"
        self.ext = ".cpp"
        self.header = ""
        self.settings = cornichon.Settings("cppunittest")

class CpphelpersHelper(Helpers):
    def WhenTheGeneratorIsCpphelpers(self):
        self.output = "cpphelpers"
        self.folder = "cpphelpers"
        self.ext = ".h"
        self.header = "// Copyright (c) 2019 ...\n\n"
        self.settings = cornichon.Settings("cpphelpers")

class GoogletestHelper(Helpers):
    def WhenTheGeneratorIsGoogletest(self):
        self.output = "googletest"
        self.folder = "googletest"
        self.ext = ".cpp"
        self.header = "// Copyright (c) 2019 ...\n\n"
        self.settings = cornichon.Settings("googletest")

class Pyunit_testsHelper(Helpers):
    def WhenTheGeneratorIsPyunit_tests(self):
        self.output = "pyunit_tests"
        self.folder = "pyunit_tests"
        self.ext = ".py"
        self.header = ""
        self.settings = cornichon.Settings("pyunit_tests")
        self.settings["helpers"] = "example_helpers"

class PyhelpersHelper(Helpers):
    def WhenTheGeneratorIsPyhelpers(self):
        self.output = "pyhelpers"
        self.folder = "pyunit_tests"
        self.ext = "_helpers.py"
        self.header = ""
        self.settings = cornichon.Settings("pyhelpers")

