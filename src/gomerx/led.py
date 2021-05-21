from gomerx import protocol
from . import module

__all__ = ['Led', 'EFFECT_ON', 'EFFECT_OFF', 'EFFECT_FLASH', 'EFFECT_BREATH']

EFFECT_ON = 'on'
EFFECT_OFF = 'off'
EFFECT_FLASH = 'flash'
EFFECT_BREATH = 'breath'


class Led(module.Module):
    def __init__(self, robot):
        super().__init__(robot)

    def set_led(self, color=(0, 0, 0), effect=EFFECT_ON):
        proto = protocol.ProtoSetLed(color)
        if effect is EFFECT_OFF:
            proto._effect = 0
        elif effect is EFFECT_ON:
            proto._effect = 1
        elif effect is EFFECT_FLASH:
            proto._effect = 2
        elif effect is EFFECT_BREATH:
            proto._effect = 3
            proto._t1 = 1000
            proto._t2 = 1000

        return self._send_sync_proto(proto)
