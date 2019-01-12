import password, time, sys

def getlogdata(password=""):
    from pynetgear import Netgear
    import datetime

    # Instantiate the netgear api connection
    netgear = Netgear(password=password)

    # Open the log files - create if needed
    uploadlog = open("netgear_upload.log","a+")
    downloadlog = open("netgear_download.log","a+")

    # Look for the previous value from the file, if there isn't one then set it to zero
    uploadprev = uploadlog.readlines()
    if len(uploadprev) > 0:
        uploadprev = uploadprev[-1].split(",")[0]
    else:
        uploadprev = 0
    downloadprev = downloadlog.readlines()
    if len(downloadprev) > 0:
        downloadprev = downloadprev[-1].split(",")[0]
    else:
        downloadprev = 0

    # The previous value from the file will be a string, we need a float to do math with
    uploadprev = float(uploadprev)
    downloadprev = float(downloadprev)

    # Get the traffic meter data via the api
    traffic = netgear.get_traffic_meter()
    upload = traffic.get("NewTodayUpload")
    download = traffic.get("NewTodayDownload")

    # If the previous value is less than the current value, subtract it.  Otherwise it is either
    # - a new log run so don't subtract or
    # - it is a new day, so we will use yesterdays total to figure it out
    if upload >= uploadprev:
        uploadvalue = upload - uploadprev
    else:
        if uploadprev == 0:
            uploadvalue = upload
        else:
            uploadvalue = upload
            #The router doesn't log yesterday right, it seems to be less than prev
            #uploadvalue = (traffic.get("NewYesterdayUpload") - uploadprev) + upload
    if download >= downloadprev:
        downloadvalue = download - downloadprev
    else:
        if downloadprev == 0:
            downloadvalue = upload
        else:
            downloadvalue = upload
            #The router doesn't log yesterday right, it seems to be less than prev
            #downloadvalue = (traffic.get("NewYesterdayDownload") - uploadprev) + upload

    # Get the time and add the lines to the log files
    now = datetime.datetime.now()
    uploadlog.writelines("%f,%s,%f\n" % (upload, now, uploadvalue))
    downloadlog.writelines("%f,%s,%f\n" % (download, now, downloadvalue))

    # Close the log files
    uploadlog.close()
    downloadlog.close()

    #send the data to the google sheet for graphing
    output_to_gsheet([[str(now),downloadvalue,uploadvalue]])

# Output to a google sheet defined in password.py eg
# {"id": "sheetid goes here", "range": "data!A:C"}
def output_to_gsheet(data):
    """Output data to a google sheet"""
    # https://developers.google.com/sheets/api/quickstart/python
    from googleapiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file as gfile, client, tools
    # Setup the Sheets API
    store = gfile.Storage('credentials.json')
    try:
        creds = store.get()
    except:
        creds = False
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'client_secret.json',
            'https://www.googleapis.com/auth/spreadsheets'
        )
        creds = tools.run_flow(flow, store)
    try:
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        resource = service.spreadsheets().values()  # pylint: disable=no-member
        # Populate the destination range
        result = resource.append(
            spreadsheetId=password.OUTPUTSHEET['id'],
            range=password.OUTPUTSHEET['range'],
            insertDataOption='INSERT_ROWS',
            valueInputOption="USER_ENTERED",
            body={
                "majorDimension": "ROWS",
                "values": data
            }
        )
        result.execute()
    except:
        googlesuccess = False

def logforever():
    # Log forever, every minute
    while True:
        getlogdata(password.PASSWORD)
        time.sleep(60)

def runonce():
    getlogdata(password.PASSWORD)

def main(arg = ""):
    if arg == 'once':
        runonce()
    elif arg == 'forever':
            logforever()
    else:
        print "options are once or forever"

if __name__ == "__main__":
    main(sys.argv[1])