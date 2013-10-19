from django.db.models.fields import AutoField, BigIntegerField
from django.db.models.fields.related import ForeignKey

from south.modelsinspector import add_introspection_rules

# From http://stackoverflow.com/a/17035822/252384
class BigAutoField(AutoField):
    def db_type(self, connection):  # pylint: disable=W0621
        if 'mysql' in connection.__class__.__module__:
            return 'bigint AUTO_INCREMENT'
        if 'postgis' in connection.__class__.__module__ or \
           'postgresql' in connection.__class__.__module__:
            return 'bigserial'
        return super(BigAutoField, self).db_type(connection)

class BigForeignKey(ForeignKey):
    def db_type(self, connection):
        rel_field = self.rel.get_related_field()
        if (isinstance(rel_field, BigAutoField) or
                (not connection.features.related_fields_match_type and
                isinstance(rel_field, BigIntegerField))):
            return BigIntegerField().db_type(connection=connection)
        return rel_field.db_type(connection=connection)

add_introspection_rules([], [r"^angkot\.osm\.fields\.BigAutoField"])
add_introspection_rules([], [r"^angkot\.osm\.fields\.BigForeignKey"])

