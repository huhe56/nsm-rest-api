'''
Created on Jul 15, 2012

@author: huhe
'''

'''
Created on Jul 14, 2012

@author: huhe
'''

from isp.performance import Performance


_HostEngine = 'od-c3-nsve'

''' This is the index of first tenant that will be created in next run, it must be great than 0 '''
_TenantStartIndex = 1

''' This is the total tenants you will create in next run, it must be great than 0 '''
_TenantCount = 1


_PortEngine = '8443'
_UrlHostPortEngine = 'https://' + _HostEngine + ':' + _PortEngine



_ResetNSM                   = False
_ResetDevice                = False
_CopyCleanRunningConfig     = False
_DiffClean                  = False

_DummyAgent                 = True
_SetDSCLoggingDebug         = False

_SaveNSMLog                 = False
_CopyCreateRunningConfig    = False

_DeviceVerification         = False


_Update = False
_UpdateSingleMetaProperties = False
_UpdateAllMetaProperties = True


_Verfiy = False
_VerifyCreate = True
_VerifyUpdate = True
_VerifyDelete = False


_Positive   = True
_Negative   = True


_StressTest  = False
_PodIndex    = 0
_TenantIndex = 0


_Performance            = False
_CurrentPerfClassName   = None
_CurrentPerfObjectName  = None
_CurrentPerfAction      = None
_PerformanceData        = Performance()
_NonPerformanceClassList = ['NsmV1', 'Top', 'Provider', 'Tenant']


### should be populated dynamically
_VCenterIP = '192.168.66.153'
_DvsUuid = 'b8323250-ffe0-b2c9-aaac-084b9ce7aef1'

_GlobalIP       = '179.0.0.0'
_GlobalIPMask   = 20
_GlobalIPSubnet = _GlobalIP + '/' + str(_GlobalIPMask) 

_InfrastructureIP       = '129.0.0.'
_InfrastructureIPMask   = 20
_InfrastructureIPSubnet = _InfrastructureIP + '/' + str(_InfrastructureIPMask)

_PrivateIP          = '192.168.0.0'
_PrivateIPMask      = 16
_PrivateIPSubnet    = _PrivateIP + '/' + str(_PrivateIPMask)
### should be populated dynamically


_UpdateJsonFileName = 'update/update-provider.json'

_Delete = True


_PathTmp = '/Users/huhe/Install/workspace/tmp'
_PathRoot = '/Users/huhe/Install/workspace/NSM-NBAPI-Jython'


_PathSource = _PathRoot + '/src'

_PathTestCase = _PathRoot + '/test-case'
_PathUpdate = _PathSource + '/update'

_PathRequestRoot                = _PathRoot + '/request'
_PathRequestCreate              = _PathRequestRoot + '/create'
_PathRequestBodyCreateDefault   = _PathRequestCreate + '/request-body-create-default'
_PathRequestBodyCreateSetup     = _PathRequestCreate + '/request-body-create-setup'

_PathRequestUpdate      = _PathRequestRoot + '/update'
_PathReqeustBodyUpdate  = _PathRequestUpdate + '/request-body-update'

_PathResponse               = _PathRoot + '/response'
_PathResponseCreate         = _PathResponse + '/create'
_PathResponseCreateDefault  = _PathResponseCreate + '/response-create-default'
_PathResponseCreateSetup    = _PathResponseCreate + '/response-create-setup'


_PathResponseGoldenData                 = _PathRoot + '/response-golden-data'
_PathResponseGoldenDataCreate           = _PathResponseGoldenData + '/create'
_PathResponseGoldenDataCreateDefault    = _PathResponseGoldenDataCreate + '/response-create-default'


_PathResponseUpdate = _PathResponse + '/update'
_PathResponseDelete = _PathResponse + '/delete'

_PathLog        = _PathRoot + '/log'
_PathUidDefault = _PathLog + '/uid-default.txt'
_PathUidSetup   = _PathLog + '/uid-setup.txt'
_PathResultDefault = _PathLog + '/result-default.txt'
_PathLogFile    = _PathLog + '/test-log.txt'
_PathSchemaFile = _PathLog + '/xsd.xml'
_PathScreenShotFile = _PathLog + '/acp-start-screenshot.png'


_PathDevice     = _PathSource + '/device'
_PathDeviceCmd  = _PathDevice + '/cmd'


_UrlSchemaRoot      = _UrlHostPortEngine + '/NetworkServicesManagerAPI/v1/schema'
_UrlSchemaNSM       = _UrlSchemaRoot + '/NetworkServicesManager-1.1.0.xsd'
_UrlSchemaAtom      = _UrlSchemaRoot + '/ATOM-1.0.xsd'
_UrlSchemaNameSpace = _UrlSchemaRoot + '/XML-Namespace-1998.xsd'

_PathSchemaRoot         = _PathRoot + '/schema'
_PathSchemaNsm          = _PathSchemaRoot + '/nsm.xsd'
_PathSchemaAtom         = _PathSchemaRoot + '/ATOM-1.0.xsd'
_PathSchemaNameSpace    = _PathSchemaRoot + '/XML-Namespace-1998.xsd'

_UriApiRoot = '/NetworkServicesManagerAPI/v1'
_UrlApiRoot = _UrlHostPortEngine + _UriApiRoot
    
_Username = 'admin'
_Password = 'admin'
_credential = 'Basic YWRtaW46YWRtaW4='

_DescriptionPrefix = 'This is the description of '

_ElementClassDefaultRequestBodyFileMapping = {
    'Provider': 'provider.xml',
    'Pod': 'pod.xml',
    'Tenant': 'tenant.xml',
    'ExternalNetwork': 'external-network.xml',
    'TenantNetworkContainer': 'tenant-network-container.xml',
    'ExternalConnection': 'external-connection.xml',
    'PrivateMplsConnection': 'private-mpls-connection.xml',
    'InternetEdgeZone': 'internet-edge-zone.xml',
    'SecuredInternetEdgeZone': 'secured-internet-edge-zone.xml',
    'PrivateEdgeZone': 'private-edge-zone.xml',
    'SecuredPrivateEdgeZone': 'secured-private-edge-zone.xml',
    'Layer3ExternalAccessVlan': 'layer3-external-access-vlan.xml',
    'FirewallService': 'firewall-service.xml',
    'LoadBalanceService': 'load-balance-service.xml'
}


# setup.json, setup-pod.xml, setup-pod-offline.json
_SetupJsonFileName = _PathSource + '/setup/setup-pod-offline.json'
_SetupGlobalOnLine = True

def __init__(self):
    '''
    Constructor
    '''
        
        