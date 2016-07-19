from googleads import dfp
import tempfile
def main(client, thingtodo, report_job, filter_statement, networks, isall):
  if isall:
    dothingstoallnetworks(client, thingtodo, filter_statement, report_job)
  else:    
    dothingstosomenetworks(client, thingtodo, networks, filter_statement, report_job)
def doareport(client, filter_statement, report_job):
  makeacsvreportpernetwork(client, filter_statement, report_job)    
def getallorders(client):
  # Initialize appropriate service.
  order_service = client.GetService('OrderService', version='v201602')

  # Create a filter statement.
  statement = dfp.FilterStatement()
  # Get orders by statement.
  allorders=[]
  while True:
    response = order_service.getOrdersByStatement(statement.ToStatement())
    if 'results' in response:
      # Display results.
      for order in response['results']:
        allorders.append(order['id'])
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break
  return allorders
def makeacsvreportpernetwork(client, filter_statement, report_job, mydir="/Users/OAO_NY_03-24-2016/Desktop/work/api/reports/"):
    # Initialize a DataDownloader.
    report_downloader = client.GetDataDownloader(version='v201505')

      # Run the report and wait for it to finish.
    report_job_id = report_downloader.WaitForReport(report_job)

   # Change to your preferred export format.

    export_format = 'CSV_DUMP'
    #export_format = 'XLSX'
    #useGzipCompression = False
    filenameprefix = client.network_code+'_'    
    report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False, prefix=filenameprefix, dir=mydir) 

    # Download report data.
    report_downloader.DownloadReportToFile(
        report_job_id, export_format, report_file)

    report_file.close()      
def dothingstoallnetworks(client, thingtodo, filter_statement, report_job):
  networks = client.GetService('NetworkService').getAllNetworks()
  networksarray=[]  
  for network in networks:
    networksarray.append(network['networkCode'])

  dothingstosomenetworks(client, thingtodo, networksarray, filter_statement, report_job)
def dothingstosomenetworks(client, thingtodo, networksarray, filter_statement, report_job):
  for network in networksarray:
    client.network_code=network
    outstr='processing network '+network
    print outstr
    if network=='1049349':
      print 'skipped'
    else:
      thingtodo(client, filter_statement, report_job)
      print 'complete'
if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  
  prospectnetworks=[
    '5936',
    '3824',
    '9729793',
    '27342165',
    '61381659',
    '1006611',
    '4364',
    '4788',
    '6850',
    '4595',
    '9389',
    '9517547',
    '1049349',
    '6178',
    '1066735',
    '1053034',
    '19565616',
    '4624',
    '7287',
    '245328236',
    '8905',
    '5702'
  ]
  
  #networks=prospectnetworks
  networks=['8788']

  #isall=False
  isall=True

  #report_jobs and filter_statement:
  filter_statement = {}  
  samplejob = {
      'reportQuery': {
          'dimensions': ['ORDER_NAME', 'DATE'],
          'dimensionAttributes': ['ORDER_TRAFFICKER', 'ORDER_START_DATE_TIME',
                                  'ORDER_END_DATE_TIME'],
          'statement': filter_statement,
          'columns': ['AD_SERVER_IMPRESSIONS'],                      
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': {'year':2016, 'month':1, 'day': 1},
          'endDate': {'year':2016, 'month':5, 'day': 1}          
      }
  }  
  reachjob = {
      'reportQuery': {
          'dimensions': ['MONTH_AND_YEAR'],
          'statement': filter_statement,
          'columns': ['REACH'],                      
          'dateRangeType': 'LAST_MONTH',      
      }
  }  
  impspermojob = {
      'reportQuery': {
          'dimensions': ['MONTH_AND_YEAR'],
          'statement': filter_statement,
          'columns': ['TOTAL_INVENTORY_LEVEL_IMPRESSIONS'],                      
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': {'year':2015, 'month':5, 'day': 1},
          'endDate': {'year':2016, 'month':4, 'day': 30}          
      }
  } 
  impspermobysizejob = {
      'reportQuery': {
          'dimensions': ['MONTH_AND_YEAR','CREATIVE_SIZE'],
          'statement': filter_statement,
          'columns': ['TOTAL_INVENTORY_LEVEL_IMPRESSIONS'],                      
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': {'year':2015, 'month':6, 'day': 1},
          'endDate': {'year':2016, 'month':5, 'day': 31}          
      }
  }     
  adrequestcustomcriteriajob = {
      'reportQuery': {
          'dimensions': ['AD_REQUEST_CUSTOM_CRITERIA'],
          'statement': filter_statement,
          'columns': ['SELL_THROUGH_AVAILABLE_IMPRESSIONS'],
          'dateRangeType': 'NEXT_90_DAYS'       
      }
  }  
  customcriteriajob = {
      'reportQuery': {
          'dimensions': ['CUSTOM_CRITERIA'],
          'statement': filter_statement,
          'columns': ['AD_SERVER_IMPRESSIONS'],     
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': {'year':2016, 'month':1, 'day': 1},
          'endDate': {'year':2016, 'month':5, 'day': 1}   
      }
  }  
  targetingjob = {
      'reportQuery': {
          'dimensions': ['TARGETING'],
          'statement': filter_statement,
          'columns': ['AD_SERVER_IMPRESSIONS'],                      
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': {'year':2016, 'month':1, 'day': 1},
          'endDate': {'year':2016, 'month':5, 'day': 1}          
      }
  }  
  main(dfp_client, doareport, reachjob, filter_statement, networks, isall)    



