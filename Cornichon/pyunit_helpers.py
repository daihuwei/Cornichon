def ExtractParams(line, delim1, delim2):
    params = []
    while True:
        i = line.find(delim1)
        if -1 == i:
            break
        j = line.find(delim2, i+1)
        if -1 == j:
            break
        params.append(line[i:j+1])
        line = line[:i] + line[j+1:]
    return line, params

def CamelCase(section, line):
    if 1 == ['Given', 'When', 'Then', 'But'].count(section):
        line = section + ' ' + line
    line, params = ExtractParams(line, '"', '"')
    line, p = ExtractParams(line, '<', '>')
    params.extend(p)
    
    line = line.replace('\'', ' Apostrophe ')
    line = line.replace('?', ' QuestionMark ')
    line = line.replace(':', ' Colon ')
    line = line.replace(',', '')
    line = line.replace('-', ' ')

    bits = line.split()
    cased = ''
    args = []
    for i in range(len(params)):
        if params[i][0] == '<':
            args.append(params[i][1:-1])
            continue
        args.append('arg%d' % (i+1))
    for bit in bits:
        cased += bit[0].upper() + bit[1:]
    return cased, args, params

def Arguments(args, type):
    arguments = ''
    for arg in args:
        arguments = "%s%s%s, " % (arguments, type, arg)
    if len(arguments) > 0:
        arguments = arguments[:-2]
    return arguments

def Description(section, lines, params, indent, lindent):
    des = ''
    first = True
    for line in lines:
        if line.strip() == '':
            continue
        if first:
            first = False
            line = "%s%s %s" % (indent, section, line)
        line = '"%s"' % line
        for i in range(len(params)):
            if params[i][0] == '<':
                line = line.replace(params[i], '", %s"' % params[i][1:-1])
                continue
            line = line.replace(params[i], '", arg%d"' % (i+1))
        line = line.replace(', ""', '')
        line = line.replace(' "", ', ' ')
        buffer = """
        print([[line]])"""
        buffer = buffer.replace("[[line]]", line)
        des += buffer
    return des[1:]

def Feature(feature, indent):
    lines = feature.split('\n')
    camelCase, args, params = CamelCase('Feature:', lines[0])
    return camelCase, Description('Feature:', lines, [], '  ', indent)

def Steps(scenarios):
    concat = ""
    steps = []
    # parse the sections
    for scenario in scenarios:
        for s in scenario.Steps():
            lines = s[1].split('\n')
            camelCase, args, params = CamelCase(s[0], lines[0])
            if 0 != steps.count(camelCase):
                continue
            steps.append(camelCase)

            arguments = Arguments(args, ', ')
            buffer = """
    def [[camelCase]](self[[arguments]]):
[[Description]]

"""[1:]
            buffer = buffer.replace("[[camelCase]]", camelCase)
            buffer = buffer.replace("[[arguments]]", arguments)
            buffer = buffer.replace("[[Description]]", Description(s[0], lines, params, '      ', '    '))
            concat += buffer
    return concat.rstrip()

def Generate(scenarios, feature, settings):
    featureName, featureDesc = Feature(feature, '  ')

    buffer = """
import unittest

class Helpers(unittest.TestCase):
[[steps]]
"""[1:]

    buffer = buffer.replace("[[rootnamespace]]", settings["rootnamespace"])
    buffer = buffer.replace("[[featureName]]", featureName)
    buffer = buffer.replace("[[steps]]", Steps(scenarios))
    return buffer