from pulsar.apps.data import register_store

from .startds import start_store
from ..redis import store


__all__ = ['start_store']


class PulsarStore(store.RedisStore):
    pass


register_store('pulsar', 'pulsar.apps.data.pulsards:PulsarStore')
