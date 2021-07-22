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
        """设置灯光颜色和显示模式

        :param tuple color: color=(R, G, B), 灯光颜色采用RGB模型组成. R:[0~255], 红色光分量, G:[0~255], 绿色光分量, B:[0~255], 蓝色光分量
        :param enum effect: "on":开启灯光, "off":关闭灯光
        :return: 灯光设置是否成功, 设置成功返回 True, 设置失败返回 False
        :rtype: bool
        """
        if not(0 <= color[0]) <= 255 or not(0 <= color[1] <= 255) or not(0 <= color[2] <= 255):
            raise Exception('invalid parameter.')
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
