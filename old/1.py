
# Import appropriate modules from the client library.
from googleads import dfp
import tempfile



def main(client):
  networks = client.GetService('NetworkService').getAllNetworks()
  with open('api_log.txt', 'w') as f:
    for network in networks:
      client.network_code=network['networkCode']
      order_service = client.GetService('OrderService', version='v201602')
      getorders(order_service,f)
  f.close
    
def getorders(order_service, outputfile):
  #gets all orders from orderservice and outputs to outputfile
  # Create a filter statement.
  statement = dfp.FilterStatement()

  # Get orders by statement.
  while True:
    response = order_service.getOrdersByStatement(statement.ToStatement())
    if 'results' in response:
      # Display results.
      for order in response['results']:
        outputstring=('Order with id \'%s\', name \'%s\', and advertiser id \'%s\' was'
               ' found.' % (order['id'], order['name'], order['advertiserId']))
        outputstring=outputstring+'\n'
        print outputstring
        outputfile.write(outputstring)        
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break
  totalresstatement='\nNumber of results found: %s' % response['totalResultSetSize']
  print totalresstatement
  outputfile.write(totalresstatement) 

if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  #dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path,network_code=network)
  main(dfp_client)
