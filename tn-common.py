#!/usr/bin/env python

# list of packages that should be imported for this code to work
import urllib3
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.config
import cobra.model.fabric
import cobra.model.fv
import cobra.model.igmp
import cobra.model.infra
import cobra.model.phys
import cobra.model.pol
import sys
from cobra.internal.codec.xmlcodec import toXMLStr
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from credentials import APIC_IP, APIC_ADMIN, APIC_PASSWORD
except ImportError:
    sys.exit("Error: please verify credentials file format.")

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession(APIC_IP, APIC_ADMIN, APIC_PASSWORD)
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
topMo = cobra.model.pol.Uni('')

# build the request using cobra syntax
fabricInst = cobra.model.fabric.Inst(topMo)
configExportP = cobra.model.config.ExportP(fabricInst, name='defaultOneTime', descr='Added TN-Common and Binding', format='json', adminSt='untriggered', maxSnapshotCount='global-limit', snapshot='yes', includeSecureFields='yes')
fvTenant = cobra.model.fv.Tenant(topMo, name='common')
fvAp = cobra.model.fv.Ap(fvTenant, name='default', prio='unspecified')
fvAEPg = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='COMMON_SVCS', prio='unspecified', prefGrMemb='exclude', floodOnEncap='disabled', pcEnfPref='unenforced')
fvRsPathAtt = cobra.model.fv.RsPathAtt(fvAEPg, tDn='topology/pod-1/protpaths-101-102/pathep-[VPC_B]', primaryEncap='unknown', instrImedcy='immediate', mode='regular', encap='vlan-99')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, tDn='uni/phys-BARE_METAL', netflowDir='both', epgCosPref='disabled', epgCos='Cos0', classPref='encap', primaryEncap='unknown', secondaryEncapInner='unknown', instrImedcy='lazy', primaryEncapInner='unknown', encap='unknown', switchingMode='native', encapMode='auto', netflowPref='disabled', resImedcy='immediate')
fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg)
fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName='default')
fvBD = cobra.model.fv.BD(fvTenant, ipLearning='yes', vmac='not-applicable', name='default', epClear='no', unkMacUcastAct='proxy', arpFlood='no', limitIpLearnToSubnets='yes', multiDstPktAct='bd-flood', OptimizeWanBandwidth='no', mcastAllow='no', mac='00:00:00:00:BD:CC', llAddr='::', intersiteL2Stretch='no', unicastRoute='yes', intersiteBumTrafficAllow='no', type='regular', unkMcastAct='flood')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName='default')
igmpIfP = cobra.model.igmp.IfP(fvBD)
fvSubnet = cobra.model.fv.Subnet(fvBD, ip='192.168.254.254/24', virtual='no', preferred='yes')
infraInfra = cobra.model.infra.Infra(topMo)
infraAttEntityP = cobra.model.infra.AttEntityP(infraInfra, name='MINI_AAEP')
infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn='uni/phys-BARE_METAL')
physDomP = cobra.model.phys.DomP(topMo, name='BARE_METAL')
infraRsVlanNs = cobra.model.infra.RsVlanNs(physDomP, tDn='uni/infra/vlanns-[ESX_VLANS]-dynamic')


# commit the generated code to APIC

c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

