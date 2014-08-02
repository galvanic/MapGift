
from ModestMaps.Stamen import BaseProvider


class StamenWatercolorProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'watercolor')

    def getTileUrls(self, coordinate):
        url = BaseProvider.getTileUrls(self, coordinate)[0]
        base_url = url[:url.rindex('.')]
        return (base_url + '.jpg',)


class StamenTonerLinesProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-lines')


class StamenTonerLiteProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-lite')


class StamenTonerLabelsProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-labels')


class StamenTonerHybridProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-hybrid')


class StamenTonerBackgroundProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-background')
