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

    # If the previous value is less than the current value, subtract it
    # Otherwise it is probably either a new log run so don't subtract or
    # It is a new day, for now we will just not subtract
    if upload >= uploadprev:
        uploadvalue = upload - uploadprev
    else:
        uploadvalue = upload
    if download >= downloadprev:
        downloadvalue = download - downloadprev
    else:
        downloadvalue = download

    # Get the time and add the lines to the log files
    now = datetime.datetime.now()
    uploadlog.writelines("%f,%s,%f\n" % (upload, now, uploadvalue))
    downloadlog.writelines("%f,%s,%f\n" % (download, now, downloadvalue))

    # Close the log files
    uploadlog.close()
    downloadlog.close()

# Log forever, every minute
import password, time
while True:
    getlogdata(password.PASSWORD)
    time.sleep(60)
