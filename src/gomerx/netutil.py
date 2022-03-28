import socket


def getBroadcastIP(ip: str) -> str:
    # 获取广播地址
    l = ip.split('.')[:3]
    l.append('255')
    return '.'.join(l)


def getIP(mode: str) -> str:
    # 获取IP地址
    # 直连模式下 地址为 192.168.5.XXX
    # 路由模式下 地址为 192.168.XXX.XXX
    addrs = socket.gethostbyname_ex(socket.gethostname())[-1]
    for addr in addrs:
        if mode == 'router':
            if addr.startswith('192.168'):
                return addr
        else:
            if addr.startswith('192.168.5'):
                return addr

    return ''

def isClosed(socket) -> bool:
    # 判断socket是否关闭
    return getattr(socket, '_closed')
