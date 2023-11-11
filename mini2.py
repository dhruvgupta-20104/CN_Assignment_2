from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI 


class CustomTopology(Topo):
    def build(self):
    
        # Adding hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Adding switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Adding links between hosts and switches
        
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s1)
        self.addLink(h4, s2)
        
        # Adding a link between switches
        self.addLink(s1,
                     s2,
                     intfName1='s1-eth3',
                     intfName2='s2-eth3')

        
        

if __name__ == '__main__':
    topo = CustomTopology()
    net = Mininet(topo=topo)
    net.start()
    CLI(net) 
    net.stop()
