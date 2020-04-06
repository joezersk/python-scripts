# python-scripts
**ACI python scripts using ARYA**

These are example python scripts that I use in my lab, generated using the ARYA utility (https://github.com/datacenter/arya).  All values are specific to my setup.  If you want to re-use, you will have to modify things to fit your setup.  

Note:  I use a credentials file to breakout authentication from the script itself.  Just modify the credentials file with your auth values and each script is set up to auto-reference those values.  

* **housekeepingEu.py** - This script sets up what I call 'housekeeping'.  This is the general stuff you do to ACI the first time you set it up and never bother with again.  Stuff like NTP servers, timezones, DNS etc.  

* **physconnEu.py** - This script configures all the front panel ports for end points connected to my fabric. It shows a mix of VPC and single port connected devices.  This is the stuff you find under *Fabric > Fabric Access* tab in APIC. 

* **vmmdomainEu.py** - This script configures a VMM-domain integration with vCenter.  Note, it will not carry the vCenter authentication values in the script, so after adding, you will need to manually type in the password for the vCenter auth object in APIC, under the *Virtual Networking Tab*

* **tn-common.py** - This scripts sets up basic networking and EPGs in tenant-common.  

* **L3OutEu.py** - This script configures an L3Out using OSPF
