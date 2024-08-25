from pygame.sprite import Group


class CameraGroup(Group):
    def __init__(self, *sprites, **kwargs):
        super().__init__(*sprites)
        self.screen_config = kwargs.get("screen_config")

    def draw(self, surface):
        sprites = [
            s
            for s in self.sprites()
            if self.screen_config.is_in_game_area(*s.rect.center)
        ]
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(sprites, surface.blits((spr.image, spr.rect) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
