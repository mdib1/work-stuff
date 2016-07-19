from googleads import dfp
from googleads import oauth2


def AssociateLineItem(client,line_items, creative_ids):
      lica_sizes = [{'width': '300','height': '250'},{'width': '300','height': '600'},{'width': '728','height': '90'},{'width': '160','height': '600'},{'width': '970','height': '250'}]
      lica_service = client.GetService('LineItemCreativeAssociationService', version='v201508')
      for line_item in line_items:
            licas = []
            for creative_id in creative_ids:
                  licas.append({'creativeId': creative_id,'sizes' : lica_sizes, 'lineItemId': line_item})
            if (len(licas) > 0):
                  licas = lica_service.createLineItemCreativeAssociations(licas)



def main(client):
  # Initialize appropriate service.
  line_item_service = client.GetService('LineItemService', version='v201502')

  # Create a filter statement.

  query = 'WHERE orderId =  203997932 AND isArchived = False'


  statement = dfp.FilterStatement(query)
  
  newline_items = []
  

  
  while True:
    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())
    if 'results' in response:
      
      for line_item in response['results']:
        newline_items.append(line_item['id'])

      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
      
    else:
      break
 
  for line_item in newline_items:
    # print line_item
   AssociateLineItem(client, newline_items, ['52234991972','52234992092','52234992212','52234992332','52234992452','52234938452'])
  # print '\nNumber of results found: %s' % response['totalResultSetSize']




if __name__ == '__main__':
	yaml_path = r"C:\Users\mauri\Desktop\work\googleads.yaml"
	dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
	main(dfp_client)

	