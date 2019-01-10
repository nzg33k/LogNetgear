Netgear's tracking is pretty basic.  It will tell you how much data has been downloaded/uploaded but only on a per day/week/month basis.

This script checks the router via its api every minute to get the today figures and figure out the difference.

These are then kept in log files and uploaded to a google sheet - which you can use to create a chart.
