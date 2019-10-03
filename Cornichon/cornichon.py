"""A small Gherkin DSL parser that generates stub code against various test frameworks"""
import gherkin


def Settings(output):
    """Get the default settings for the output type"""
    mod = gherkin.Import(output)
    return mod.Settings()


def PrintSettings(settings, level="settings"):
    """Utility that prints all the given settings"""
    for key in settings:
        try:
            if type(settings[key]) is str:
                print('{}["{}"] = "{}"'.format(level, key, settings[key]))
            else:
                PrintSettings(settings[key], '{}["{}"]'.format(level, key))
        except TypeError:
            pass


def Generate(settings, output):
    """Generate the stub code for the output type"""
    parsed = gherkin.Parse(settings)
    mod = gherkin.Import(output)
    return mod.Generate(parsed, settings)
