int x509_date_is_valid(int mon)
{
    switch (mon) {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            break;
        default:
            return 0x2400;
    }

    return 0;
}
