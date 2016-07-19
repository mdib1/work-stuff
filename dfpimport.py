from googleads import dfp
import sys
import csv
import logging
import random


logging.getLogger('suds.client').setLevel(logging.CRITICAL)

def main(client):
  global mycache
  mycache={}
  global debug
  global createdadunits
  createdadunits = 0

  #debug = True
  debug = False

  gothrucsvanddothings(str(sys.argv[1]),parseadunitimport, client)
  #displayresults(mycache)
  print str(createdadunits)+" ad units have been created"

def displayresults(mycache):
  for key in mycache:
    print key

def parseadunitimport(client,lineitemimportcsvrow):
  
  client.network_code = lineitemimportcsvrow[0]
  inventory_service = client.GetService('InventoryService', version='v201605')
  adunitnames = getadunitnames(lineitemimportcsvrow)
  labels = []
  adunitlevel = 0
  network_service = client.GetService('NetworkService', version='v201605')
  rootID = network_service.getCurrentNetwork()['effectiveRootAdUnitId']  
  adunittree = str(rootID)
  if lineitemimportcsvrow[6]=="":
    print 'sizes missing skipping entire row'
    return
  for adunitname in adunitnames:
    #update adunit tree for use as local cache key
    parenttree=adunittree
    adunittree+=">"+adunitname
    #parse imported csv row for user entered data
    print "Parsing "+adunittree    
    fixedsizes=parseadunitsizes(lineitemimportcsvrow[6])
    labels=getlabels(lineitemimportcsvrow[7])
    adunitlevel=adunitlevel+1
    #prepare the ad unit
    tempadunit=fetchadunit(adunittree,adunitlevel,adunitname,rootID,inventory_service,parenttree,fixedsizes,labels)
    #now update the ad unit
    tempadunit = correctsizes(tempadunit,fixedsizes,inventory_service,adunittree)
    tempadunit = checklabels(tempadunit,labels,inventory_service)
    #updating done, recache
    mycache[adunittree]=tempadunit      
    if debug:
      print "caching "+adunittree    
    print ""      


def checklabels(tempadunit,neededlabels,inventory_service):
  if debug:
    print "neededlabels: "+str(neededlabels)
  if len(neededlabels)>0:
    if debug:
      print "checking if all requested labels are present"
    if type(tempadunit) is dict:
      if debug:
        tempadunit=addlabelstofakeadunit(tempadunit,neededlabels,inventory_service)
    else:
      tempadunit=addlabels(tempadunit,neededlabels,inventory_service)
  else:
    if debug:
      print "no need to add labels"
  return tempadunit

def addlabelstofakeadunit(tempadunit,neededlabels,inventory_service):
  if 'appliedLabels' in tempadunit.keys():
    for label in tempadunit['appliedLabels']:
      if label['labelId'] in neededlabels:
        neededlabels.remove(label['labelId'])
    if len(neededlabels)>0:
      tempadunit = addmissinglabels(tempadunit,neededlabels,inventory_service)
      return tempadunit
    else:
      print "all labels accounted for"
      return tempadunit    
  else:
    print "didnt have the key, didnt add somehow. investigate"  
    pass
    return tempadunit

def addlabels(tempadunit,neededlabels,inventory_service):
  if hasattr(tempadunit,'appliedLabels'):    
    for label in tempadunit['appliedLabels']:
      if label['labelId'] in neededlabels:
        if debug:
          print "found "+str(label['labelId'])
        neededlabels.remove(label['labelId'])
    if len(neededlabels)>0:
      tempadunit = addmissinglabels(tempadunit,neededlabels,inventory_service)
      return tempadunit
    else:
      if debug:
        print "all labels accounted for"
      return tempadunit
  else:
    if debug:
      print "Had no labels, adding all of em."
    labelarray=[]
    for label in neededlabels:
      labelarray.append({'labelId':label})        
    #setattr(tempadunit,'appliedLabels',labelarray) 
    tempadunit['appliedLabels']=labelarray
    tempadunit = addmissinglabels(tempadunit,neededlabels,inventory_service)    
    return tempadunit

