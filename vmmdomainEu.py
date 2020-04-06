#!/usr/bin/env python

# list of packages that should be imported for this code to work
import urllib3
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.config
import cobra.model.fabric
import cobra.model.infra
import cobra.model.pol
import cobra.model.vmm
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
configExportP = cobra.model.config.ExportP(fabricInst, name='defaultOneTime', descr='Added Base VMM Domain ESX', format='json', adminSt='untriggered', maxSnapshotCount='global-limit', snapshot='yes', includeSecureFields='yes')
vmmProvP = cobra.model.vmm.ProvP(topMo, vendor='VMware')
vmmDomP = cobra.model.vmm.DomP(vmmProvP, mcastAddr='0.0.0.0', name='VC_DVS', accessMode='read-write', prefEncapMode='unspecified', ctrlKnob='epDpVerify', mode='default', enableAVE='no', enfPref='hw', encapMode='unknown', epRetTime='0')
vmmVSwitchPolicyCont = cobra.model.vmm.VSwitchPolicyCont(vmmDomP)
vmmRsVswitchOverrideLldpIfPol = cobra.model.vmm.RsVswitchOverrideLldpIfPol(vmmVSwitchPolicyCont, tDn='uni/infra/lldpIfP-LLDP_OFF')
vmmRsVswitchOverrideLacpPol = cobra.model.vmm.RsVswitchOverrideLacpPol(vmmVSwitchPolicyCont, tDn='uni/infra/lacplagp-MAC_PIN')
vmmRsVswitchOverrideCdpIfPol = cobra.model.vmm.RsVswitchOverrideCdpIfPol(vmmVSwitchPolicyCont, tDn='uni/infra/cdpIfP-CDP_ON')
vmmUsrAccP = cobra.model.vmm.UsrAccP(vmmDomP, name='VC_ADMIN', usr='admin@vsphere.local')
vmmRsDefaultStpIfPol = cobra.model.vmm.RsDefaultStpIfPol(vmmDomP)
vmmRsDefaultLacpLagPol = cobra.model.vmm.RsDefaultLacpLagPol(vmmDomP)
vmmRsDefaultL2InstPol = cobra.model.vmm.RsDefaultL2InstPol(vmmDomP)
vmmRsDefaultFwPol = cobra.model.vmm.RsDefaultFwPol(vmmDomP)
vmmRsDefaultCdpIfPol = cobra.model.vmm.RsDefaultCdpIfPol(vmmDomP)
vmmRsDefaultLldpIfPol = cobra.model.vmm.RsDefaultLldpIfPol(vmmDomP)
vmmCtrlrP = cobra.model.vmm.CtrlrP(vmmDomP, n1kvStatsMode='enabled', name='VC6', seqNum='0', inventoryTrigSt='untriggered', statsMode='enabled', port='0', vxlanDeplPref='vxlan', mode='default', dvsVersion='6.0', hostOrIp='10.50.129.204', rootContName='AMS6')
vmmRsAcc = cobra.model.vmm.RsAcc(vmmCtrlrP, tDn='uni/vmmp-VMware/dom-VC_DVS/usracc-VC_ADMIN')
infraRsVlanNs = cobra.model.infra.RsVlanNs(vmmDomP, tDn='uni/infra/vlanns-[ESX_VLANS]-dynamic')

c = cobra.mit.request.ConfigRequest()
c.addMo(vmmDomP)
md.commit(c)

infraInfra = cobra.model.infra.Infra(topMo)
infraAttEntityP = cobra.model.infra.AttEntityP(infraInfra, name='MINI_AAEP')
infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn='uni/vmmp-VMware/dom-VC_DVS')

# commit the generated code to APIC
c = cobra.mit.request.ConfigRequest()
c.addMo(infraInfra)
md.commit(c)

