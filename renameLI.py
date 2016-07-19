from googleads import dfp
import sys
import csv

def main(client):
  # network=50536250
  # line_item_id=99934570
  # newname = 'now im renamed'

  gothrucsvanddothings(str(sys.argv[1]),renamealineitem, client)

def printthings(row):
  print row
  for item in row:
    print item

def dothingstorow(row, client,thingtodo):
  thingtodo(client, row)

def gothrucsvanddothings(file, thingstodo, client):
  ifile  = open(file, "rb")
  reader = csv.reader(ifile)
  for row in reader:
    try:
      dothingstorow(row, client, thingstodo)
    except:
      True
  ifile.close()
  
def renamealineitem(client,array):
  network=array[0]
  line_item_id=array[1]
  newname=array[2]
  line_item_service = client.GetService('LineItemService', version='v201605')
  client.network_code=network

  # Create statement object to only select line items that need creatives from a
  # given order.
  values = [{
      'key': 'Id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': line_item_id
      }
  }]
  query = ('WHERE Id = \'%s\'' % (line_item_id))
  #query = ('WHERE Id = :line_item_id')
  statement = dfp.FilterStatement(query)
  #statement = dfp.FilterStatement(query, values)
  while True:
    # Get line items by statement.
    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())

    if 'results' in response:
      # Display results.
      updated_line_items = []
      for line_item in response['results']:
        oldname = line_item['name']
        line_item['name'] = newname
        updated_line_items.append(line_item)
        print ('line item renamed from \'%s\' to \'%s\'.' % (oldname,line_item['name']))
      line_items = line_item_service.updateLineItems(updated_line_items)
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  
  main(dfp_client)    