def addmissinglabels(tempadunit,neededlabels,inventory_service):
  newstr=""
  for label in neededlabels:
    newlist={}
    newlist['labelId']=label
    newlist['isNegated']=False
    tempadunit['appliedLabels'].append(newlist)
    newstr+=str(label)+" "  
  if debug:
    print "added missing labels: "+newstr
    return tempadunit
  else:
    updated_ad_units = []
    updated_ad_units.append(tempadunit)
    ad_units = inventory_service.updateAdUnits(updated_ad_units)
    # Display results.
    for ad_unit in ad_units:
      ad_unit_labels = ['%s' % (label['labelId'])
                       for label in ad_unit['appliedLabels']]
      print ('Ad unit with ID \'%s\', name \'%s\', and labels [%s] was updated'
             % (ad_unit['id'], ad_unit['name'], ','.join(ad_unit_labels)))  
      return ad_unit    

def getlabels(cell):
  strlabels=cell.split(',')
  longlabels=[]
  for strg in strlabels:
    if strg == '':
      if debug:
        print "no labels requested"
      return longlabels
    else:
      longlabels.append(long(strg))
  return longlabels

def correctsizes(tempadunit,fixedsizes,inventory_service,adunittree):
  global mycache
  missingsizes = checkingsizes(tempadunit,fixedsizes)   
  for missingsize in missingsizes:
    tempadunit = addmissingsize(inventory_service, missingsize,tempadunit)
  mycache[adunittree]=tempadunit
  return tempadunit      

def addmissingsize(inventory_service, missingsize,tempadunit):
  fixednewsize = parseadunitsizes(missingsize)[0]
  print "adding additional size: "+missingsize
  if debug:
    print "debug mode, fake adding size"
    if hasattr(tempadunit,'adUnitSizes'):
      tempadunit['adUnitSizes'].append(fixednewsize)
      return tempadunit    
    else:
      newarr=[]
      newarr.append(fixednewsize)
      setattr(tempadunit,'adUnitSizes',newarr)
      return tempadunit       
  else:
    values = [{
        'key': 'id',
        'value': {
            'xsi_type': 'TextValue',
            'value': tempadunit['id']
        }
    }]
    query = 'WHERE id = :id'
    statement = dfp.FilterStatement(query, values)

    # Get ad units by statement.
    response = inventory_service.getAdUnitsByStatement(
        statement.ToStatement())

    if 'results' in response:
      updated_ad_units = []
      for ad_unit in response['results']:
        if 'adUnitSizes' not in ad_unit:
          ad_unit['adUnitSizes'] = []
        ad_unit['adUnitSizes'].append(fixednewsize)
        updated_ad_units.append(ad_unit)

      # Update ad unit on the server.
      ad_units = inventory_service.updateAdUnits(updated_ad_units)

      # Display results.
      for ad_unit in ad_units:
        ad_unit_sizes = ['{%s x %s}' % (size['size']['width'],
                                        size['size']['height'])
                         for size in ad_unit['adUnitSizes']]
        print ('Ad unit with ID \'%s\', name \'%s\', and sizes [%s] was updated'
               % (ad_unit['id'], ad_unit['name'], ','.join(ad_unit_sizes)))  
        return ad_unit

def checkingsizes(tempadunit,fixedsizes):
  if debug:
    print "checking if it has the requested sizes"
  neededsizearray=[]
  for fixedsize in fixedsizes:
    neededsizearray.append( str(fixedsize['size']['width'])+"x"+str(fixedsize['size']['height']) )
  try:
    for adunitsize in tempadunit['adUnitSizes']:
      currentsize = str(adunitsize['size']['width'])+"x"+str(adunitsize['size']['height'])
      if currentsize in neededsizearray:
        neededsizearray.remove(currentsize)
  except:
    pass
  if debug:
    if len(neededsizearray)!=0:
      print "need to add these sizes: "+str(neededsizearray)
    else:
      if debug:
        print "all sizes accounted for"
  return neededsizearray

def parseadunitsizes(sizes):
  sizearray=[]
  sizepairs=sizes.split(',')
  for mysize in sizepairs:
    newsizepair={}
    newthing={}
    singlepair=mysize.split('x')
    newsizepair['width']=singlepair[0]
    newsizepair['height']=singlepair[1]
    newthing['size']=newsizepair
    sizearray.append(newthing)
  return sizearray

