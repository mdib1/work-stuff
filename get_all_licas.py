"""This code example gets all line item creative associations (LICA).
To create LICAs, run create_licas.py or associate_creative_set_to_line_item.py.
"""


# Import appropriate modules from the client library.
from googleads import dfp
import csv


def main(client):
  client.network_code=8788  

  

  line_item_service = client.GetService('LineItemService', version='v201605')
  query = "WHERE status IN ('READY', 'DELIVERING') AND OrderId IN (315076474, 315388474, 316457194, 316664794, 324726634, 325561354, 336246154, 339645034, 373422874, 373620634, 374485114, 374610634)"

  statement = dfp.FilterStatement(query)
  ofile  = open('LICAs.csv', "ab")
  writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)  
  while True:
    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())

    if 'results' in response:
      for line_item in response['results']:
        getlicasforlineitem(client,line_item, writer)
      break
    else:
      break
  ofile.close


def getlicasforlineitem(client,line_item, writer):
  print 'fetching lica for '
  print line_item['id']
  print 'line item archived status is '
  print line_item['isArchived']
  # Initialize appropriate service.
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v201605')
  # print 'Connected to LICA service'
  # Create a filter statement.
  values = [{
      'key': 'lineItemId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': line_item['id']
      }
  }]        
  # query = 'WHERE lineItemId = :lineItemId'
  query = "WHERE lineItemId = :lineItemId AND status = 'ACTIVE'"
  statement = dfp.FilterStatement(query, values)
  # Get line items by statement.
  while True:
    print 'fetching LICA'
    response = lica_service.getLineItemCreativeAssociationsByStatement(
        statement.ToStatement())
    if 'results' in response:
      print 'got response'
      # Display results.
      for lica in response['results']:
        row=[]
        print ('LICA with line item ID \'%s\', creative ID \'%s\', and status'
               ' \'%s\' was found.' % (lica['lineItemId'], lica['creativeId'],
                                       lica['status']))
        row.append(line_item['id'])
        row.append(line_item['name'])
        row.append(lica['creativeId'])
        row.append(getcreativename(client,lica['creativeId']))
        row.append(getcreativesize(client,lica['creativeId']))
        writer.writerow(row)
      break
    else:
      break
  print '\nNumber of results found: %s' % response['totalResultSetSize']  


def activelineitem(client,line_item_id):
  line_item_service = client.GetService('LineItemService', version='v201605')
  query = ('WHERE Id = \'%s\'' % (line_item_id))
  statement = dfp.FilterStatement(query)
  while True:
    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())

    if 'results' in response:
      for line_item in response['results']:
        if line_item['isArchived']:
          return False
        else:
          return True
    else:
      return False

def getlineitemname(client,line_item_id):
  line_item_service = client.GetService('LineItemService', version='v201605')
  query = ('WHERE Id = \'%s\'' % (line_item_id))
  statement = dfp.FilterStatement(query)
  while True:
    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())

    if 'results' in response:
      for line_item in response['results']:
        return line_item['name']
    else:
      print 'error! could not find line item by id'
      return False

def getcreativename(client,creative_id):
  creative_service = client.GetService('CreativeService', version='v201605')
  query = ('WHERE Id = \'%s\'' % (creative_id))
  statement = dfp.FilterStatement(query)
  while True:
    response = creative_service.getCreativesByStatement(
        statement.ToStatement())

    if 'results' in response:
      for creative in response['results']:
        return creative['name']
    else:
      print 'error! could not find creative by id'      
      return False

def getcreativesize(client,creative_id):
  creative_service = client.GetService('CreativeService', version='v201605')
  query = ('WHERE Id = \'%s\'' % (creative_id))
  statement = dfp.FilterStatement(query)
  while True:
    response = creative_service.getCreativesByStatement(
        statement.ToStatement())

    if 'results' in response:
      for creative in response['results']:
        newsize = str(creative['size']['width'])+"x"+str(creative['size']['height'])
        return newsize
    else:
      print 'error! could not find creative by id'      
      return False  


if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  main(dfp_client)

