import digitalocean
import logging

class createFirewall:
   def __init__(self, token):
     self.logger = logging.getLogger(__name__)
     self.token = token
     self.inboundRules = None
     self.outboundRules = None
     self.digitalOceanFirewall = None

   def createInboundRules(self):
     #tcpHTTPPortRule = digitalocean.InboundRule(protocol="tcp", ports="80",
     #                                           sources=digitalocean.Sources(
     #                                           addresses=["0.0.0.0/0","::/0"]))
     
     #tcpHTTPSPortRule = digitalocean.InboundRule(protocol="tcp", ports="443",
     #                                           sources=digitalocean.Sources(
     #                                           addresses=["0.0.0.0/0","::/0"]))

     tcpSSHPortRule = digitalocean.InboundRule(protocol="tcp", ports="22",
                                                sources=digitalocean.Sources(
                                                addresses=["0.0.0.0/0","::/0"]))   
     
     icmpPortRule = digitalocean.InboundRule(protocol="icmp",
                                             sources=digitalocean.Sources(
                                             addresses=["0.0.0.0/0","::/0"]))

     #self.inboundRules = [tcpHTTPPortRule,tcpHTTPSPortRule,tcpSSHPortRule,icmpPortRule]
     self.inboundRules = [tcpSSHPortRule,icmpPortRule]


   def createOutboundRules(self):
     allTCPRule = digitalocean.OutboundRule(protocol="tcp", ports="all",
                                            destinations=digitalocean.Destinations(
                                            addresses=["0.0.0.0/0","::/0"]))
     
     allUDPRule = digitalocean.OutboundRule(protocol="udp", ports="all",
                                            destinations=digitalocean.Destinations(
                                            addresses=["0.0.0.0/0","::/0"]))

     self.outboundRules=[allTCPRule,allUDPRule]

   def writeFirewall(self,dropletName):
     self.dropletName = dropletName

     self.createInboundRules()
     self.createOutboundRules()

     self.digitalOceanFirewall=digitalocean.Firewall(token=self.token,
                                    name=self.dropletName+"Firewall",
                                    inbound_rules=self.inboundRules,
                                    outbound_rules=self.outboundRules)

     self.digitalOceanFirewall.create()

   def attachFirewall(self,dropletID):
     self.dropletID = [dropletID]
     self.digitalOceanFirewall.add_droplets(self.dropletID)
 
   
