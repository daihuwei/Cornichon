import common
import gherkin


def Settings():
    settings = common.Settings()
    settings["rootnamespace"] = "Cornichon::"
    settings["cases"]["class"] = "Camel"
    settings["cases"]["namespace"] = "Camel"
    settings["cases"]["param"] = "camel"
    settings["cases"]["step"] = "Camel"
    settings["types"]["bool"] = "bool {}"
    settings["types"]["int"] = "int {}"
    settings["types"]["uint"] = "unsigned int {}"
    settings["types"]["float"] = "double {}"
    settings["types"]["string"] = "const std::string& {}"
    return settings


def Macro():
    settings = {}
    for type in ["bool", "int", "uint", "float", "string"]:
        settings[type] = "_{}"
    return settings


def ArgModifier(val, type):
    if type == "bool":
        return common.Lower(val)
    if type in ["string", "symbol"]:
        return val.replace('"', '\\"')
    return val


def Arguments(examples, header):
    settings = Macro()
    return common.ArgumentList(header, examples.types, settings, common.AsUpperSymbol)


def Concat(examples, header):
    settings = Macro()
    return common.ArgumentList(header, examples.types, settings, common.AsUpperSymbol, " ## ")


def Stringify(examples, header):
    settings = Macro()
    settings["string"] = "#_{}"
    return common.ArgumentList(header, examples.types, settings, common.AsUpperSymbol)


def PrintScenario(namespace, scenario, arguments, steps, settings, indent):
    buffer = """
[[indent]]static void [[scenario]]([[arguments]])
[[indent]]{
[[indent]]  [[rootnamespace]][[namespace]]::Helpers::[[scenario]] instance;
[[steps]]
[[indent]]}
"""[1:]
    buffer = buffer.replace("[[indent]]", indent)
    buffer = buffer.replace("[[scenario]]", scenario)
    buffer = buffer.replace("[[arguments]]", arguments)
    buffer = buffer.replace("[[namespace]]", namespace)
    buffer = buffer.replace("[[rootnamespace]]", settings["rootnamespace"])

    concat = ""
    for step in steps:
        concat += step + "\n"
    buffer = buffer.replace("[[steps]]", concat.rstrip())
    return buffer


def FeatureName(feature, case):
    lines = feature.split('\n')
    camelCase = common.Tokenise(lines[0], case)
    return camelCase


def Scenarios(namespace, scenarios, settings, indent):
    concat = ""
    # parse the scenarios
    for s in scenarios:
        fullArgs = s.examples.ArgumentsList(settings["types"])
        steps = []
        for step in s.Steps():
            lines = step[1].split('\n')
            st = gherkin.Step(step[0], step[1])
            camelCase = st.Tokenise(settings["cases"]["step"])
            arguments = st.ArgumentList(s.examples.types, settings["values"])
            buffer = '[[indent]]  instance.[[camelCase]]([[arguments]]);'
            buffer = buffer.replace("[[indent]]", indent)
            buffer = buffer.replace("[[camelCase]]", camelCase)
            buffer = buffer.replace("[[arguments]]", arguments)
            steps.append(buffer)
            continue
        lines = s.lines.split('\n')
        scenarioName = common.Tokenise(lines[0], settings["cases"]["scenario"])
        concat += PrintScenario(namespace, scenarioName, fullArgs, steps, settings, indent)
        concat += "\n"
    return concat.rstrip()


def ScenarioInsts(scenarios, settings, indent):
    concat = ""
    # parse the sections
    for s in scenarios:
        lines = s.lines.split('\n')
        scenario = common.Tokenise(lines[0], settings["cases"]["scenario"])
        if s.examples.Exists():
            lines = s.examples.lines.split('\n')
            for line in lines[2:]:
                arguments = s.examples.ArgumentsInstance(settings["values"], line, ArgModifier)
                if "" == arguments:
                    continue
                buffer = """
[[indent]][[scenario]]Inst([[arguments]]);
"""
                buffer = buffer.replace("[[indent]]", indent)
                buffer = buffer.replace("[[scenario]]", scenario)
                buffer = buffer.replace("[[arguments]]", arguments)
                concat += buffer
        else:
            buffer = """
[[indent]][[scenario]]Inst();
"""
            buffer = buffer.replace("[[indent]]", indent)
            buffer = buffer.replace("[[scenario]]", scenario)
            concat += buffer
    return concat.rstrip()
