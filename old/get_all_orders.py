#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example gets all orders.
To create orders, run create_orders.py.
"""


# Import appropriate modules from the client library.
from googleads import dfp

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

def main(client):
  # Initialize appropriate service.
  networks = client.GetService('NetworkService').getAllNetworks()
    for network in networks
      print network
  allorders=[]
  allorders=getallorders(client)

  with open('api_log.txt', 'w') as f:
    order_service = client.GetService('OrderService', version='v201602')

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
          f.write(outputstring)        
        statement.offset += dfp.SUGGESTED_PAGE_LIMIT
      else:
        break
    totalresstatement='\nNumber of results found: %s' % response['totalResultSetSize']
    print totalresstatement
    f.write(totalresstatement)
  f.close

if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  main(dfp_client)