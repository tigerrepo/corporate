class CorporateRouter(object):
    """Allows each model to set its own destiny"""

    def db_for_read(self, model, **hint):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return 'default'

    def db_for_write(self, model, **hint):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return 'default'

    def allow_syncdb(self, db, model, **hint):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False
