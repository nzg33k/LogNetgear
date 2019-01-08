def getlogdata(password=""):
    from pynetgear import Netgear
    import datetime

    netgear = Netgear(password=password)

    uploadlog = open("netgear_upload.log","a+")
    downloadlog = open("netgear_download.log","a+")

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


    uploadprev = float(uploadprev)
    downloadprev = float(downloadprev)

    traffic = netgear.get_traffic_meter()
    upload = traffic.get("NewTodayUpload")
    download = traffic.get("NewTodayDownload")

    if upload >= uploadprev:
        uploadvalue = upload - uploadprev
    else:
        uploadvalue = upload

    if download >= downloadprev:
        downloadvalue = download - downloadprev
    else:
        downloadvalue = download

    now = datetime.datetime.now()
    uploadlog.writelines("%f,%s,%f\n" % (upload, now, uploadvalue))
    downloadlog.writelines("%f,%s,%f\n" % (download, now, downloadvalue))

    uploadlog.close()
    downloadlog.close()

import password, time
while True:
    getlogdata(password.PASSWORD)
    time.sleep(60)
