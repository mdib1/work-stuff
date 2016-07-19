

def AssociateLineItem(client,line_items, creative_ids):
      lica_sizes = [{'width': '300','height': '250'},{'width': '300','height': '600'},{'width': '728','height': '90'},{'width': '160','height': '600'},{'width': '970','height': '250'}]
      lica_service = client.GetService('LineItemCreativeAssociationService', version='v201508')
      for line_item in line_items:
            licas = []
            for creative_id in creative_ids:
                  licas.append({'creativeId': creative_id,'sizes' : lica_sizes, 'lineItemId': line_item})
            if (len(licas) > 0):
                  licas = lica_service.createLineItemCreativeAssociations(licas)


# creative ids from the Prebid-ZDT (I think)
AssociateLineItem(dfp_client, line_items, ['52234991972','52234992092','52234992212','52234992332','52234992452','52234938452'])