def makeanadunit(inventory_service, adunitname, parentID, sizes,labels):
  # modify below to take CSV row as input
  global createdadunits
  global debug  
  labelarray=[]
  for label in labels:
    labelarray.append({'labelId':label})
  
  # Create ad unit objects.
  ad_unit = {
      'name': adunitname,
      'adUnitCode': adunitname,
      'parentId': parentID,
      'adUnitSizes': sizes,
      'appliedLabels': labelarray
  }

  if debug==False:
    ad_units = inventory_service.createAdUnits([ad_unit])

    # Display results.
    for ad_unit in ad_units:
      print ('Ad unit with ID \'%s\' and name \'%s\' and code \'%s\' and was created.'
             % (ad_unit['id'], ad_unit['name'], ad_unit['adUnitCode']))     
      createdadunits+=1
      return ad_unit
  else:
    randomid = random.randint(12093781, 120937812)
    debugmsg = "Debug mode enabled, generating fake ad unit with ID: "+str(randomid)
    print debugmsg
    ad_unit['id']=randomid
    ad_unit['parentPath']=[]
    newlist={}
    newlist['id']=parentID
    ad_unit['parentPath'].append(newlist)
    createdadunits+=1
    return ad_unit

def getadunitnames(lineitemimportcsvrow):
  adunitnames=[]
  invalidrow=False
  foundemptycell=False
  for cell in range(1,6):
    if lineitemimportcsvrow[cell]=="":
      foundemptycell=True
    else:
      if foundemptycell:
        print "warning: missing ad unit name in column for ad unit "+str(cell-1)+" skipping the entire row"
        invalidrow=True
        break
      else:
        adunitnames.append(lineitemimportcsvrow[cell]) 
  if invalidrow:
    return []
  else:
    return adunitnames

def dothingstorow(row, client,thingtodo):
  thingtodo(client, row)

def gothrucsvanddothings(file, thingstodo, client):
  ifile  = open(file, "rb")
  reader = csv.reader(ifile)
  inum=1
  for row in reader:
    if row[0]=="network":
      print "skipping header row"
      pass
    else:
      inum=inum+1
      print '***Beginning row '+str(inum)+':'
      dothingstorow(row, client, thingstodo)
  ifile.close()
  
def getadunitwithparent(inventory_service,adunitname,parentID):
  query = ('WHERE name = \'%s\'' % (adunitname))
  statement = dfp.FilterStatement(query)

  # Get ad units by statement.
  while True:
    response = inventory_service.getAdUnitsByStatement(
        statement.ToStatement())
    if 'results' in response:
      # Display results.
      for ad_unit in response['results']:
        if debug:
          print "checking if parent: "+str(ad_unit['parentPath'][-1]['id'])+" is expected parent: "+str(parentID)
        if ad_unit['parentPath'][-1]['id']==parentID:
          if debug:
            print "found a match and returning"
          return ad_unit
        else:
          if debug:
            print "not a match, next"
          pass
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      if debug:
        print "no matches"
      break 

def fetchadunit(adunittree,adunitlevel,adunitname,rootID,inventory_service,parenttree,fixedsizes,labels):
  if adunittree not in mycache: 
    #get ad unit from DFP
    if debug:
      print adunitname+" not cached yet, looking in DFP"
    if adunitlevel>1:
      parentID = mycache[parenttree]['id'] 
    else:
      parentID = rootID      
    tempadunit = (getadunitwithparent(inventory_service,adunitname,parentID))
    if tempadunit == None:
      #ad unit doesn't exist
      if debug:
        print adunitname+' not found, need to create'
      tempadunit = makeanadunit(inventory_service,adunitname,parentID,fixedsizes,labels) 
    else:
      #received ad unit from DFP
      pass
  else:
    #Get ad unit from local cache
    if debug:
      print "retrieving "+adunittree+" from cache"
    tempadunit = mycache[adunittree] 
  return tempadunit      

if __name__ == '__main__':
  # Initialize client object.
  yaml_path = r"C:\Users\OAO_NY_03-24-2016\Desktop\work\api\googleads.yaml"
  dfp_client = dfp.DfpClient.LoadFromStorage(path=yaml_path)
  
  main(dfp_client)    


