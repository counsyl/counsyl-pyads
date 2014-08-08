def HexBlock(data, width=8):
    i = 0
    result = ''
    currentHexLine = ''
    currentChrLine = ''

    for byte in data:
        # next line, if required
        if (i == width):
            result += '%s %s\n' % (currentHexLine, currentChrLine)
            currentHexLine = ''
            currentChrLine = ''
            i = 0

        # python2 / python3 - normalize to numeric byte
        char = ord(byte) if isinstance(byte, str) else byte

        # append to lines
        currentHexLine += '%02x ' % char
        currentChrLine += '.' if (char < 32 or char > 126) else chr(char)
        i += 1

    # append last line
    result += '%s %s' % (currentHexLine, currentChrLine)
    return result
