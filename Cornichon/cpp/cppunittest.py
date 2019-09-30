import common

def TestMethods(scenarios):
    concat = ""
    # parse the sections
    for s in scenarios:
        lines = s.lines.split('\n')
        scenario, args, params = common.CamelCase('Scenario', lines[0])

        if s.examples != '':
            args = ''
            lines = s.examples.split('\n')
            for line in lines[1:]:
                args = line.strip()[1:-2].replace('|', ' ').upper()
                break
            arguments = common.Arguments(args.split(), '_')
            concat2 = arguments.replace(', _', ' ## _')
            stringify = arguments.replace('_', '#_')
            buffer = """
#define [[scenario]]Inst([[arguments]]) \\
  TEST_METHOD([[scenario]] ## [[concat2]]) \\
  { \\
    [[scenario]]([[stringify]]); \\
  }

"""[1:]
            buffer = buffer.replace("[[scenario]]", scenario)
            buffer = buffer.replace("[[arguments]]", arguments)
            buffer = buffer.replace("[[concat2]]", concat2)
            buffer = buffer.replace("[[stringify]]", stringify)
            concat += buffer
        else:
            buffer = """
#define [[scenario]]Inst() \\
  TEST_METHOD([[scenario]] ## Impl) \\
  { \\
    [[scenario]](); \\
  }

"""[1:]
            buffer = buffer.replace("[[scenario]]", scenario)
            concat += buffer
    return concat.rstrip()

def Settings():
    settings = common.Settings("cpp")
    settings["helpers"] = "../helpers/"
    return settings

def Generate(parsed, settings):
    scenarios = parsed[0]
    feature = parsed[1]
    buffer = """
#include "stdafx.h"

// Other bespoke headers
#include "[[helpers]][[stub]].h"
#include "[[helpers]]LogStream.h"

// Third party headers
#include "CppUnitTest.h"

// Standard library headers
#include <iostream>
#include <memory>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

[[TestMethods]]


namespace [[rootnamespace]][[namespace]]
{
  TEST_CLASS([[featureName]])
  {
    static std::streambuf* oldBuffer;
    static std::shared_ptr<std::streambuf> newBuffer;

[[Scenarios]]


    TEST_CLASS_INITIALIZE(ClassInitialize)
    {
      newBuffer = std::make_shared<TestUtils::LogStream>();
      oldBuffer = std::clog.rdbuf(newBuffer.get());
      std::clog << "Entering [[stub]]" << std::endl;
    }

    TEST_CLASS_CLEANUP(ClassCleanup)
    {
      std::clog << "Exiting [[stub]]" << std::endl;
      std::clog.rdbuf(oldBuffer);
      newBuffer = nullptr;
    }

  public:
[[ScenarioInsts]]
  };

  std::streambuf* [[featureName]]::oldBuffer = nullptr;
  std::shared_ptr<std::streambuf> [[featureName]]::newBuffer = nullptr;
}

"""[1:]

    buffer = buffer.replace("[[stub]]", settings["stub"])
    buffer = buffer.replace("[[helpers]]", settings["helpers"])
    buffer = buffer.replace("[[TestMethods]]", TestMethods(scenarios))
    
    namespace = settings["stub"]
    namespace, args, params = common.CamelCase('', namespace)
    buffer = buffer.replace("[[rootnamespace]]", settings["rootnamespace"])
    buffer = buffer.replace("[[namespace]]", namespace)

    # Print the class
    featureName, featureDesc = common.Feature(feature, '    ')
    settings["feature"] = featureName
    buffer = buffer.replace("[[featureName]]", featureName)
    buffer = buffer.replace("[[Scenarios]]", common.Scenarios(scenarios, featureDesc, settings, "    "))
    buffer = buffer.replace("[[ScenarioInsts]]", common.ScenarioInsts(scenarios, "    "))

    return buffer