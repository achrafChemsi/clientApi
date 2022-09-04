# -*- coding: utf-8 -*-

class HerokuDatabaseWrapper(dict):
    """
    Use this class to wrap your settings.DATABASES like this:

    DATABASES = HerokuDatabaseWrapper({
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myuser',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    })
    """
    def get_config_for_app(self, name):
        from subprocess import check_output
        d = {}
        output = check_output('heroku config -a'.split() + [name, ])
        for line in output.split('\n'):
            if ':' not in line:
                continue
            key, val = map(lambda s: s.strip(), line.split(':', 1))
            d[key] = val
        return d

    def get_config(self, name):
        import dj_database_url
        db_url = self.get_config_for_app(name)['DATABASE_URL']
        return dj_database_url.parse(db_url)

    def __getitem__(self, name):
        if name not in self:
            self[name] = self.get_config(name)
        return dict.__getitem__(self, name)

def db_copy(obj, to, *skip, **kwargs):
    '''
    Copies a model from one database into another.
    `obj` is the model that is going to be cloned
    `to` is the db definition
    `skip` is a list of attribtues that won't be copied
    `kwargs is a list of elements that will be overwritten over model data
    returns the copied object in `to` db
    '''
    from django.forms.models import model_to_dict
    from django.db.models import Model
    assert isinstance(obj, Model)
    data = model_to_dict(obj)
    for key in skip:
        if key in data:
            v = data.pop(key)
            print("Removing {}: {}".format(key, v))
    data.update(kwargs)
    return type(obj).objects.using(to).create(**data)
