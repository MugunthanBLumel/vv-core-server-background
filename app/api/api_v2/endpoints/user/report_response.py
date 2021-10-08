import json
import random


def get_reports(start,agent_instance_user_id_list=[1], bi_report_count=20):
    result = []
    reports = json.loads(
        """{
         "user_metadata":{
            "id":"ATXb3J3RcpdOqKkgzJ9Ta4o",
            "username":"srvadm"
         },
         "agent_name":"BOBJ_REST",
         "config":{
            "INSTANCE_NAME":"BOBJ_Checknew",
            "USERNAME":"Administrator",
            "AUTHENTICATION_TYPE":"HTTP_HEADER",
            "HEADER":"X-SAP-TRUSTED-USER",
            "SERVER_URL":"http: //solutionsbobj.visualbi.solutions:8070",
            "WACS_URL":"http://vbi-sol-bobj.visualbi.solutions:6405",
            "LOG_TRACE":false,
            "FILTER_LIST":[
               
            ]
         },
         "triggered_by":"admin",
         "reports":[
            {
               "description":"Shows how data can be visualized on different kinds of charts. And the features supported on the charts.",
               "name":"Chart Demo",
               "report_id":"AZx1nlTlCMdCvyJ6bWUTC5I",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AZx1nlTlCMdCvyJ6bWUTC5I&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AZx1nlTlCMdCvyJ6bWUTC5I&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"Jan 4, 2018 12:58 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"May 4, 2017 7:43 PM",
                  "Schedule End Time":"May 4, 2027 7:43 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AZx1nlTlCMdCvyJ6bWUTC5I"
               }
            },
            {
               "description":"Shows how Input Controls can be used to filter the entire report, or individual tables or charts.",
               "name":"Input Controls & Filter Demo",
               "report_id":"AU8SwOvit8dNsDrBhKcWgog",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AU8SwOvit8dNsDrBhKcWgog&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AU8SwOvit8dNsDrBhKcWgog&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Dec 19, 2012 10:09 PM",
                  "Schedule End Time":"Dec 19, 2022 10:09 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AU8SwOvit8dNsDrBhKcWgog"
               }
            },
            {
               "description":"Shows Google maps with a geo-data  overlay. You can switch measures, data point icons, and visualize charts for a given data point.",
               "name":"Geo Analysis Demo",
               "report_id":"AY.sKzGgXcpMge9B1xMPOlU",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AY.sKzGgXcpMge9B1xMPOlU&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AY.sKzGgXcpMge9B1xMPOlU&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Dec 19, 2012 10:09 PM",
                  "Schedule End Time":"Dec 19, 2022 10:09 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AY.sKzGgXcpMge9B1xMPOlU"
               }
            },
            {
               "description":"Shows how the data can be divided into sections and features supported on sections.",
               "name":"Sections Demo",
               "report_id":"AXHs6mETheJLgqA6OnZ0Fp0",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXHs6mETheJLgqA6OnZ0Fp0&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXHs6mETheJLgqA6OnZ0Fp0&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Dec 19, 2012 10:09 PM",
                  "Schedule End Time":"Dec 19, 2022 10:09 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AXHs6mETheJLgqA6OnZ0Fp0"
               }
            },
            {
               "description":"Displaying the data in different kinds of Tables supported and the features supported on table.",
               "name":"Mobile - Table Demo",
               "report_id":"AXxv4ZR4kntKr1OJ1Kv9Hs0",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXxv4ZR4kntKr1OJ1Kv9Hs0&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXxv4ZR4kntKr1OJ1Kv9Hs0&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Dec 19, 2012 10:09 PM",
                  "Schedule End Time":"Dec 19, 2022 10:09 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AXxv4ZR4kntKr1OJ1Kv9Hs0"
               }
            },
            {
               "description":"This document demonstrates the drill functionality on tables and Charts",
               "name":"Drill Demo",
               "report_id":"AS9ukIRdciZLuUS6ESGVRBg",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AS9ukIRdciZLuUS6ESGVRBg&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AS9ukIRdciZLuUS6ESGVRBg&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//Mobile Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Dec 19, 2012 10:09 PM",
                  "Schedule End Time":"Dec 19, 2022 10:09 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:43 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AS9ukIRdciZLuUS6ESGVRBg"
               }
            },
            {
               "description":"",
               "name":"Formatting Sample",
               "report_id":"AQtkbbSqN4NOj3ydf.Sw1lY",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AQtkbbSqN4NOj3ydf.Sw1lY&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AQtkbbSqN4NOj3ydf.Sw1lY&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:44 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Jul 21, 2011 9:39 AM",
                  "Schedule End Time":"Jul 21, 2021 9:39 AM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:44 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AQtkbbSqN4NOj3ydf.Sw1lY"
               }
            },
            {
               "description":"Web Intelligence 4.0 sample\nExample of detailed report implementing input controls and element links",
               "name":"Input Controls And Charts",
               "report_id":"AVOEBpPXOvpGhcrzzE_RAeY",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AVOEBpPXOvpGhcrzzE_RAeY&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AVOEBpPXOvpGhcrzzE_RAeY&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:44 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Jul 21, 2011 9:39 AM",
                  "Schedule End Time":"Jul 21, 2021 9:39 AM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:44 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AVOEBpPXOvpGhcrzzE_RAeY"
               }
            },
            {
               "description":"",
               "name":"Charting Samples",
               "report_id":"AW4AVT1AUhVAogA6P7OQv9c",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AW4AVT1AUhVAogA6P7OQv9c&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AW4AVT1AUhVAogA6P7OQv9c&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"Aug 16, 2021 3:52 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Jul 21, 2011 9:39 AM",
                  "Schedule End Time":"Jul 21, 2021 9:39 AM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:44 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AW4AVT1AUhVAogA6P7OQv9c"
               }
            },
            {
               "description":"",
               "name":"Fold Unfold Sample",
               "report_id":"AXpyoryP_Z5BoXVoM2_3kWQ",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXpyoryP_Z5BoXVoM2_3kWQ&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXpyoryP_Z5BoXVoM2_3kWQ&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:44 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Jul 21, 2011 9:39 AM",
                  "Schedule End Time":"Jul 21, 2021 9:39 AM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:44 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AXpyoryP_Z5BoXVoM2_3kWQ"
               }
            },
            {
               "description":"How input controls can be used to filter report content, and assign values to variables.\nUser can leverage these capacities to control report display and perform what-if analysis.",
               "name":"Input Controls and variables",
               "report_id":"AXb0jR1xevFLlX5hpPUGu.4",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXb0jR1xevFLlX5hpPUGu.4&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AXb0jR1xevFLlX5hpPUGu.4&sIDType=CUID&token={token}",
               "path":"Web Intelligence Samples//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:44 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Jul 21, 2011 9:39 AM",
                  "Schedule End Time":"Jul 21, 2021 9:39 AM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:44 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AXb0jR1xevFLlX5hpPUGu.4"
               }
            },
            {
               "description":"",
               "name":"MonitoringTrend Data-Sample",
               "report_id":"ATeBlMbXn.xCuSaEElUEGI0",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=ATeBlMbXn.xCuSaEElUEGI0&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=ATeBlMbXn.xCuSaEElUEGI0&sIDType=CUID&token={token}",
               "path":"Monitoring Report Sample//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"May 4, 2017 7:45 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Nov 10, 2011 3:04 PM",
                  "Schedule End Time":"Nov 10, 2021 3:04 PM",
                  "Type":"Webi",
                  "Creation Time":"May 4, 2017 7:45 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"ATeBlMbXn.xCuSaEElUEGI0"
               }
            },
            {
               "description":"",
               "name":"Report Conversion Tool Audit Statistics Report",
               "report_id":"AZW60OSD3NdJsgxaZgiScRY",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AZW60OSD3NdJsgxaZgiScRY&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=AZW60OSD3NdJsgxaZgiScRY&sIDType=CUID&token={token}",
               "path":"Report Conversion Tool//Report Conversion Tool Documents//Report Conversion Tool Audit Documents//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"Mar 6, 2019 5:47 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"Aug 8, 2007 7:19 PM",
                  "Schedule End Time":"Aug 8, 2017 7:19 PM",
                  "Type":"Webi",
                  "Creation Time":"Mar 12, 2008 3:46 PM",
                  "Read Only":false,
                  "report_type":"Webi",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"AZW60OSD3NdJsgxaZgiScRY"
               }
            },
            {
               "description":"",
               "name":"Comparative Income Statement",
               "report_id":"Afp4QLdyJXZMglytQ5ygu_s",
               "url":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=Afp4QLdyJXZMglytQ5ygu_s&sIDType=CUID&token={token}",
               "url_t":"http://solutionsbobj.visualbi.solutions:8070/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=Afp4QLdyJXZMglytQ5ygu_s&sIDType=CUID&token={token}",
               "path":"Report Samples//Demonstration//",
               "meta":{
                  "Data Provider":"",
                  "Source Systems":"",
                  "Links To Other Reports":"",
                  "Last Refresh Date Time":"Dec 26, 2018 3:43 PM",
                  "Owner":"Administrator",
                  "Scheduled":true,
                  "Refresh Frequency":"Once",
                  "Schedule Start Time":"May 4, 2017 7:45 PM",
                  "Schedule End Time":"May 4, 2027 7:45 PM",
                  "Type":"CrystalReport",
                  "Creation Time":"May 4, 2017 7:45 PM",
                  "Read Only":false,
                  "report_type":"CrystalReport",
                  "Tags":""
               },
               "sync_metadata":{
                  "report_id":"Afp4QLdyJXZMglytQ5ygu_s"
               }
            }
         ]
      }""",
        strict=False,
    )
    
    for id,agent_instance_user_id in enumerate(agent_instance_user_id_list):
        if start==0 and id<100:
            bi_report_count = 25000
        elif start ==0 and id>=100 and id<200:
            bi_report_count = 5000
        elif  start ==0 and id>=200 and id<300:
           bi_report_count = 1000
        else:
            bi_report_count = 10
        if agent_instance_user_id==1:
            bi_report_count=0
         
        report_list = []
        for report_id in range(1, bi_report_count + 1):
            id = random.randrange(1, 10000000)
            id = report_id 
            random_report = reports["reports"][0]
            # random_report = random.choice(reports["reports"])

            report_copy = random_report
            if True or random.randrange(1, 10) == 3:
                report_copy = random_report.copy()
                report_copy["name"] += f"_{id}"
                report_copy["report_id"] += f"_{id}"
                report_copy["path"] += f"_{id}//"

            if not  ( (report_id==1 or agent_instance_user_id==1 )):
                report_list.append(report_copy)
        result.append((agent_instance_user_id, report_list))

    return result

