import http.client

batch_ids = ["01HJ998VSTND2T3K1XXZZ6CZ4F","01HJ97HW4CHT3DD478VG0M0CE8","01HJ9384AQNG3RYQSFAV0Q9TQY","01HJ90P3SD2NPMC9DVVAXHEVCX","01HJ88NPP8TFA73VD0Z869TFD9"]
paths = ["115650.8ea0acd4-779c-43aa-8ace-1bfe1c06dab2.184.ndjson","115648.c6cdbe0b-ad75-42e8-afd1-a9938512922f.491.ndjson","115643.49ec1f98-e9dd-4f64-81e0-8c1ebc067018.200.ndjson","115640.abe27827-d904-4e48-be26-4c29767baca7.400.ndjson","115612.1ba124fe-6536-45a2-a1fd-207ff50ffc99.147.ndjson"]

conn = http.client.HTTPSConnection("platform.adobe.io")
payload = ''
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer XXXXXXXXXXXXXXXX',
    'x-api-key': 'XXXXXXXXXXXXXXXX',
    'x-gw-ims-org-id': 'XXXXXXXXXXXXXXXX@AdobeOrg',
    'x-sandbox-name': 'prod'
}


for batch_id in batch_ids:
    for path in paths:
        url = f"/data/foundation/export/batches/{batch_id}/failed?path={path}"
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
