
from functools import reduce
from netaddr import IPAddress, IPNetwork


class RFC3046(object):
    """
    """

    def __init__(self, data):
        """
        """
        self._agent_remote_id = []
        self._agent_circuit_id = []

        self.agent_remote_id = self.agent_circuit_id = []

        self.empty = True

        # check if data not empty
        if not data or not isinstance(data, (list, tuple)):
            return

        # keep passed data for later use
        self._raw_data = data

        # decode suboptions
        self._agent_circuit_id, self._agent_remote_id = \
            self._decodeSubopts(data)

        if len(self._agent_circuit_id) > 2:
            self.agent_circuit_id = \
                self._decodeAgentCircuitId(self._agent_circuit_id)

        if len(self._agent_remote_id) > 2:
            self.agent_remote_id = \
                self._decodeAgentRemoteId(self._agent_remote_id)

        self.empty = False

    def _decodeSubopts(self, data):
        suboptions = {1: [], 2: []}
        pos = 0

        while pos < len(data):
            suboption_code, suboption_len = data[pos:pos+2]

            if suboption_code not in suboptions:
                # Malformed DHCP agent relay field
                break

            suboptions[suboption_code] = data[pos + 2:pos + 2 + suboption_len]
            pos += 2 + suboption_len
        
        return suboptions[1], suboptions[2]

    def _decodeAgentCircuitId(self, agent_circuit_id):
        """
        D-Link DHCP option 82 Circuit ID suboption format:

        +-----+-----+-----+-----+-----------+-------------+-----------+
        |  1) |  2) |  3) |  4) |     5)    |      6)     |    7)     |
        +=====+=====+=====+=====+===========+=============+===========+
        |  1  |  6  |  0  |  4  |  VLAN(2)  |  Module(1)  |  Port(1)  |
        +-----+-----+-----+-----+-----------+-------------+-----------+

        1) Suboption type
        2) Length
        3) Circuit ID type
        4) Length
        5) VLAN id
        6) Module (0 for standalone, Unit ID for stackable)
        7) Port
        """

        circuit_id_vlan = 0
        circuit_id_module = 0
        circuit_id_port = 0

        circuit_id_type, circuit_id_len = agent_circuit_id[:2]

        if circuit_id_type == 0 and circuit_id_len == 4:
            circuit_id_vlan = reduce(lambda x, y: (x << 8) + y,
                                     agent_circuit_id[2:4], 0)
            circuit_id_module = agent_circuit_id[4]
            circuit_id_port = agent_circuit_id[5]

        return circuit_id_vlan, circuit_id_module, circuit_id_port

    def _decodeAgentRemoteId(self, agent_remote_id):
        """
        D-Link DHCP option 82 Remote ID suboption format:

        +-----+-----+-----+-----+-------------------+
        |  1) |  2) |  3) |  4) |       5)          | 
        +=====+=====+=====+=====+===================+
        |  2  |  8  |  0  |  6  |  MAC ADDRESS (6)  |
        +-----+-----+-----+-----+-------------------+

        1) Suboption type
        2) Length
        3) Remote ID type
        4) Length
        5) MAC address (or sysname?)
        """

        remote_id_mac = []

        remote_id_type, remote_id_len = agent_remote_id[:2]

        if remote_id_type == 0 and remote_id_len > 0:
            remote_id_mac = agent_remote_id[-remote_id_len:]

        return remote_id_mac

    @property
    def AgentRemoteId(self):
        return self.agent_remote_id

    @property
    def AgentCircuitId(self):
        return self.agent_circuit_id

    def __len__(self):
        return len(self._raw_data)


class RFC3442:
    def __init__(self, routes):
        self._routes = []
        for subnet, gw in routes.iteritems():
            self._routes.append((IPNetwork(subnet).network,
                                 IPNetwork(subnet).prefixlen,
                                 IPNetwork(subnet).network.words,
                                 IPAddress(gw).words))

    def ListClasslessRoutes(self):
        result = []

        for route in self._routes:
            result.append(route[1])
            for i in range(4):
                if route[1] > i * 8:
                    result.append(route[2][i])

            result.extend(route[3])

        return result
