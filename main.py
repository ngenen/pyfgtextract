from fgtparser import *

# Usage example
if __name__ == '__main__':
    # We create ftg parser object with its only param the configuration backup
    fp = FGTParser('fortigate.conf')
    # We want for example extract the address inside a Deny group 'External IP Block'
    ips = fp.get_addr_group('External IP Block')
    with open('external_ip_block_ips.txt', 'w') as output_file:
        for ip in ips:
            output_file.write(ip + '\n')
