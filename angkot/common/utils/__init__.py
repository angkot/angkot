def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def set_model_values(model, data):
    for field in model._meta.get_all_field_names():
        if field in data:
            setattr(model, field, data[field])

