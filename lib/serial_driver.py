import serial

import lib.log as log_man


# module config
_MODULE_ID = 'lib.serial_driver'
_BAUD_RATE = 115200
_TIME_OUT = 1

# module state
_serial_port: serial.Serial = None


def init_driver():
    func_id = f"{_MODULE_ID}.init_module"

    global _serial_port

    log_man.print_log(func_id, 'DEBUG', 'initializing serial driver')

    try:
        _serial_port = serial.Serial(
            port='/dev/ttyACM0', baudrate=_BAUD_RATE, timeout=_TIME_OUT)
        flush_serial()

    except Exception as err:
        log_man.print_log(func_id, 'ERROR',
                          f"faild to initialize serial driver: {err}")

    log_man.print_log(func_id, 'DEBUG',
                      'finished initializing serial driver')


def flush_serial():
    while _serial_port.inWaiting():
        _serial_port.read(1)


def write_raw(msg: str):
    if _serial_port == None:
        return

    msg_to_write = f"{msg};"
    msg_buffer = msg_to_write.encode()

    if _serial_port != None:
        _serial_port.write(msg_buffer)


def read_raw():
    out = ''

    if _serial_port == None:
        return out

    if not _serial_port.inWaiting():
        return out

    while True:
        if _serial_port.inWaiting():
            char = _serial_port.read(1)

            if char == b';':
                break

            if char != b'\n' and char != b'\r':
                out += char.decode()

    flush_serial()
    return out


def read_raw_char():
    out = ''

    if _serial_port.inWaiting():
        out = _serial_port.read(1)

    return out
