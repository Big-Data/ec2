#coding=utf-8


class _BaseSettings(object):

    def __init__(self, defaults, values=None):
        self.defaults = defaults
        self.values = values.copy() if values else {}

    def __getitem__(self, opt_name):
        if opt_name in self.values:
            return self.values[opt_name]
        return getattr(self.defaults, opt_name, None)

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getbool(self, name, default=False):
        """
        True is: 1, '1', True
        False is: 0, '0', False, None
        """
        return bool(int(self.get(name, default)))

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getlist(self, name, default=None):
        value = self.get(name)
        if value is None:
            return default or []
        elif hasattr(value, '__iter__'):
            return value
        else:
            return str(value).split(',')

class Settings(_BaseSettings):

    def __init__(self, defaults=None, settings_module=None, **kw):
        super(Settings, self).__init__(defaults, **kw)
        self.settings_module = settings_module
        self.overrides = {}

    def enable(self, settings):
        self.settings_module = settings

    def update(self, v ):
        self.overrides.update(v)
        
    def __getitem__(self, opt_name):
        if opt_name in self.overrides:
            return self.overrides[opt_name]
        if self.settings_module and hasattr(self.settings_module, opt_name):
            return getattr(self.settings_module, opt_name)
        
        return super(Settings, self).__getitem__(opt_name)

    def __str__(self):
        return "<Settings module=%r>" % self.settings_module

