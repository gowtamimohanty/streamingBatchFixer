import http.client
import csv
import os
import re

conn = http.client.HTTPSConnection("platform.adobe.io")
payload = ""
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer XXXXXXXXXXXXXXXX",
    "x-api-key": "XXXXXXXXXXXXXXXX",
    "x-gw-ims-org-id": "XXXXXXXXXXXXXXXX@AdobeOrg",
    "x-sandbox-name": "prod",
}


current_directory = os.getcwd()
# open the csv file with batch and path information
inp_csv_file_path = os.path.join(current_directory, "transactionTotalstring_batch_path2.csv")
# Create the full path for the CSV file
out_csv_file_path = os.path.join(current_directory, "failedBatchesData_transactionTotalstring_path2.json")

# Open the inp csv file for reading
with open(inp_csv_file_path,mode ='r') as file:
    # creating dictreader object
    inpcsvfile = csv.DictReader(file)
    #inpcsvfile = csv.reader(file)

    # Open a CSV file for writing
    with open(out_csv_file_path, "w", newline="") as csvfile:
        #outcsvfile = csv.writer(csvfile)

        # Write header to the CSV file
        #outcsvfile.writerow(["FAILED_BATCH_ID", "PATH", "ECID", "xdmEntity"])

        for lines in inpcsvfile:
            url = (
                f"/data/foundation/export/batches/{lines['FAILED_BATCH_ID_STR']}/failed?path={lines['PATH']}"
            )
            conn.request("GET", url, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            start_index = 0
            while start_index != -1:
                # Find the start and end indices of "xdmEntity" in the response
                start_index = data.find('"xdmEntity":', start_index)
                if start_index != -1:
                    xdmstart_index = data.find('"xdmEntity":', start_index)+12
                    end_index = data.find('},"_errors":', start_index)
                    # Extract the "xdmEntity" part
                    xdm_entity_part = data[xdmstart_index:end_index]

                    # Extract the "ECID" part
                    ecidstart_index = 0
                    ecidstart_index = xdm_entity_part.find('"ECID":[{"id":"', ecidstart_index)+15
                    ecidend_index = xdm_entity_part.find('","authenticatedState"', ecidstart_index)
                    ecid_part = xdm_entity_part[ecidstart_index:ecidend_index]

                    # Check for ECID null part
                    xdm_entity_part_withecid = xdm_entity_part.replace('"ECID":null', '"ECID":"'+ecid_part+'"')

                    # Check for transactionTotal null part
                    xdm_entity_part_withecid_withTT = xdm_entity_part_withecid.replace('"transactionTotal":null', '"transactionTotal":0')
                    
                    # Check for transactionTotal not-null part
                    xdm_entity_part_withecid_withTT0 = re.sub('"transactionTotal":"([0-9.]+)"', '"transactionTotal":0', xdm_entity_part_withecid_withTT)

                    # Write batch_id, path, and xdmEntity to the CSV file
                    #outcsvfile.writerow([lines['FAILED_BATCH_ID'], lines['PATH'], ecid_part, xdm_entity_part_withecid_withTT0])
                    csvfile.write(xdm_entity_part_withecid_withTT0+','+'\n')
                    start_index = end_index

print(f"CSV file '{out_csv_file_path}' created successfully.")
