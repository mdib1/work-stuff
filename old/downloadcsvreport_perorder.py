
# Import appropriate modules from the client library.
from googleads import dfp
import tempfile



def main(client):
  # networks = dfp_client.GetService('NetworkService').getAllNetworks()
  # for network in networks:
  #   print (network['networkCode'])

    # Initialize appropriate service.
    # Create statement object to filter for an order.


    # networks = client.GetService('NetworkService').getAllNetworks()
    # for network in networks:
    #   client.network_code=network['networkCode']    
    client.network_code=8788
#    order_id = 264021634
    allorders=[]
    allorders=getallorders(client)
    
    for order_id in allorders:
      values = [{
          'key': 'id',
          'value': {
              'xsi_type': 'NumberValue',
              'value': order_id
          }
      }]
      filter_statement = {'query': 'WHERE ORDER_ID = :id',
                          'values': values}

      # Create report job.
      report_job = {
          'reportQuery': {
              'dimensions': ['ORDER_ID', 'ORDER_NAME'],
              'dimensionAttributes': ['ORDER_TRAFFICKER', 'ORDER_START_DATE_TIME',
                                      'ORDER_END_DATE_TIME'],
              'statement': filter_statement,
              'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                          'AD_SERVER_CTR', 'AD_SERVER_CPM_AND_CPC_REVENUE',
                          'AD_SERVER_WITHOUT_CPD_AVERAGE_ECPM'],
              'dateRangeType': 'LAST_MONTH'
          }
      }
      makeacsvreport(client,filter_statement, report_job)    

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

def makeacsvreport(client, filter_statement, report_job, mydir="/Users/OAO_NY_03-24-2016/Desktop/work/api/reports/"):
    # Initialize a DataDownloader.
    report_downloader = client.GetDataDownloader(version='v201505')

      # Run the report and wait for it to finish.
    report_job_id = report_downloader.WaitForReport(report_job)

   # Change to your preferred export format.

    export_format = 'CSV_DUMP'
    #export_format = 'XLSX'
    #useGzipCompression = False
    report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False, dir=mydir) 

    # Download report data.
    report_downloader.DownloadReportToFile(
        report_job_id, export_format, report_file)

    report_file.close()      
  

if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  main(dfp_client)
