from google.appengine.ext.db import *


class DictProperty(Property):
    data_type = type('')

    def get_value_for_datastore(self, model_instance):
        data = super(DictProperty, self).get_value_for_datastore(model_instance)
        return json.loads(data)

    def get_value_from_datastore(self, value):
        if value is None:
            return None

        return json.dumps(value)
