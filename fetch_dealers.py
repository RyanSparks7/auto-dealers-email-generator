import requests
import csv
import time

MY_COOKIE = "_cs_c=1; _BEAMER_USER_ID_FmNWbLVp23294=aa657a20-af89-403e-bbb3-f5f0c6015458; _BEAMER_FIRST_VISIT_FmNWbLVp23294=2025-07-01T17:28:30.483Z; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ii8zMVhyK2h3T0ludXkvR1dSbnRaK2c9PSIsInZhbHVlIjoiY0dmU2FLQVpTeHRUVWRWWU1qeHBpY05jTzRUUXMzWTdOWXRsS09jY2Zrc0RqYVFEYThvQ05sQ1hydjFlN2tUSDVValg2UUhXMWgyaDU4NnpGSlMyT3NsUkRqMmtUS01XaTE4Q0hTU1l4eVR5OXgyODRQMFRrR1JpZUx4VTFDMzZiNDU0dnFzYmRqWnFxVTAza1lrWU5qZ21xcEV2VnBlSGdWTlBXREwvaDJaa2V3eFIxcTRERjBnTnNCaVVyVmJSeUVzQS9IRWFIZDIvUjRsVzhBOWhzWnZ5TnZLbjdzOXdrNW9pRXNPbVVlVT0iLCJtYWMiOiI3OGI1ZGZiNWJiMGI0NGM0MGVlOTYzZTFkMzcxNGM1ZGI1MzY4YTQzMDIzMmQxYmRmZjA2OThiMWNmOGE4YmRkIiwidGFnIjoiIn0%3D; _ga=GA1.1.1151463570.1753110854; _BEAMER_DATE_FmNWbLVp23294=2025-09-02T19:30:14.823Z; _cs_id=e6e6f930-4cb8-a1a9-f9e1-4a29482bcb0d.1751390053.49.1771352872.1771352872.1734932206.1785554053245.1.x; _hp2_id.1325449719=%7B%22userId%22%3A%22673966819637494%22%2C%22pageviewId%22%3A%221873617968208111%22%2C%22sessionId%22%3A%223778073724962750%22%2C%22identity%22%3A%22766678315528658328%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _hp2_id.870388005=%7B%22userId%22%3A%224581752264432938%22%2C%22pageviewId%22%3A%223106603307413011%22%2C%22sessionId%22%3A%225502766432693573%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_0RYY2RR2WR=GS2.1.s1772818178$o16$g0$t1772818178$j60$l0$h0; mp_22c76e1f1dfaeebb03ed8c342995906d_mixpanel=%7B%22distinct_id%22%3A%2221535%22%2C%22%24device_id%22%3A%22051b05be-fc6c-4413-85cb-b9df796e1682%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Faccount.autodealersdigital.com%2F%22%2C%22%24initial_referring_domain%22%3A%22account.autodealersdigital.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Faccount.autodealersdigital.com%2F%22%2C%22%24initial_referring_domain%22%3A%22account.autodealersdigital.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22%24user_id%22%3A%2221535%22%7D; XSRF-TOKEN=eyJpdiI6IlhxYWJ5MzJVTEo0dEVSdU9SaG0vSUE9PSIsInZhbHVlIjoiYnpzNWlneG9ERk90NUhrWnl2Yk5iWHJnamdkTTFkSldBUlBsR1M4a3BPL3ZIR1VFTnpWdFY0Q1hGV0NFN1lGVkFMM3l4d1pBaU1UVVVwUk5mQWxJcmFIK3p1YUVXaHRBb0R4SjREcWRGZVZMYzJuUU4wRE5nV0lodjNQM04rTUkiLCJtYWMiOiJiZTBiMzU4N2FhZjk5NWI4YjBmYTZhMjFlNTI3MjgzMTJiZmViMTZjMzRjODZjOTIwM2ZlNTkwYjkxYzQ5OTE3IiwidGFnIjoiIn0%3D; ad_hub_session=eyJpdiI6ImpZQ01ralRjeUdOS3dFREozcE5vMnc9PSIsInZhbHVlIjoiTkFEMFMrQmloK3V2cXZFb1Q4TXRFMk0wMG80Y21FMlVDYjk2OE5RbmFzZFhoSGxFRzVsL2NINDB6eVkxdmRsK05haXBtTWtaN2s1NWpaS0ZXdXVYNGQwZW1lMFB4cC9BMThLV1pxWk44aXBYYlpLeklYaWtxa091OHBET0c4dUMiLCJtYWMiOiI5OTI5ZWQ1NTZlY2Y1OTEyODkzODVjMWU3OWE0ZTU5MTU4MmM5YTFhYTY4NmRiZDhkYjNjNWY1MmEyYWVhYmUzIiwidGFnIjoiIn0%3D; AWSALB=62k4So9KC/U/54RZ3r49TotfwNphkKk1foFQYg5znWlEeoiFHBJlv/cDnxiNCIRFnisT6M/mwMt8DDxMAIOx350VkO6NCzAIpthYZZKnoh6ApcxaWACv+ar+oVuU; AWSALBCORS=62k4So9KC/U/54RZ3r49TotfwNphkKk1foFQYg5znWlEeoiFHBJlv/cDnxiNCIRFnisT6M/mwMt8DDxMAIOx350VkO6NCzAIpthYZZKnoh6ApcxaWACv+ar+oVuU; XSRF-TOKEN=eyJpdiI6Ik5LM0RLN0Jza3BZVGd0d3pYc2RVdXc9PSIsInZhbHVlIjoienRWTEswTFFuVVpwaUxZVlBTK1BiRmJyaEhlcUh0aFFWcGJtS1RENXUrT1lTdTZCbzB4ZzUrMCtHck1nYU5IVWRDcmFnc2VrdFN2SW9ORmxMYk5BM29ZNVRrb3BXdmtvUUdhVFhBbWJ1VnpYTStkeDZkQXJlUXI0OFNYODRzTWoiLCJtYWMiOiJhZDZkZGI0ZWFiZjZiMzUxYzBjYWE4NWM5Njg1MDMxNzhmZmJmMGE1MTAzZmQ5ZjY4MmUwY2EwZWQ3NDA5MmY0IiwidGFnIjoiIn0%3D; myaccount_session=eyJpdiI6IjduUVMvQjhsaHhEdk1zSDJwRjh3VXc9PSIsInZhbHVlIjoiVVdIQlZpZG1mSndSZU9vcS9qMXRBM3RTTEpmZldsTll4aDIrcUFDM3VZb3JkTEg5azMrbEh6ZkQxeVZQdmhxazRXTjg5bXdpRHVIUWduWFJYMEpicjlLMlhnd3VoeXRQNXQ0TlJzM2dsbTJLSjNDY2hEbzJoL1dlUlJVVVR0T28iLCJtYWMiOiI0N2FmYzg3N2UxZDMzYzNkOWQ2MDMzNjMxZTViMDYzNDViNDViMzEzODk4MTBiZmU0NzhkMTdjMjEzMzg4Y2MzIiwidGFnIjoiIn0%3D"

