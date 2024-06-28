import http.client
import csv 
import os 

batch_ids = ["01HJ998VSTND2T3K1XXZZ6CZ4F", "01HJ97HW4CHT3DD478VG0M0CE8", "01HJ9384AQNG3RYQSFAV0Q9TQY"]
paths = ["115650.8ea0acd4-779c-43aa-8ace-1bfe1c06dab2.184.ndjson", "115648.c6cdbe0b-ad75-42e8-afd1-a9938512922f.491.ndjson", "115643.49ec1f98-e9dd-4f64-81e0-8c1ebc067018.200.ndjson"]

conn = http.client.HTTPSConnection("platform.adobe.io")
payload = ''
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer your_actual_access_token',
    'x-api-key': 'your_actual_api_key',
    'x-gw-ims-org-id': 'your_actual_ims_org_id',
    'x-sandbox-name': 'jas'
}


current_directory = os.getcwd()
# Create the full path for the CSV file
csv_file_path = os.path.join(current_directory, 'xdm_entities.csv')

# Open a CSV file for writing
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header to the CSV file
    csv_writer.writerow(['Batch ID', 'Path', 'xdmEntity'])

    for batch_id in batch_ids:
        for path in paths:
            url = f"/data/foundation/export/batches/{batch_id}/failed?path={path}"
            conn.request("GET", url, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            # Find the start and end indices of "xdmEntity" in the response
            start_index = data.find('"xdmEntity":{')
            end_index = data.find('}', start_index) + 1
            # Extract the "xdmEntity" part
            xdm_entity_part = data[start_index:end_index]

            # Write batch_id, path, and xdmEntity to the CSV file
            csv_writer.writerow([batch_id, path, xdm_entity_part])

print(f"CSV file '{csv_file_path}' created successfully.")
