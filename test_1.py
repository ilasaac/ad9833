import time
import spidev

# activate spidev module and settings SPI
bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 100000


def output_freq(hz_value):
    return int(round((hz_value * 2**28) / 25e6))


def freq_change_start():
    ctrl_reg = 0
    ctrl_reg += 2**13  # set DB13 (28 bit freq reg)
    ctrl_reg += 2**8  # set DB8 (Reset)
    return ctrl_reg


def freq_reg_lsb(freq_reg):
    fourteen_bit_mask = 0b0011111111111111
    write_value = 0
    write_value += 2**14  # set DB14
    lsb = freq_reg & fourteen_bit_mask
    write_value += lsb
    return write_value


def freq_reg_msb(freq_reg):
    fourteen_bit_mask = 0b0011111111111111
    write_value = 0
    write_value += 2**14  # set DB14
    msb = freq_reg >> 14 & fourteen_bit_mask
    write_value += msb
    return write_value


def phase_register():
    # Currently always the same value
    write_value = 0
    # Set phase register address
    write_value += 2 ** 15  # set DB15
    write_value += 2 ** 14  # set DB14
    return write_value


def freq_change_end():
    ctrl_reg = 0
    ctrl_reg += 2**13  # set DB13 (28 bit freq reg)
    return ctrl_reg


def word_split(word16):
    tx_msb = word16 >> 8
    tx_lsb = word16 & 0xFF
    return tx_msb, tx_lsb


def send_spi_sequence(sequence):
    for word16 in sequence:
        two_bytes = word_split(word16)
        print(f"\tsending:[{two_bytes[0]:#02x}, {two_bytes[1]:#02x}]")
        print(f"\tsend_data({word16:#06x})")
        spi.xfer(two_bytes)
        # spi.xfer2(two_bytes)


def change_freq(freq_hz):
    # Calc values to send
    print("For Frequency:", freq_hz)
    freq_reg = output_freq(freq_hz)
    print(f"Frequency setting: {freq_reg} = {freq_reg:#04x} = {freq_reg:016b}")
    ctrl_start = freq_change_start()
    print(f"Control register write: {ctrl_start:#04x}")
    lsb_value = freq_reg_lsb(freq_reg)
    print(f"lsb value: {lsb_value:#04x}")
    msb_value = freq_reg_msb(freq_reg)
    print(f"lsb value: {msb_value:#04x}")
    phase_reg = phase_register()
    print(f"Phase register write: {phase_reg:#04x}")
    ctrl_end = freq_change_end()
    print(f"Control register write: {ctrl_end:#04x}")

    # Write values to spi
    send_spi_sequence([ctrl_start, lsb_value, msb_value, phase_reg, ctrl_end])


def main():
    freq = int(input())
    show_freq_for = 3
    change_freq(freq)
#    time.sleep(show_freq_for)
#    change_freq(500)
#    time.sleep(show_freq_for)
#    change_freq(600)
#    time.sleep(show_freq_for)
#    change_freq(1000)
#    time.sleep(show_freq_for)


if __name__ == '__main__':
    main()
