from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()
class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addNode('r2', cls=LinuxRouter, ip='10.1.0.1/24')
        r3 = self.addNode('r3', cls=LinuxRouter, ip='10.2.0.1/24')
        # Add 2 switches
        s1 = self.addSwitch('s1')
        #s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        #s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        #s6 = self.addSwitch('s6')
        # Add host-switch links in the same subnet
        self.addLink(s1,
                     r1,
                     intfName2='s1r1',
                     params2={'ip': '10.0.0.1/25'})
        self.addLink(s3,
                     r2,
                     intfName2='s3r2',
                     params2={'ip': '10.1.0.1/25'})
        self.addLink(s5,
                     r3,
                     intfName2='s5r3',
                     params2={'ip': '10.2.0.1/25'})
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1,
                     r2,
                     intfName1='r1r2',
                     intfName2='r2r1',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
        self.addLink(r2,
                     r3,
                     intfName1='r2r3',
                     intfName2='r3r2',
                     params1={'ip': '10.101.0.3/24'},
                     params2={'ip': '10.101.0.4/24'})
        self.addLink(r1,
                     r3,
                     intfName1='r1r3',
                     intfName2='r3r1',
                     params1={'ip': '10.102.0.5/24'},
                     params2={'ip': '10.102.0.6/24'})
        # Adding hosts specifying the default route
        d1 = self.addHost(name='d1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='d2',
                          ip='10.0.0.252/24',
                          defaultRoute='via 10.0.0.1')
        d3 = self.addHost(name='d3',
                          ip='10.1.0.251/24',
                          defaultRoute='via 10.1.0.1')
        d4 = self.addHost(name='d4',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        d5 = self.addHost(name='d5',
                          ip='10.2.0.251/24',
                          defaultRoute='via 10.2.0.1')
        d6 = self.addHost(name='d6',
                          ip='10.2.0.252/24',
                          defaultRoute='via 10.2.0.1')
        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d2, s1)
       	self.addLink(d3, s3)
        self.addLink(d4, s3)
        self.addLink(d5, s5)
        self.addLink(d6, s5)
def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1r2"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2r1"))
    #info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.102.0.6 dev r1r3"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.0.2 dev r1r2"))
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.102.0.5 dev r3r1"))
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.101.0.3 dev r3r2"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.101.0.4 dev r2r3"))
    net.start()
    CLI(net)
    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    run()
