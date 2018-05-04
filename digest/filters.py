from json import dumps
from digest import app
from markdown import markdown


@app.template_filter('json')
def json_dumps(data):
    return dumps(data)

@app.template_filter('mapout')
def map_out(data, attribute):
    if type(data) == list:
        return list(map(lambda x: getattr(x, attribute), data))
    if type(data) == dict:
        build = {}
        for i in data:
            build[getattr(i, attribute)] = map_out(list(data[i]), attribute) # sql instrumented list, make this more abstract later
        return build

@app.template_filter('markdown')
def md(data):
    return markdown(data)