import re


class FGTParser:
    def __init__(self, file_name):
        with open(file_name, 'r') as file:
            self._content = file.readlines()

        self._addresses = None
        self._address_groups = None

    def extract_addr_groups(self):
        addrgrp_section = re.compile(r'config firewall addrgrp')
        set_member = re.compile(r'set member')
        member_name = re.compile(r'"([^"]+)"')
        start_pattern = re.compile(r'edit "([^"]+)"')
        end_pattern = re.compile(r'next$')
        end_section = re.compile(r'end$')
        in_addrgrp_section = False
        current_group = ""
        in_group = False
        self._address_groups = {}

        for line in self._content:
            if addrgrp_section.search(line):
                in_addrgrp_section = True
            elif in_addrgrp_section and end_section.search(line):
                in_addrgrp_section = False
            elif in_addrgrp_section:
                if start_pattern.search(line):
                    current_group = start_pattern.search(line).group(1)
                    in_group = True
                elif in_group and end_pattern.search(line):
                    in_target_group = False
                elif in_group:
                    if set_member.search(line):
                        found_members = member_name.findall(line)
                        self._address_groups[current_group] = found_members

    def extract_addresses(self):
        address_section = re.compile(r'config firewall address')
        start_pattern = re.compile(r'edit "([^"]+)"')
        set_start_ip = re.compile(r'set start-ip (\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)')
        set_end_ip = re.compile(r'set end-ip (\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)')
        set_subnet = re.compile(r'set subnet (\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b) (\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)')
        set_fqdn = re.compile(r'set fqdn "([^"]+)"')
        end_pattern = re.compile(r'next$')
        end_section = re.compile(r'end$')
        in_address_section = False
        inside_edit = False
        current_object = ""
        curr_start = ""
        curr_end = ""
        self._addresses = {}
        # lineNum = 1


        # Iterate through each line in the file
        # We extract addresses first
        for line in self._content:
            if address_section.search(line):
                # We are inside address section
                # print("Line %d: Found address section at \"%s\"" % (lineNum, line.strip()))
                in_address_section = True
            elif in_address_section and end_section.search(line):
                # print("Line %d: Found address end section at \"%s\"" % (lineNum, line.strip()))
                in_address_section = False
            elif in_address_section:
                if start_pattern.search(line):
                    # print("Line %d: Address object start \"%s\"" % (lineNum, start_pattern.search(line).group(1)))
                    inside_edit = True
                    current_object = start_pattern.search(line).group(1)
                elif inside_edit and end_pattern.search(line):
                    # print("Line %d: Address object end \"%s\"" % (lineNum, line.strip()))
                    inside_edit = False
                    curr_start = ""
                    curr_end = ""
                elif inside_edit:
                    if set_subnet.search(line):
                        self._addresses[current_object] = "%s/%s" % (set_subnet.search(line).group(1),
                                                               set_subnet.search(line).group(2))
                    elif set_start_ip.search(line):
                        curr_start = set_start_ip.search(line).group(1)
                        if curr_end != "":
                            # We have start & end
                            self._addresses[current_object] = "%s-%s" % (curr_start, curr_end)
                    elif set_end_ip.search(line):
                        curr_end = set_end_ip.search(line).group(1)
                        if curr_start != "":
                            # We have start & end
                            self._addresses[current_object] = "%s-%s" % (curr_start, curr_end)
                    elif set_fqdn.search(line):
                        self._addresses[current_object] = set_fqdn.search(line).group(1)
                    # else:
                    #    print("Line %d: Inside address object \"%s\"" % (lineNum, line.strip()))
            # lineNum += 1

    def get_addr_group(self, group_name):
        ips = []
        addresses = self.get_addresses()
        groups = self.get_addr_groups()

        if group_name in groups:
            for member in groups[group_name]:
                if member in addresses:
                    # If member is a address we get it
                    ips.append(addresses[member])
                else:
                    # Otherwise we re iterate over the group and keept the address
                    ips.extend(self.get_addr_group(member))
        else:
            print("Address Group %s not found." % group_name)

        return ips

    def get_addresses(self):
        if not self._addresses:
            self.extract_addresses()

        return self._addresses

    def get_addr_groups(self):
        if not self._address_groups:
            self.extract_addr_groups()

        return self._address_groups


