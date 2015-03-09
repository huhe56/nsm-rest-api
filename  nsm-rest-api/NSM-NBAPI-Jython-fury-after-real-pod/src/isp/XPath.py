'''
Created on Jul 15, 2012

@author: huhe
'''



_PodParameterType   = '//*[local-name()="property" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"][*[local-name()="name"]="${parameter-name}"]/*[local-name()="type"]/text()'
_PodStringTypeValue = '//*[local-name()="property" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"][*[local-name()="name"]="${parameter-name}"]/*[local-name()="string"]/text()'

_PodVlanRangeStart  = '//*[local-name()="property" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"][*[local-name()="name"]="pod.device.vlanpool"]/*[local-name()="range"]/*[local-name()="start"]/text()'
_PodVlanRangeEnd    = '//*[local-name()="property" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"][*[local-name()="name"]="pod.device.vlanpool"]/*[local-name()="range"]/*[local-name()="end"]/text()'

_TaskResponseProperty   = '//*[local-name()="property" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"][*[local-name()="name"]="${property-name}"]/*[local-name()="${property-type}"]/text()'

_CatalogServiceOfferings = '/*[local-name()="serviceOfferings" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'
_CatalogServiceOffering  = _CatalogServiceOfferings + '/*[local-name()="serviceOffering" and @*[local-name()="type"]="${offering-type}"][*[local-name()="name"]="${offering-name}"]'

_CatalogUid         = _CatalogServiceOffering + '/*[local-name()="uid"]/text()'
_CatalogName        = _CatalogServiceOffering + '/*[local-name()="name"]/text()'
_CatalogDescription = _CatalogServiceOffering + '/*[local-name()="description"]/text()'
_CatalogVersion     = _CatalogServiceOffering + '/*[local-name()="version"]/text()'

_CatalogLinksLinkTitle  = _CatalogServiceOffering + '/*[local-name()="links"][*[local-name()="link" and @*[local-name()="title"]="${link-title}"]]'
_CatalogLinkSelf        = _CatalogLinksLinkTitle + '/*[local-name()="link" and @*[local-name()="rel"]="self"]/@*[local-name()="href"]'
_CatalogLinkCreate      = _CatalogLinksLinkTitle + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:create"]/@*[local-name()="href"]'


_TaskTask       = '/*[local-name()="task" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'

_TaskUid        = _TaskTask + '/*[local-name()="uid"]/text()'
_TaskName       = _TaskTask + '/*[local-name()="name"]/text()'

_TaskLinks      = _TaskTask + '/*[local-name()="links"]'
_TaskLink       = _TaskLinks + '/*[local-name()="link" and @*[local-name()="rel"]="self"]'
_TaskLinkSelf   = _TaskLink + '/@*[local-name()="href"]'

_TaskStatus         = _TaskTask + '/*[local-name()="status"]'
_TaskTaskStatus     = _TaskStatus + '/*[local-name()="taskStatus"]/text()'
_TaskResponseCode   = _TaskStatus + '/*[local-name()="responseCode"]/text()'

_TaskFaults         = _TaskTask + '/*[local-name()="faults"]'
_TaskFault          = _TaskFaults + '/*[local-name()="fault"]'
_TaskFaultType      = _TaskFault + '/*[local-name()="faultType"]/text()'
_TaskFaultMessag    = _TaskFault + '/*[local-name()="message"]/text()'
_TaskFaultArguments = _TaskFault + '/*[local-name()="arguments"]/text()'


_TaskResult     = _TaskTask + '/*[local-name()="result"]'
_TaskElementUid = _TaskResult + '/*[local-name()="uid"]/text()'

_DetailLinks        =  '//*[local-name()="links" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'
_DetailLink         = _DetailLinks + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:catalog"]'
_DetailLinkCatalog  = _DetailLink + '/@*[local-name()="href"]'

_DetailLinkListPod      = _DetailLinks + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:pods"]'
_DetailLinkListPodHref  = _DetailLinkListPod + '/@*[local-name()="href"]'


_DetailUid  = '/*/*[local-name()="uid" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]/text()'

_DetailFirstUidFromList  = '/*/*/*[local-name()="uid" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]/text()'

_DetailLinkTenant       = _DetailLinks + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:tenants"]'
_DetailLinkTenantHref   = _DetailLinkTenant + '/@*[local-name()="href"]'



_RequestBodyServiceOffering = '/*[local-name()="serviceOffering" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'
_RequestBodyName = _RequestBodyServiceOffering + '/*[local-name()="name"]/text()'
_RequestBodyDescription = _RequestBodyServiceOffering + '/*[local-name()="description"]/text()'

_Links = '//*[local-name()="links" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'

_ProviderGlobalIpAddressPool   = _Links + '/*[local-name()="link" and @*[local-name()="title"]="Global IP Address Pool" and @*[local-name()="rel"]="nsmr:ipaddresspool"]'
_LinkProviderGlobalIpAddressPool = _ProviderGlobalIpAddressPool + '/@*[local-name()="href"]'

_ProviderInfrastructureIpAddressPool   = _Links + '/*[local-name()="link" and @*[local-name()="title"]="Infrastructure IP Address Pool" and @*[local-name()="rel"]="nsmr:ipaddresspool"]'
_LinkProviderInfrastructureIpAddressPool = _ProviderInfrastructureIpAddressPool + '/@*[local-name()="href"]'

_TenantRoutablePrivateIpAddressPool   = _Links + '/*[local-name()="link" and @*[local-name()="title"]="Routable Private IP Address Pool" and @*[local-name()="rel"]="nsmr:ipaddresspool"]'
_LinkTenantRoutablePrivateIpAddressPool = _TenantRoutablePrivateIpAddressPool + '/@*[local-name()="href"]'

_ExternalAccessLayer3VlanSubPool1   = _Links + '/*[local-name()="link" and contains(@*[local-name()="title"], "SubPool") and @*[local-name()="rel"]="nsmr:ipaddresspool"]'
_LinkExternalAccessLayer3VlanSubPool1 = _ExternalAccessLayer3VlanSubPool1 + '/@*[local-name()="href"]'


_IpReservation = _Links + '/*[local-name()="link" and @*[local-name()="rel"]="${rel}"]'
_LinkIpReservation = _IpReservation + '/@*[local-name()="href"]'

_TaskElementIpReservationUid =  _TaskResult + '/*[local-name()="ipReservation"]/*[local-name()="uid"]/text()'


_TopIndexLinks              =  '//*[local-name()="links" and namespace-uri()="http://www.cisco.com/NetworkServicesManager/1.1"]'
_TopIndexCatalogLink        = _TopIndexLinks + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:catalog"]'
_TopIndexCatalogLinkHref    = _TopIndexCatalogLink + '/@*[local-name()="href"]'

_TopIndexListProviderLink       = _TopIndexLinks + '/*[local-name()="link" and @*[local-name()="rel"]="nsmr:providers"]'
_TopIndexListProviderLinkHref   = _TopIndexListProviderLink + '/@*[local-name()="href"]' 





