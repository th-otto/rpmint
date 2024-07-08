int mbedtls_to_psa_error(int ret)
{
    switch (ret) {
        case -0x0020:
            return (-134);
        case -0x0060:
        case -0x0062:
        case -0x0064:
        case -0x0066:
        case -0x0068:
            return (-135);
        case -0x006A:
            return (-141);
    }
    return (-132);
}
