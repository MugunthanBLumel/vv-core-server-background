import json
import random


def get_reports(agent_instance_user_id_list=[1], bi_report_count=20):
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

    for agent_instance_user_id in agent_instance_user_id_list:
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

            if not (False and report_id == 1):
                report_list.append(report_copy)
        result.append((agent_instance_user_id, report_list))

    return result
