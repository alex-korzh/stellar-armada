from abc import ABC

from pygame import Event


class Scene(ABC):
    next_scene: "Scene" = None

    def __init__(self):
        pass

    def draw(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def handle_event(self, event: Event):
        raise NotImplementedError()
