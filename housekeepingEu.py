#!/usr/bin/env python


# list of packages that should be imported for this code to work
import urllib3
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.aaa
import cobra.model.bgp
import cobra.model.comm
import cobra.model.config
import cobra.model.ctrlr
import cobra.model.datetime
import cobra.model.dns
import cobra.model.fabric
import cobra.model.fault
import cobra.model.fv
import cobra.model.latency
import cobra.model.mgmt
import cobra.model.mon
import cobra.model.pki
import cobra.model.pol
import cobra.model.snmp
import cobra.model.syslog
import cobra.model.trig
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
fabricFuncP = cobra.model.fabric.FuncP(fabricInst)
fabricPodPGrp = cobra.model.fabric.PodPGrp(fabricFuncP, name='HOUSEKEEPING_GROUP')
fabricRsSnmpPol = cobra.model.fabric.RsSnmpPol(fabricPodPGrp, tnSnmpPolName='default')
fabricRsPodPGrpIsisDomP = cobra.model.fabric.RsPodPGrpIsisDomP(fabricPodPGrp)
fabricRsPodPGrpCoopP = cobra.model.fabric.RsPodPGrpCoopP(fabricPodPGrp)
fabricRsPodPGrpBGPRRP = cobra.model.fabric.RsPodPGrpBGPRRP(fabricPodPGrp, tnBgpInstPolName='default')
fabricRsTimePol = cobra.model.fabric.RsTimePol(fabricPodPGrp, tnDatetimePolName='AMS-LAB')
fabricRsMacsecPol = cobra.model.fabric.RsMacsecPol(fabricPodPGrp)
fabricRsCommPol = cobra.model.fabric.RsCommPol(fabricPodPGrp)
snmpPol = cobra.model.snmp.Pol(fabricInst, loc='Amsterdam', contact='Joseph Ezerski', name='default', adminSt='disabled')
fabricPodP = cobra.model.fabric.PodP(fabricInst, name='default')
fabricPodS = cobra.model.fabric.PodS(fabricPodP, type='ALL', name='default')
fabricRsPodPGrp = cobra.model.fabric.RsPodPGrp(fabricPodS, tDn='uni/fabric/funcprof/podpgrp-HOUSEKEEPING_GROUP')
commPol = cobra.model.comm.Pol(fabricInst, name='default')
commHttp = cobra.model.comm.Http(commPol, name='http', accessControlAllowCredential='disabled', accessControlAllowOrigins='http://127.0.0.1:8000', maxRequestStatusCount='0', adminSt='enabled', visoreAccess='enabled', throttleSt='enabled', port='80', throttleRate='2', redirectSt='disabled')
datetimeFormat = cobra.model.datetime.Format(fabricInst, showOffset='enabled', tz='p120_Europe-Amsterdam', name='default', displayFormat='local')
latencyPtpMode = cobra.model.latency.PtpMode(fabricInst, latencyPolCount='0', isCountValid='no')
configExportP = cobra.model.config.ExportP(fabricInst, name='defaultOneTime', descr='After HOUSEKEEPING GROUP', format='json', adminSt='untriggered', maxSnapshotCount='global-limit', snapshot='yes', includeSecureFields='yes')
trigSchedP = cobra.model.trig.SchedP(fabricInst, name='ConstCatSchedP')
trigAbsWindowP = cobra.model.trig.AbsWindowP(trigSchedP, procBreak='none', name='ConstAbsWindowP', concurCap='1', procCap='unlimited', date='2014-01-01T01:00:00.000+01:00', timeCap='00:01:00:00.000')
trigSchedP2 = cobra.model.trig.SchedP(fabricInst, name='ConstSchedP')
trigAbsWindowP2 = cobra.model.trig.AbsWindowP(trigSchedP2, procBreak='none', name='ConstAbsWindowP', concurCap='1', procCap='unlimited', date='2014-01-01T01:00:00.000+01:00', timeCap='00:01:00:00.000')
monCommonPol = cobra.model.mon.CommonPol(fabricInst, name='default')
syslogSystemMsgP = cobra.model.syslog.SystemMsgP(monCommonPol, descr='Policy for system syslog messages')
syslogFacilityFilter = cobra.model.syslog.FacilityFilter(syslogSystemMsgP, minSev='information', facility='default')
faultLcP = cobra.model.fault.LcP(monCommonPol, code='generic', descr='Default fault lifecycle policy', soak='12', clear='12', retain='36', name='default')
bgpInstPol = cobra.model.bgp.InstPol(fabricInst, name='default')
bgpRRP = cobra.model.bgp.RRP(bgpInstPol)
bgpRRNodePEp = cobra.model.bgp.RRNodePEp(bgpRRP, id='201', podId='1')
bgpAsP = cobra.model.bgp.AsP(bgpInstPol, asn='65001')
datetimePol = cobra.model.datetime.Pol(fabricInst, name='AMS-LAB', adminSt='enabled', masterMode='disabled', StratumValue='8', authSt='disabled', serverState='disabled')
datetimeNtpProv = cobra.model.datetime.NtpProv(datetimePol, maxPoll='6', keyId='0', name='173.38.201.67', preferred='yes', minPoll='4')
datetimeRsNtpProvToEpg = cobra.model.datetime.RsNtpProvToEpg(datetimeNtpProv, tDn='uni/tn-mgmt/mgmtp-default/oob-default')
dnsProfile = cobra.model.dns.Profile(fabricInst, IPVerPreference='IPv4', name='default')
dnsRsProfileToEpg = cobra.model.dns.RsProfileToEpg(dnsProfile, tDn='uni/tn-mgmt/mgmtp-default/oob-default')
dnsProv = cobra.model.dns.Prov(dnsProfile, addr='173.38.200.100', preferred='yes')
dnsDomain = cobra.model.dns.Domain(dnsProfile, name='cisco.com', isDefault='yes')
trigSchedP3 = cobra.model.trig.SchedP(fabricInst, name='onetime')
ctrlrInst = cobra.model.ctrlr.Inst(topMo)
fabricNodeIdentPol = cobra.model.fabric.NodeIdentPol(ctrlrInst, name='default')
fabricNodeIdentP = cobra.model.fabric.NodeIdentP(fabricNodeIdentPol, nodeType='unspecified', extPoolId='0', podId='1', fabricId='1', nodeId='102', role='unspecified', serial='FDO202521JW', name='leaf-2')
fabricNodeIdentP2 = cobra.model.fabric.NodeIdentP(fabricNodeIdentPol, nodeType='unspecified', extPoolId='0', podId='1', fabricId='1', nodeId='201', role='unspecified', serial='FDO21422G6C', name='spine-1')
fabricNodeIdentP3 = cobra.model.fabric.NodeIdentP(fabricNodeIdentPol, nodeType='unspecified', extPoolId='0', podId='1', fabricId='1', nodeId='103', role='unspecified', serial='FDO21162N03', name='leaf-3')
fabricNodeIdentP4 = cobra.model.fabric.NodeIdentP(fabricNodeIdentPol, nodeType='unspecified', extPoolId='0', podId='1', fabricId='1', nodeId='101', role='unspecified', serial='FDO202521JU', name='leaf-1')
trigSchedP4 = cobra.model.trig.SchedP(ctrlrInst, name='ConstSchedP')
trigAbsWindowP3 = cobra.model.trig.AbsWindowP(trigSchedP4, procBreak='none', name='ConstAbsWindowP', concurCap='1', procCap='unlimited', date='2014-01-01T01:00:00.000+01:00', timeCap='01:00:00:00.000')
fvTenant = cobra.model.fv.Tenant(topMo, name='mgmt')
mgmtMgmtP = cobra.model.mgmt.MgmtP(fvTenant, name='default')
mgmtOoB = cobra.model.mgmt.OoB(mgmtMgmtP, name='default', prio='unspecified')
mgmtRsOoBStNode = cobra.model.mgmt.RsOoBStNode(mgmtOoB, gw='10.50.129.254', v6Gw='::', v6Addr='::', tDn='topology/pod-1/node-201', addr='10.50.129.247/24')
mgmtRsOoBStNode2 = cobra.model.mgmt.RsOoBStNode(mgmtOoB, gw='10.50.129.254', v6Gw='::', v6Addr='::', tDn='topology/pod-1/node-103', addr='10.50.129.244/24')
mgmtRsOoBStNode3 = cobra.model.mgmt.RsOoBStNode(mgmtOoB, gw='10.50.129.254', v6Gw='::', v6Addr='::', tDn='topology/pod-1/node-102', addr='10.50.129.243/24')
mgmtRsOoBStNode4 = cobra.model.mgmt.RsOoBStNode(mgmtOoB, gw='10.50.129.254', v6Gw='::', v6Addr='::', tDn='topology/pod-1/node-101', addr='10.50.129.242/24')
aaaUserEp = cobra.model.aaa.UserEp(topMo, pwdStrengthCheck='no')
aaaPreLoginBanner = cobra.model.aaa.PreLoginBanner(aaaUserEp, switchMessage='This is the ACI Fabric for INSBU in AMS. Authorized Access Only', message='Application Policy Infrastructure Controller')
aaaPwdProfile = cobra.model.aaa.PwdProfile(aaaUserEp, historyCount='0', changeInterval='48', changeCount='2', changeDuringInterval='disable', expirationWarnTime='15', noChangeInterval='24')
pkiEp = cobra.model.pki.Ep(aaaUserEp)
pkiWebTokenData = cobra.model.pki.WebTokenData(pkiEp, uiIdleTimeoutSeconds='65525', sessionRecordFlags='login,logout,refresh', maximumValidityPeriod='24', webtokenTimeoutSeconds='9600')


# commit the generated code to APIC

c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

