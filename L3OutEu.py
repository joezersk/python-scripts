#!/usr/bin/env python

# list of packages that should be imported for this code to work
import urllib3
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.config
import cobra.model.fabric
import cobra.model.fv
import cobra.model.infra
import cobra.model.l3ext
import cobra.model.ospf
import cobra.model.pol
from cobra.internal.codec.xmlcodec import toXMLStr
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.50.129.241', 'admin', '1234Qwer')
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
topMo = cobra.model.pol.Uni('')

# build the request using cobra syntax
fabricInst = cobra.model.fabric.Inst(topMo)
configExportP = cobra.model.config.ExportP(fabricInst, name='defaultOneTime', descr='Added L3OUT in common', format='json', adminSt='untriggered', maxSnapshotCount='global-limit', snapshot='yes', includeSecureFields='yes')
fvTenant = cobra.model.fv.Tenant(topMo, name='common')
fvBD = cobra.model.fv.BD(fvTenant, ipLearning='yes', vmac='not-applicable', name='default', epClear='no', unkMacUcastAct='proxy', arpFlood='no', limitIpLearnToSubnets='yes', multiDstPktAct='bd-flood', OptimizeWanBandwidth='no', mcastAllow='no', mac='00:00:00:00:BD:CC', llAddr='::', intersiteL2Stretch='no', unicastRoute='yes', intersiteBumTrafficAllow='no', type='regular', unkMcastAct='flood')
fvSubnet = cobra.model.fv.Subnet(fvBD, ip='192.168.254.254/24', virtual='no', preferred='yes')
ospfIfPol = cobra.model.ospf.IfPol(fvTenant, nwT='p2p', pfxSuppress='inherit', name='OSPF_P2P_BFD', prio='1', ctrl='advert-subnet,bfd,mtu-ignore', helloIntvl='10', rexmitIntvl='5', xmitDelay='1', cost='unspecified', deadIntvl='40')
l3extOut = cobra.model.l3ext.Out(fvTenant, name='N5K_OSPF_L3OUT', enforceRtctrl='export', targetDscp='unspecified')
ospfExtP = cobra.model.ospf.ExtP(l3extOut, areaCtrl='redistribute,summary', areaId='0.0.0.1', areaType='nssa', multipodInternal='no', areaCost='1')
l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn='uni/l3dom-N5K_EXT_DOM')
l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName='default')
l3extLNodeP = cobra.model.l3ext.LNodeP(l3extOut, tag='yellow-green', name='N5K_OSPF_NODE', targetDscp='unspecified')
l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, tDn='topology/pod-1/node-103', rtrId='1.2.1.2', rtrIdLoopBack='yes')
l3extInfraNodeP = cobra.model.l3ext.InfraNodeP(l3extRsNodeL3OutAtt, fabricExtIntersiteCtrlPeering='no', fabricExtCtrlPeering='no')
l3extLIfP = cobra.model.l3ext.LIfP(l3extLNodeP, tag='yellow-green', name='N5K_OSPF_INTS')
ospfIfP = cobra.model.ospf.IfP(l3extLIfP, authKeyId='1', authType='none')
ospfRsIfPol = cobra.model.ospf.RsIfPol(ospfIfP, tnOspfIfPolName='OSPF_P2P_BFD')
l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(l3extLIfP, tDn='topology/pod-1/paths-103/pathep-[eth1/1]', targetDscp='unspecified', encapScope='local', llAddr='0.0.0.0', autostate='disabled', mac='00:22:BD:F8:19:FF', mode='regular', encap='vlan-333', ifInstT='ext-svi', mtu='inherit', addr='4.4.4.5/24')
l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP)
l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP)
l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP)
l3extInstP = cobra.model.l3ext.InstP(l3extOut, matchT='AtleastOne', name='NETS_10', prio='unspecified', targetDscp='unspecified', prefGrMemb='exclude', floodOnEncap='disabled')
l3extSubnet = cobra.model.l3ext.Subnet(l3extInstP, ip='10.0.0.0/8')
fvRsCustQosPol = cobra.model.fv.RsCustQosPol(l3extInstP)
infraInfra = cobra.model.infra.Infra(topMo)
infraAttEntityP = cobra.model.infra.AttEntityP(infraInfra, name='SOLO_PORTS_AAEP')
infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn='uni/l3dom-N5K_EXT_DOM')
l3extDomP = cobra.model.l3ext.DomP(topMo, name='N5K_EXT_DOM')
infraRsVlanNs = cobra.model.infra.RsVlanNs(l3extDomP, tDn='uni/infra/vlanns-[N5K_VLANS]-static')


# commit the generated code to APIC
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

