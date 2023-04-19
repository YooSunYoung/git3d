from typing import List, Union, AnyStr

class DictionaryItemOverwrittenWarning(Warning):
    """Overwriting dictionary item might be unexpected."""


class DictionaryItemOverwrittenError(Exception):
    """Overwriting dictionary item is not expected at all."""



def list_to_dict(
    items: List,
    key_field: Union[AnyStr, int] = "name",
    value_field: Union[AnyStr, int] = None,
    allow_overwriting: bool = False,
) -> dict:
    """
    Converts a list to a dictionary based on the ``key_field`` and ``value_field``.
    From the converted dictionary,
    each ``item`` will be accessible by it's own member, which is ``item[key_field]``.

    If ``value_field`` is not defined, it will keep all fields of each item, otherwise
    each item will only keep ``item[value_field]`` in the converted dictionary.

    This helper was needed to prevent unexpected overwriting in the configuration file.
    See https://github.com/scipp/beamlime/discussions/33 for more details.

    You can also give a list of indices as a ``key_field`` but not recommended.

    Examples
    --------
    ```
    >>> items = [{'name': 'lime0', 'price': 1}, {'name': 'lime1', 'price': 2}]
    >>> dict_items = list_to_dict(items, key_field='name')
    >>> dict_items
    {'lime0': {'name': 'lime0', 'price': 1}, 'lime1': {'name': 'lime1', 'price': 2}}

    >>> smaller_dict_items = list_to_dict(items, key_field='name', value_field='price')
    >>> smaller_dict_items
    {'lime0': 1, 'lime1': 2}

    ```

    Raises
    ------
    DictionaryItemOverwrittenWarning
      If ``allow_overwriting`` == True and any values of ``key_field`` are not unique.

    DictionaryItemOverwrittenError
      If ``allow_overwriting`` == False and any values of ``key_field`` are not unique.
    """
    if value_field is None:
        converted_dict = {item[key_field]: item for item in items}
    else:
        converted_dict = {item[key_field]: item[value_field] for item in items}

    if len(converted_dict) != len(items):  # If any items are overwritten.
        message = f"'{key_field}' contains non-unique values. "
        if allow_overwriting:
            raise DictionaryItemOverwrittenWarning(message)
        else:
            hint = "If it is expected you may set the `allow_overwriting` as `True`."
            raise DictionaryItemOverwrittenError(message, hint)

    return converted_dict