user_rep = json.loads('''{
  "event_id": "ee25ae08-250e-4cda-9148-e8f65348b749", 
  "instance_info": {
    "agent_name": "BOBJ_REST", 
    "config": {
      "AUTHENTICATION_TYPE": "HTTP_HEADER", 
      "FILTER_LIST": [], 
      "HEADER": "X-SAP-TRUSTED-USER", 
      "INSTANCE_NAME": "BOBJ_Checknew", 
      "LOG_TRACE": false, 
      "SERVER_URL": "http://solutionsbobj.visualbi.solutions:8070", 
      "USERNAME": "Administrator", 
      "WACS_URL": "http://vbi-sol-bobj.visualbi.solutions:6405"
    }, 
    "user_metadata": {
      "id": "AW2ea0JHvcBJqxIdMbNRtoA", 
      "username": "biadm"
    }
  }, 
  "users_list": [
    {
      "id": "AXRIk1NsORpMgzn3GCyxcxo", 
      "metadata": {
        "id": "AXRIk1NsORpMgzn3GCyxcxo", 
        "username": "nithyar"
      }, 
      "username": "nithyar"
    }, 
    {
      "id": "ATNZHwXWXsxNpjZOnQdpKp4", 
      "metadata": {
        "id": "ATNZHwXWXsxNpjZOnQdpKp4", 
        "username": "vbiviewdemo0"
      }, 
      "username": "vbiviewdemo0"
    }, 
    {
      "id": "Ae48ikE7WSFEpewYWUV1W5M", 
      "metadata": {
        "id": "Ae48ikE7WSFEpewYWUV1W5M", 
        "username": "srv100"
      }, 
      "username": "srv100"
    }, 
    {
      "id": "AUtmLSTDEU1IgrI_hTaJnmw", 
      "metadata": {
        "id": "AUtmLSTDEU1IgrI_hTaJnmw", 
        "username": "srv090"
      }, 
      "username": "srv090"
    }, 
    {
      "id": "AQI1_YDFUi9LrhapkQX6HRs", 
      "metadata": {
        "id": "AQI1_YDFUi9LrhapkQX6HRs", 
        "username": "srv080"
      }, 
      "username": "srv080"
    }, 
    {
      "id": "AffAG4YwgBdNnPd34.M2OK8", 
      "metadata": {
        "id": "AffAG4YwgBdNnPd34.M2OK8", 
        "username": "srv070"
      }, 
      "username": "srv070"
    }, 
    {
      "id": "Ab22HJlz4sNFi3MUYFC9Mqs", 
      "metadata": {
        "id": "Ab22HJlz4sNFi3MUYFC9Mqs", 
        "username": "srv060"
      }, 
      "username": "srv060"
    }, 
    {
      "id": "AanBkF7MfqxEqTT7.qqlj0Y", 
      "metadata": {
        "id": "AanBkF7MfqxEqTT7.qqlj0Y", 
        "username": "srv050"
      }, 
      "username": "srv050"
    }, 
    {
      "id": "AQqgSP64RXNJvSEYjY7mVFI", 
      "metadata": {
        "id": "AQqgSP64RXNJvSEYjY7mVFI", 
        "username": "sapsupport"
      }, 
      "username": "sapsupport"
    }, 
    {
      "id": "AZCh5wFPbj1JrvQrW43rNns", 
      "metadata": {
        "id": "AZCh5wFPbj1JrvQrW43rNns", 
        "username": "vv00046"
      }, 
      "username": "vv00046"
    }, 
    {
      "id": "AXPurjX2fZBDlIwGmKTW37Q", 
      "metadata": {
        "id": "AXPurjX2fZBDlIwGmKTW37Q", 
        "username": "vv00012"
      }, 
      "username": "vv00012"
    }, 
    {
      "id": "Acz29jCeMPFMk3ZOr5TtWOM", 
      "metadata": {
        "id": "Acz29jCeMPFMk3ZOr5TtWOM", 
        "username": "vv00026"
      }, 
      "username": "vv00026"
    }, 
    {
      "id": "AZrSiaVC_GNAsF6W2gxltx0", 
      "metadata": {
        "id": "AZrSiaVC_GNAsF6W2gxltx0", 
        "username": "vv00020"
      }, 
      "username": "vv00020"
    }, 
    {
      "id": "AWC.R.Hf4dNNioSC9dRvxqw", 
      "metadata": {
        "id": "AWC.R.Hf4dNNioSC9dRvxqw", 
        "username": "vv00008"
      }, 
      "username": "vv00008"
    }, 
    {
      "id": "AfL4SnPN_Z5KpMQpuxR2cRg", 
      "metadata": {
        "id": "AfL4SnPN_Z5KpMQpuxR2cRg", 
        "username": "vv00010"
      }, 
      "username": "vv00010"
    }, 
    {
      "id": "ASwYLIAzyGdHgDw8E_mAw2g", 
      "metadata": {
        "id": "ASwYLIAzyGdHgDw8E_mAw2g", 
        "username": "vv00007"
      }, 
      "username": "vv00007"
    }, 
    {
      "id": "ASFodg19nr5EtBn2H_1krx4", 
      "metadata": {
        "id": "ASFodg19nr5EtBn2H_1krx4", 
        "username": "vv00037"
      }, 
      "username": "vv00037"
    }, 
    {
      "id": "ATqzWcJbDaVOrrYjfUPZ698", 
      "metadata": {
        "id": "ATqzWcJbDaVOrrYjfUPZ698", 
        "username": "vv00048"
      }, 
      "username": "vv00048"
    }, 
    {
      "id": "AQveTceulKFBndt7rFogHGc", 
      "metadata": {
        "id": "AQveTceulKFBndt7rFogHGc", 
        "username": "vv00035"
      }, 
      "username": "vv00035"
    }, 
    {
      "id": "AbBKq3N06kNKtq.BCyIy5No", 
      "metadata": {
        "id": "AbBKq3N06kNKtq.BCyIy5No", 
        "username": "vv00036"
      }, 
      "username": "vv00036"
    }, 
    {
      "id": "AZPbX62BCMlLkFxdhEuH4SM", 
      "metadata": {
        "id": "AZPbX62BCMlLkFxdhEuH4SM", 
        "username": "vv00009"
      }, 
      "username": "vv00009"
    }, 
    {
      "id": "AYvfR67ohOhHmeLYEqCUDpA", 
      "metadata": {
        "id": "AYvfR67ohOhHmeLYEqCUDpA", 
        "username": "vv00047"
      }, 
      "username": "vv00047"
    }, 
    {
      "id": "Ad8W83S8m55EuRuWC9mzPog", 
      "metadata": {
        "id": "Ad8W83S8m55EuRuWC9mzPog", 
        "username": "vv00031"
      }, 
      "username": "vv00031"
    }, 
    {
      "id": "Ae4ocLpvZkhFpfctom0me9Q", 
      "metadata": {
        "id": "Ae4ocLpvZkhFpfctom0me9Q", 
        "username": "vv00019"
      }, 
      "username": "vv00019"
    }, 
    {
      "id": "AaWo7BvKR_1LshyPH6K8_qA", 
      "metadata": {
        "id": "AaWo7BvKR_1LshyPH6K8_qA", 
        "username": "vv00022"
      }, 
      "username": "vv00022"
    }, 
    {
      "id": "AY8dgiMzzcBGvnZEYlL6xow", 
      "metadata": {
        "id": "AY8dgiMzzcBGvnZEYlL6xow", 
        "username": "vv00002"
      }, 
      "username": "vv00002"
    }, 
    {
      "id": "AUmG.SHPId5GjKc1v06b5FU", 
      "metadata": {
        "id": "AUmG.SHPId5GjKc1v06b5FU", 
        "username": "vv00005"
      }, 
      "username": "vv00005"
    }, 
    {
      "id": "AdB9L.FtHm1MtT6BdUngwyE", 
      "metadata": {
        "id": "AdB9L.FtHm1MtT6BdUngwyE", 
        "username": "vv00021"
      }, 
      "username": "vv00021"
    }, 
    {
      "id": "AaIq4Nv5vG5GilqyJF_mNEU", 
      "metadata": {
        "id": "AaIq4Nv5vG5GilqyJF_mNEU", 
        "username": "vv00034"
      }, 
      "username": "vv00034"
    }, 
    {
      "id": "AWz06HmgAVxFoRuMU93HNa0", 
      "metadata": {
        "id": "AWz06HmgAVxFoRuMU93HNa0", 
        "username": "vv00006"
      }, 
      "username": "vv00006"
    }, 
    {
      "id": "AX_xnnrmb.hAvgnKZRh7HBA", 
      "metadata": {
        "id": "AX_xnnrmb.hAvgnKZRh7HBA", 
        "username": "vv00001"
      }, 
      "username": "vv00001"
    }, 
    {
      "id": "AYmAm3BUwcBGmf5hdVSejcs", 
      "metadata": {
        "id": "AYmAm3BUwcBGmf5hdVSejcs", 
        "username": "vv00027"
      }, 
      "username": "vv00027"
    }, 
    {
      "id": "AZwazhnH2wlGjGOXNrxbz8Y", 
      "metadata": {
        "id": "AZwazhnH2wlGjGOXNrxbz8Y", 
        "username": "vv00018"
      }, 
      "username": "vv00018"
    }, 
    {
      "id": "AaIffnNU6aZDrblBGOLkKF4", 
      "metadata": {
        "id": "AaIffnNU6aZDrblBGOLkKF4", 
        "username": "vv00017"
      }, 
      "username": "vv00017"
    }, 
    {
      "id": "AbTuGxt6gaBHpsM_T7pvpOU", 
      "metadata": {
        "id": "AbTuGxt6gaBHpsM_T7pvpOU", 
        "username": "vv00032"
      }, 
      "username": "vv00032"
    }, 
    {
      "id": "AQ.20GkAbhpHlvGlF14hfu0", 
      "metadata": {
        "id": "AQ.20GkAbhpHlvGlF14hfu0", 
        "username": "vv00011"
      }, 
      "username": "vv00011"
    }, 
    {
      "id": "AUDlKFqriwVCi7YTOW3WVx8", 
      "metadata": {
        "id": "AUDlKFqriwVCi7YTOW3WVx8", 
        "username": "vv00044"
      }, 
      "username": "vv00044"
    }, 
    {
      "id": "ATKT9mphEmdKsUpNO5MvPDw", 
      "metadata": {
        "id": "ATKT9mphEmdKsUpNO5MvPDw", 
        "username": "vv00024"
      }, 
      "username": "vv00024"
    }, 
    {
      "id": "AQ5XYHz8J1JPiFtlEGw2xD8", 
      "metadata": {
        "id": "AQ5XYHz8J1JPiFtlEGw2xD8", 
        "username": "vv00040"
      }, 
      "username": "vv00040"
    }, 
    {
      "id": "AVrOh3dmOJNGpTPTPT47Qsk", 
      "metadata": {
        "id": "AVrOh3dmOJNGpTPTPT47Qsk", 
        "username": "vv00039"
      }, 
      "username": "vv00039"
    }, 
    {
      "id": "AeJHkOokf55AkhVrhLuHBzE", 
      "metadata": {
        "id": "AeJHkOokf55AkhVrhLuHBzE", 
        "username": "vv00015"
      }, 
      "username": "vv00015"
    }, 
    {
      "id": "AYDtXiZHtupGjoxNHfaHlHo", 
      "metadata": {
        "id": "AYDtXiZHtupGjoxNHfaHlHo", 
        "username": "vv00038"
      }, 
      "username": "vv00038"
    }, 
    {
      "id": "ARJ4U8ZCwh5NpJK5h5G2kDQ", 
      "metadata": {
        "id": "ARJ4U8ZCwh5NpJK5h5G2kDQ", 
        "username": "vv00042"
      }, 
      "username": "vv00042"
    }, 
    {
      "id": "AXOpQz2i.x5AhvPhvQGGCzs", 
      "metadata": {
        "id": "AXOpQz2i.x5AhvPhvQGGCzs", 
        "username": "vv00028"
      }, 
      "username": "vv00028"
    }, 
    {
      "id": "AQJ3jRoptElBgAuHZtNU4Pg", 
      "metadata": {
        "id": "AQJ3jRoptElBgAuHZtNU4Pg", 
        "username": "vv00013"
      }, 
      "username": "vv00013"
    }, 
    {
      "id": "AfqyaQW.bzlJhLSi6YNZOCA", 
      "metadata": {
        "id": "AfqyaQW.bzlJhLSi6YNZOCA", 
        "username": "vv00033"
      }, 
      "username": "vv00033"
    }, 
    {
      "id": "AajN2Bq1vq5HssRu0oehu2w", 
      "metadata": {
        "id": "AajN2Bq1vq5HssRu0oehu2w", 
        "username": "vv00004"
      }, 
      "username": "vv00004"
    }, 
    {
      "id": "AdVUkDSVU8xNpNsqF0pUYVo", 
      "metadata": {
        "id": "AdVUkDSVU8xNpNsqF0pUYVo", 
        "username": "vv00043"
      }, 
      "username": "vv00043"
    }, 
    {
      "id": "AU4.8jlWikxMqw4Y2wW7CtQ", 
      "metadata": {
        "id": "AU4.8jlWikxMqw4Y2wW7CtQ", 
        "username": "vv00003"
      }, 
      "username": "vv00003"
    }, 
    {
      "id": "AVWAqUOTXKNGgGwizdlfICA", 
      "metadata": {
        "id": "AVWAqUOTXKNGgGwizdlfICA", 
        "username": "vv00016"
      }, 
      "username": "vv00016"
    }, 
    {
      "id": "AROza.ZAlwNKibQqFxp4tmw", 
      "metadata": {
        "id": "AROza.ZAlwNKibQqFxp4tmw", 
        "username": "vv00023"
      }, 
      "username": "vv00023"
    }, 
    {
      "id": "AfJu72trdg1BvkRrJcMMD6s", 
      "metadata": {
        "id": "AfJu72trdg1BvkRrJcMMD6s", 
        "username": "vv00049"
      }, 
      "username": "vv00049"
    }, 
    {
      "id": "ARJzzcZ1LUpMmNKePTCl.zE", 
      "metadata": {
        "id": "ARJzzcZ1LUpMmNKePTCl.zE", 
        "username": "vv00050"
      }, 
      "username": "vv00050"
    }, 
    {
      "id": "AcPQYoeKEi5Bvpgu_XkuRfY", 
      "metadata": {
        "id": "AcPQYoeKEi5Bvpgu_XkuRfY", 
        "username": "vv00030"
      }, 
      "username": "vv00030"
    }, 
    {
      "id": "AdFuJuj9475JuxrWWTTF38U", 
      "metadata": {
        "id": "AdFuJuj9475JuxrWWTTF38U", 
        "username": "vv00041"
      }, 
      "username": "vv00041"
    }, 
    {
      "id": "AeOh_2KRYihPmX5Bpv43ogE", 
      "metadata": {
        "id": "AeOh_2KRYihPmX5Bpv43ogE", 
        "username": "vv00045"
      }, 
      "username": "vv00045"
    }, 
    {
      "id": "AagbpxC8JypOu.OB4era.4w", 
      "metadata": {
        "id": "AagbpxC8JypOu.OB4era.4w", 
        "username": "vv00025"
      }, 
      "username": "vv00025"
    }, 
    {
      "id": "AcvVhcwSXgtBvATuGsnhWwM", 
      "metadata": {
        "id": "AcvVhcwSXgtBvATuGsnhWwM", 
        "username": "vv00014"
      }, 
      "username": "vv00014"
    }, 
    {
      "id": "AdLTcQowV0RAvGG_5hrZ4iw", 
      "metadata": {
        "id": "AdLTcQowV0RAvGG_5hrZ4iw", 
        "username": "vv00029"
      }, 
      "username": "vv00029"
    }, 
    {
      "id": "AUGMfc1q3YFIvsYHMS.WAOo", 
      "metadata": {
        "id": "AUGMfc1q3YFIvsYHMS.WAOo", 
        "username": "Gopal"
      }, 
      "username": "Gopal"
    }, 
    {
      "id": "AeEcrVVCCXJKlkFqLPOblYY", 
      "metadata": {
        "id": "AeEcrVVCCXJKlkFqLPOblYY", 
        "username": "VBI10258"
      }, 
      "username": "VBI10258"
    }, 
    {
      "id": "AcqTAzHRrIJKuvJNxIbEk7Q", 
      "metadata": {
        "id": "AcqTAzHRrIJKuvJNxIbEk7Q", 
        "username": "AnandJ"
      }, 
      "username": "AnandJ"
    }, 
    {
      "id": "ATXb3J3RcpdOqKkgzJ9Ta4o", 
      "metadata": {
        "id": "ATXb3J3RcpdOqKkgzJ9Ta4o", 
        "username": "AishwaryaR"
      }, 
      "username": "AishwaryaR"
    }, 
    {
      "id": "Adl8rCU7shpJhOQPfH6i8Mg", 
      "metadata": {
        "id": "Adl8rCU7shpJhOQPfH6i8Mg", 
        "username": "ssrskab@bir1({srs})"
      }, 
      "username": "ssrskab@bir1({srs})"
    }, 
    {
      "id": "ASUlS34sL_5HoeM6gRol5v4", 
      "metadata": {
        "id": "ASUlS34sL_5HoeM6gRol5v4", 
        "username": "SRV06"
      }, 
      "username": "SRV06"
    }, 
    {
      "id": "AT2m6PpBdf5DmuwIafoD55w", 
      "metadata": {
        "id": "AT2m6PpBdf5DmuwIafoD55w", 
        "username": "vbiviewdemo"
      }, 
      "username": "vbiviewdemo"
    }, 
    {
      "id": "AcIUV2UzqsZMkrn64mkVff0", 
      "metadata": {
        "id": "AcIUV2UzqsZMkrn64mkVff0", 
        "username": "srvadm"
      }, 
      "username": "srvadm"
    }, 
    {
      "id": "AcCS4KjV60JAp8.qdSGDRa0", 
      "metadata": {
        "id": "AcCS4KjV60JAp8.qdSGDRa0", 
        "username": "fullerg"
      }, 
      "username": "fullerg"
    }, 
    {
      "id": "ATIqzhsnj9NFi3BkweLX0KE", 
      "metadata": {
        "id": "ATIqzhsnj9NFi3BkweLX0KE", 
        "username": "bobjadm"
      }, 
      "username": "bobjadm"
    }, 
    {
      "id": "AalkmLppcM1PnGyFBEHihS4", 
      "metadata": {
        "id": "AalkmLppcM1PnGyFBEHihS4", 
        "username": "SRV09"
      }, 
      "username": "SRV09"
    }, 
    {
      "id": "AfJZvpd3liRCh8NwbMfNLwQ", 
      "metadata": {
        "id": "AfJZvpd3liRCh8NwbMfNLwQ", 
        "username": "SRV10"
      }, 
      "username": "SRV10"
    }, 
    {
      "id": "AY98tNkAgTdGm54KzbwJi_A", 
      "metadata": {
        "id": "AY98tNkAgTdGm54KzbwJi_A", 
        "username": "SRV08"
      }, 
      "username": "SRV08"
    }, 
    {
      "id": "Af2i_I1ruLlEj.3QbyO_9QA", 
      "metadata": {
        "id": "Af2i_I1ruLlEj.3QbyO_9QA", 
        "username": "SRV03"
      }, 
      "username": "SRV03"
    }, 
    {
      "id": "ASDaRwtpZ.VKuNYwoExSkLI", 
      "metadata": {
        "id": "ASDaRwtpZ.VKuNYwoExSkLI", 
        "username": "SRV02"
      }, 
      "username": "SRV02"
    }, 
    {
      "id": "AW2ea0JHvcBJqxIdMbNRtoA", 
      "metadata": {
        "id": "AW2ea0JHvcBJqxIdMbNRtoA", 
        "username": "biadm"
      }, 
      "username": "biadm"
    }, 
    {
      "id": "AcOCGfunNNtImhhFMHJSp9c", 
      "metadata": {
        "id": "AcOCGfunNNtImhhFMHJSp9c", 
        "username": "mtdemo"
      }, 
      "username": "mtdemo"
    }, 
    {
      "id": "AXhRsTJ91pBKkQi1KOaLPUI", 
      "metadata": {
        "id": "AXhRsTJ91pBKkQi1KOaLPUI", 
        "username": "SRV04"
      }, 
      "username": "SRV04"
    }, 
    {
      "id": "AcxXzxJ0IAZBsbocb_VJ3p0", 
      "metadata": {
        "id": "AcxXzxJ0IAZBsbocb_VJ3p0", 
        "username": "SRV07"
      }, 
      "username": "SRV07"
    }, 
    {
      "id": "Ac_gVqbvOWdFsr.vy_GshAQ", 
      "metadata": {
        "id": "Ac_gVqbvOWdFsr.vy_GshAQ", 
        "username": "SRV05"
      }, 
      "username": "SRV05"
    }, 
    {
      "id": "AV4hSOuKWalGi2c.8eW39FY", 
      "metadata": {
        "id": "AV4hSOuKWalGi2c.8eW39FY", 
        "username": "SRV01"
      }, 
      "username": "SRV01"
    }, 
    {
      "id": "AaVi6KcBxyNCiCGkgttW4lY", 
      "metadata": {
        "id": "AaVi6KcBxyNCiCGkgttW4lY", 
        "username": "gfuller"
      }, 
      "username": "gfuller"
    }, 
    {
      "id": "AddW1iZNDF9LsyhgQJmqJAg", 
      "metadata": {
        "id": "AddW1iZNDF9LsyhgQJmqJAg", 
        "username": "adrian"
      }, 
      "username": "adrian"
    }, 
    {
      "id": "AYg8wRzSdVRNjlsLqPb3VGI", 
      "metadata": {
        "id": "AYg8wRzSdVRNjlsLqPb3VGI", 
        "username": "george"
      }, 
      "username": "george"
    }, 
    {
      "id": "AdtZFN7XZTlMqwtB2CFAxAA", 
      "metadata": {
        "id": "AdtZFN7XZTlMqwtB2CFAxAA", 
        "username": "cook"
      }, 
      "username": "cook"
    }, 
    {
      "id": "AYkjABN1wsVJsBsu4HkI9Hw", 
      "metadata": {
        "id": "AYkjABN1wsVJsBsu4HkI9Hw", 
        "username": "adam"
      }, 
      "username": "adam"
    }, 
    {
      "id": "Ab5goKfpHnVHi51vMMsYeM8", 
      "metadata": {
        "id": "Ab5goKfpHnVHi51vMMsYeM8", 
        "username": "harvey"
      }, 
      "username": "harvey"
    }, 
    {
      "id": "AZXxgvnSAIFNpj9oy1vbgRA", 
      "metadata": {
        "id": "AZXxgvnSAIFNpj9oy1vbgRA", 
        "username": "QaaWSServletPrincipal"
      }, 
      "username": "QaaWSServletPrincipal"
    }, 
    {
      "id": "AYOND92OTmRDiSOfmHNmLy4", 
      "metadata": {
        "id": "AYOND92OTmRDiSOfmHNmLy4", 
        "username": "SMAdmin"
      }, 
      "username": "SMAdmin"
    }, 
    {
      "id": "AfRWaT5_131NlLLf5bRMLKY", 
      "metadata": {
        "id": "AfRWaT5_131NlLLf5bRMLKY", 
        "username": "Administrator"
      }, 
      "username": "Administrator"
    }, 
    {
      "id": "AcgOFGfhCzJEg.VjnPaidmI", 
      "metadata": {
        "id": "AcgOFGfhCzJEg.VjnPaidmI", 
        "username": "Guest"
      }, 
      "username": "Guest"
    }
  ]
}
''')
user_rep=[
  {"user_id": "18FC2D0B4368CB9A93C9C6A7AF6BA270", "username": "SRV03"},
  {"user_id": "3BE945444189ED29F0646387D3793495", "username": "srvadm"},
  {"user_id": "54F3D26011D2896560009A8E67019608", "username": "Administrator"},
  {"user_id": "4E70890241DBB18E6CA1D8B850952A68", "username": "BusinessUser"}
]
def get_user_meta(leng):
  return user_rep
  meta = []
#  for user in user_rep.get("users_list")[:leng]:
  for user in user_rep:
    meta.append(user)
  return meta