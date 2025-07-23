from mininet.topo import Topo
from mininet.node import Node, RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()

class SDNRoteadoresTopo(Topo):
    def build(self):
        # Roteadores
        r0 = self.addNode('r0', cls=LinuxRouter)
        r1 = self.addNode('r1', cls=LinuxRouter)
        r2 = self.addNode('r2', cls=LinuxRouter)
        r3 = self.addNode('r3', cls=LinuxRouter)

        # Hosts
        pc0 = self.addHost('pc0', ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
        pc1 = self.addHost('pc1', ip='10.1.1.1/24', defaultRoute='via 10.1.1.254')
        ftp = self.addHost('ftp', ip='10.2.2.1/24', defaultRoute='via 10.2.2.254')
        web = self.addHost('web', ip='10.3.3.1/24', defaultRoute='via 10.3.3.254')

        # Hosts ↔ Roteadores
        self.addLink(pc0, r0, cls=TCLink, bw=1000, intfName2='r0-eth0', params2={'ip': '10.0.0.254/24'})
        self.addLink(pc1, r1, cls=TCLink, bw=1000, intfName2='r1-eth0', params2={'ip': '10.1.1.254/24'})
        self.addLink(ftp, r2, cls=TCLink, bw=1000, intfName2='r2-eth0', params2={'ip': '10.2.2.254/24'})
        self.addLink(web, r3, cls=TCLink, bw=1000, intfName2='r3-eth0', params2={'ip': '10.3.3.254/24'})

        # Interligações dos roteadores
        self.addLink(r0, r1, cls=TCLink, bw=1000, intfName1='r0-eth1', params1={'ip': '10.0.10.2/30'},
                               intfName2='r1-eth1', params2={'ip': '10.0.10.1/30'})
        self.addLink(r0, r2, cls=TCLink, bw=1000, intfName1='r0-eth2', params1={'ip': '10.0.20.1/30'},
                               intfName2='r2-eth1', params2={'ip': '10.0.20.2/30'})
        self.addLink(r0, r3, cls=TCLink, bw=1000, intfName1='r0-eth3', params1={'ip': '10.0.30.1/30'},
                               intfName2='r3-eth1', params2={'ip': '10.0.30.2/30'})
        self.addLink(r1, r2, cls=TCLink, bw=1000, intfName1='r1-eth2', params1={'ip': '10.1.20.1/30'},
                               intfName2='r2-eth2', params2={'ip': '10.1.20.2/30'})
        self.addLink(r1, r3, cls=TCLink, bw=1000, intfName1='r1-eth3', params1={'ip': '10.1.30.1/30'},
                               intfName2='r3-eth2', params2={'ip': '10.1.30.2/30'})
        self.addLink(r2, r3, cls=TCLink, bw=1000, intfName1='r2-eth3', params1={'ip': '10.2.30.2/30'},
                               intfName2='r3-eth3', params2={'ip': '10.2.30.1/30'})

def fix_router_ips(net):
    r0, r1, r2, r3 = net.get('r0', 'r1', 'r2', 'r3')

    # r0 interfaces
    r0.cmd('ip addr flush dev r0-eth0')
    r0.cmd('ip addr add 10.0.0.254/24 dev r0-eth0')
    r0.cmd('ip link set r0-eth0 up')

    r0.cmd('ip addr flush dev r0-eth1')
    r0.cmd('ip addr add 10.0.10.2/30 dev r0-eth1')
    r0.cmd('ip link set r0-eth1 up')

    r0.cmd('ip addr flush dev r0-eth2')
    r0.cmd('ip addr add 10.0.20.1/30 dev r0-eth2')
    r0.cmd('ip link set r0-eth2 up')

    r0.cmd('ip addr flush dev r0-eth3')
    r0.cmd('ip addr add 10.0.30.1/30 dev r0-eth3')
    r0.cmd('ip link set r0-eth3 up')

    # r1 interfaces
    r1.cmd('ip addr flush dev r1-eth0')
    r1.cmd('ip addr add 10.1.1.254/24 dev r1-eth0')
    r1.cmd('ip link set r1-eth0 up')

    r1.cmd('ip addr flush dev r1-eth1')
    r1.cmd('ip addr add 10.0.10.1/30 dev r1-eth1')
    r1.cmd('ip link set r1-eth1 up')

    r1.cmd('ip addr flush dev r1-eth2')
    r1.cmd('ip addr add 10.1.20.1/30 dev r1-eth2')
    r1.cmd('ip link set r1-eth2 up')

    r1.cmd('ip addr flush dev r1-eth3')
    r1.cmd('ip addr add 10.1.30.1/30 dev r1-eth3')
    r1.cmd('ip link set r1-eth3 up')

    # r2 interfaces
    r2.cmd('ip addr flush dev r2-eth0')
    r2.cmd('ip addr add 10.2.2.254/24 dev r2-eth0')
    r2.cmd('ip link set r2-eth0 up')

    r2.cmd('ip addr flush dev r2-eth1')
    r2.cmd('ip addr add 10.0.20.2/30 dev r2-eth1')
    r2.cmd('ip link set r2-eth1 up')

    r2.cmd('ip addr flush dev r2-eth2')
    r2.cmd('ip addr add 10.1.20.2/30 dev r2-eth2')
    r2.cmd('ip link set r2-eth2 up')

    r2.cmd('ip addr flush dev r2-eth3')
    r2.cmd('ip addr add 10.2.30.2/30 dev r2-eth3')
    r2.cmd('ip link set r2-eth3 up')

    # r3 interfaces
    r3.cmd('ip addr flush dev r3-eth0')
    r3.cmd('ip addr add 10.3.3.254/24 dev r3-eth0')
    r3.cmd('ip link set r3-eth0 up')

    r3.cmd('ip addr flush dev r3-eth1')
    r3.cmd('ip addr add 10.0.30.2/30 dev r3-eth1')
    r3.cmd('ip link set r3-eth1 up')

    r3.cmd('ip addr flush dev r3-eth2')
    r3.cmd('ip addr add 10.1.30.2/30 dev r3-eth2')
    r3.cmd('ip link set r3-eth2 up')

    r3.cmd('ip addr flush dev r3-eth3')
    r3.cmd('ip addr add 10.2.30.1/30 dev r3-eth3')
    r3.cmd('ip link set r3-eth3 up')

def config_static_routes(net):
    r0, r1, r2, r3 = net.get('r0', 'r1', 'r2', 'r3')
    # R0
    r0.cmd('ip route add 10.1.1.0/24 via 10.0.10.1 metric 10')
    r0.cmd('ip route add 10.1.1.0/24 via 10.0.20.2 metric 10')
    r0.cmd('ip route add 10.1.1.0/24 via 10.0.30.2 metric 10')

    r0.cmd('ip route add 10.2.2.0/24 via 10.0.20.2 metric 10')
    r0.cmd('ip route add 10.2.2.0/24 via 10.0.10.1 metric 10')
    r0.cmd('ip route add 10.2.2.0/24 via 10.0.30.2 metric 10')

    r0.cmd('ip route add 10.3.3.0/24 via 10.0.30.2 metric 10')
    r0.cmd('ip route add 10.3.3.0/24 via 10.0.10.1 metric 10')
    r0.cmd('ip route add 10.3.3.0/24 via 10.0.20.2 metric 10')

    # R1
    r1.cmd('ip route add 10.0.0.0/24 via 10.0.10.2 metric 10')
    r1.cmd('ip route add 10.0.0.0/24 via 10.1.20.2 metric 10')
    r1.cmd('ip route add 10.0.0.0/24 via 10.1.30.2 metric 10')

    r1.cmd('ip route add 10.2.2.0/24 via 10.1.20.2 metric 10')
    r1.cmd('ip route add 10.2.2.0/24 via 10.0.10.2 metric 10')
    r1.cmd('ip route add 10.2.2.0/24 via 10.1.30.2 metric 10')

    r1.cmd('ip route add 10.3.3.0/24 via 10.1.30.2 metric 10')
    r1.cmd('ip route add 10.3.3.0/24 via 10.0.10.2 metric 10')
    r1.cmd('ip route add 10.3.3.0/24 via 10.1.20.2 metric 10')

    # R2
    r2.cmd('ip route add 10.0.0.0/24 via 10.0.20.1 metric 10')
    r2.cmd('ip route add 10.0.0.0/24 via 10.1.20.1 metric 10')
    r2.cmd('ip route add 10.0.0.0/24 via 10.2.30.1 metric 10')

    r2.cmd('ip route add 10.1.1.0/24 via 10.1.20.1 metric 10')
    r2.cmd('ip route add 10.1.1.0/24 via 10.0.20.1 metric 10')
    r2.cmd('ip route add 10.1.1.0/24 via 10.2.30.1 metric 10')

    r2.cmd('ip route add 10.3.3.0/24 via 10.2.30.1 metric 10')
    r2.cmd('ip route add 10.3.3.0/24 via 10.1.30.2 metric 10')
    r2.cmd('ip route add 10.3.3.0/24 via 10.0.20.1 metric 10')

    # R3
    r3.cmd('ip route add 10.0.0.0/24 via 10.0.30.1 metric 10')
    r3.cmd('ip route add 10.0.0.0/24 via 10.1.30.1 metric 10')
    r3.cmd('ip route add 10.0.0.0/24 via 10.2.30.2 metric 10')

    r3.cmd('ip route add 10.1.1.0/24 via 10.1.30.1 metric 10')
    r3.cmd('ip route add 10.1.1.0/24 via 10.0.30.1 metric 10')
    r3.cmd('ip route add 10.1.1.0/24 via 10.2.30.2 metric 10')

    r3.cmd('ip route add 10.2.2.0/24 via 10.1.20.2 metric 10')
    r3.cmd('ip route add 10.2.2.0/24 via 10.2.30.2 metric 10')
    r3.cmd('ip route add 10.2.2.0/24 via 10.0.30.1 metric 10')


def run():
    net = Mininet(topo=SDNRoteadoresTopo(), controller=RemoteController, link=TCLink)
    net.start()

    # Corrige IPs nas interfaces dos roteadores antes de configurar rotas
    fix_router_ips(net)

    for r in ['r0', 'r1', 'r2', 'r3']:
        router = net.get(r)
        router.cmd('/usr/lib/frr/zebra -d')

    # Subir serviços
    ftp = net.get('ftp')
    web = net.get('web')
    ftp.cmd('python3 -m pyftpdlib -p 21 &')
    web.cmd('python3 -m http.server 80 &')

    config_static_routes(net)

    print("\n🌐 Rede iniciada!")
    print("Servidor FTP: 10.2.2.1:21")
    print("Servidor WEB: 10.3.3.1:80\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