BASE_URL = "https://account.autodealersdigital.com/admin/dashboard"
PAGE_SIZE = 25
OUTPUT_FILE = "active_dealers.csv"

FIELDS = [
    "user_id", "status", "email", "sales_person",
    "state", "city", "promo_code",
    "register_date", "next_billing_date", "special_price"
]

HEADERS = {
    "Cookie": MY_COOKIE,
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://account.autodealersdigital.com/admin/dashboard",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
}

def build_params(start):
    params = {
        "draw": 1,
        "order[0][column]": 0,
        "order[0][dir]": "desc",
        "order[0][name]": "user_id",
        "start": start,
        "length": PAGE_SIZE,
        "search[value]": "",
        "search[regex]": "false",
        "status_type": "",
        "date_range": "",
        "search_text": "",
        "state": "",
        "promo_code": "",
    }
    for i, field in enumerate(FIELDS):
        params[f"columns[{i}][data]"] = field
        params[f"columns[{i}][name]"] = field
        params[f"columns[{i}][searchable]"] = "true"
        params[f"columns[{i}][orderable]"] = "false"
        params[f"columns[{i}][search][value]"] = ""
        params[f"columns[{i}][search][regex]"] = "false"
    return params

def fetch_all_dealers():
    all_dealers = []
    start = 0
    total = None

    print("Starting export...")

    while True:
        params = build_params(start)
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Error at start={start}: Status {response.status_code}")
            break

        data = response.json()

        if total is None:
            total = data["recordsFiltered"]
            print(f"Total active dealers found: {total}")

        records = data["data"]
        if not records:
            break

        all_dealers.extend(records)
        print(f"Fetched {len(all_dealers)} / {total} dealers...")

        start += PAGE_SIZE
        if start >= total:
            break

        time.sleep(0.3)

    return all_dealers

def save_to_csv(dealers):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(dealers)
    print(f"\nDone! {len(dealers)} dealers saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    dealers = fetch_all_dealers()
    save_to_csv(dealers)
