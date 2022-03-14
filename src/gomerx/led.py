from . import event
from . import module
from . import message


EFFECT_ON = 'on'
EFFECT_OFF = 'off'
EFFECT_FLASH = 'flash'
EFFECT_BREATH = 'breath'


class Led(module.Module):

    def set_led(self, color: tuple = (0, 0, 0), effect: str = EFFECT_ON, T: int = 1000) -> bool:
        """设置灯光颜色和显示模式

        :param tuple color: color=(R, G, B), 灯光颜色采用RGB模型组成. R:[0~255], 红色光分量, G:[0~255], 绿色光分量, B:[0~255], 蓝色光分量
        :param enum effect: "on":开启灯光, "off":关闭灯光, "flash":灯光闪烁, "breath":呼吸灯
        :param int T:设置灯光闪烁/呼吸的时间周期, 呼吸的时间范围为[500,2000], 闪烁的时间范围为[100,1000], 单位Ms;
        :return: 灯光设置是否成功, 设置成功返回 True, 设置失败返回 False
        :rtype: bool
        """
        if min(color) < 0 or max(color) > 255:
            raise Exception("color value error")
        if effect == EFFECT_BREATH:
            if T > 2000 or T < 500:
                raise Exception("T value error")
        elif effect == EFFECT_FLASH:
            if T > 1000 or T < 100:
                raise Exception("T value error")
        msg = message.Message(
            message.SetLed, [color[0], color[1], color[2], T], effect)
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        return True
