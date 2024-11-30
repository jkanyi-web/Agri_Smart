from importlib_metadata import entry_points

def kombu_serializers():
    return entry_points(group='kombu.serializers')
