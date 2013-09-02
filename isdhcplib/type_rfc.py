#-*- coding: utf-8 -*-

class RFC3046:
    """
    """

    def __init__(self,data):
        """
        """
        self._agent_remote_id = []
        self._agent_circuit_id = []

        self.empty = True
        if isinstance(data, (list, tuple)):
            self._data = data
        else:
            self._data = []

        if not self._data:
            return
        if self._data[0] == 1:
            l1 = self._data[1]
            self._agent_circuit_id = self._data[2:l1+2]
            if self._data[l1+2] == 2:
                l2 = self._data[l1+3]
                self._agent_remote_id = self._data[l1+4:l1+4+l2]

        self.empty = False

    def StrAgentRemoteId(self):
        """
        """
        return ':'.join([ '%02X'%c for c in self._agent_remote_id])

    def ListAgentRemoteId(self):
        """
        """
        return self._agent_remote_id

    def StrAgentCircuitId(self):
        """
        """
        return ':'.join([ '%02X'%c for c in self._agent_circuit_id])

    def ListAgentCircuitId(self):
        """
        """
        return self._agent_circuit_id

    def AgentRemoteId_MAC(self):
        """
        """
        return ':'.join([ '%02X'%c for c in self._agent_remote_id[-6:]])

    def AgentCircuitId_Port(self):
        """
        """
        try:
            port = '%d'%self._agent_circuit_id[-1]
        except:
            port = "0"

        return port

    def AgentCircuitId_Vlan(self):
        """
        """
        try:
            x = 0
            for i in (1, 0):
                x += self._agent_circuit_id[3 - i] << i * 8
        except:
            x = 0

        return x

class RFC3442:
    def __init__(self, routes):
        self._routes = []
        for subnet, gw in routes.iteritems():
            self._routes.append((IPNetwork(subnet).network, IPNetwork(subnet).prefixlen, 
                        IPNetwork(subnet).network.words, IPAddress(gw).words))

    def ListClasslessRoutes(self):
        result = []

        for route in self._routes:
            result.append(route[1])
            for i in xrange(4):
                if route[1] > i * 8:
                    result.append(route[2][i])

            result.extend(route[3])

        return result
