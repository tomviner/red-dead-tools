from datetime import datetime, timedelta
import json

import attr


SETTINGS = {
    "main.isMenuOpened": "true",
    "main.isFmeDisplayEnabled": "false",
    "main.markerColor": "\"by_category\"",
}


@attr.s
class Settings:
    version = 2

    static = attr.ib(default=SETTINGS)
    important_items = attr.ib(factory=list)
    unimportant_items = attr.ib(factory=list)

    def as_export(self):
        data = self.static.copy()

        items = [item.code for item in self.important_items]
        data['importantItems'] = json.dumps(items)

        for item in self.unimportant_items:
            data[f'amount.{item.code}'] = '1'
            data[f'collected.{item.code}'] = 'true'
            for i in range(10):
                data[f'collected.{item.code}_{i}'] = 'true'

        date = datetime.now() - timedelta(hours=2)
        data['main.date'] = date.strftime('%Y-%m-%d')
        data['length'] = len(data)
        data['version'] = self.version

        return data

    def as_json(self):
        return json.dumps(self.as_export(), indent=4)


@attr.s(frozen=True)
class Item:
    collection = attr.ib()
    code = attr.ib()
    name = attr.ib()


@attr.s(frozen=True)
class Collection:
    code = attr.ib()
    name = attr.ib()
