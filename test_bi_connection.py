import urllib.request


url = "https://www.bi.go.id/biwebservice/wskursbi.asmx"

soap_body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:web="http://www.bi.go.id/">
    <soap:Body>
        <web:getSubKursJisdor3>
            <web:mts>USD</web:mts>
            <web:startdate>2026-09-28</web:startdate>
            <web:enddate>2026-09-29</web:enddate>
        </web:getSubKursJisdor3>
    </soap:Body>
</soap:Envelope>
"""

data = soap_body.encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    method="POST",
    headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": '"http://www.bi.go.id/getSubKursJisdor3"',
        "User-Agent": "Mozilla/5.0",
    },
)

try:
    with urllib.request.urlopen(
        request,
        timeout=10
    ) as response:

        result = response.read().decode("utf-8")

        print("SUCCESS")
        print(result[:3000])

except Exception as e:
    print("ERROR")
    print(type(e).__name__)
    print(e)