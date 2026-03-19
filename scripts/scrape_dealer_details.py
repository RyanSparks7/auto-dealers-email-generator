import requests
import csv
import time
from bs4 import BeautifulSoup

MY_COOKIE = "_cs_c=1; _BEAMER_USER_ID_FmNWbLVp23294=aa657a20-af89-403e-bbb3-f5f0c6015458; _BEAMER_FIRST_VISIT_FmNWbLVp23294=2025-07-01T17:28:30.483Z; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ii8zMVhyK2h3T0ludXkvR1dSbnRaK2c9PSIsInZhbHVlIjoiY0dmU2FLQVpTeHRUVWRWWU1qeHBpY05jTzRUUXMzWTdOWXRsS09jY2Zrc0RqYVFEYThvQ05sQ1hydjFlN2tUSDVValg2UUhXMWgyaDU4NnpGSlMyT3NsUkRqMmtUS01XaTE4Q0hTU1l4eVR5OXgyODRQMFRrR1JpZUx4VTFDMzZiNDU0dnFzYmRqWnFxVTAza1lrWU5qZ21xcEV2VnBlSGdWTlBXREwvaDJaa2V3eFIxcTRERjBnTnNCaVVyVmJSeUVzQS9IRWFIZDIvUjRsVzhBOWhzWnZ5TnZLbjdzOXdrNW9pRXNPbVVlVT0iLCJtYWMiOiI3OGI1ZGZiNWJiMGI0NGM0MGVlOTYzZTFkMzcxNGM1ZGI1MzY4YTQzMDIzMmQxYmRmZjA2OThiMWNmOGE4YmRkIiwidGFnIjoiIn0%3D; _ga=GA1.1.1151463570.1753110854; _BEAMER_DATE_FmNWbLVp23294=2025-09-02T19:30:14.823Z; _cs_id=e6e6f930-4cb8-a1a9-f9e1-4a29482bcb0d.1751390053.49.1771352872.1771352872.1734932206.1785554053245.1.x; _hp2_id.1325449719=%7B%22userId%22%3A%22673966819637494%22%2C%22pageviewId%22%3A%221873617968208111%22%2C%22sessionId%22%3A%223778073724962750%22%2C%22identity%22%3A%22766678315528658328%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _hp2_id.870388005=%7B%22userId%22%3A%224581752264432938%22%2C%22pageviewId%22%3A%223106603307413011%22%2C%22sessionId%22%3A%225502766432693573%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_0RYY2RR2WR=GS2.1.s1772818178$o16$g0$t1772818178$j60$l0$h0; mp_22c76e1f1dfaeebb03ed8c342995906d_mixpanel=%7B%22distinct_id%22%3A%2221535%22%2C%22%24device_id%22%3A%22051b05be-fc6c-4413-85cb-b9df796e1682%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Faccount.autodealersdigital.com%2F%22%2C%22%24initial_referring_domain%22%3A%22account.autodealersdigital.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Faccount.autodealersdigital.com%2F%22%2C%22%24initial_referring_domain%22%3A%22account.autodealersdigital.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22%24user_id%22%3A%2221535%22%7D; AWSALB=sDxRWGi4x2LwJH/vFdIXI56kJfPzue4NBmWWDSOhiWNsWuGb3Qtt4rVS2EDJjV+ZCFbV5tVc0ZjUvsQWiGtFQp+Az0SKowUVL1ul8E8fjcrFgN/EjQXPjTUMy+OA; AWSALBCORS=sDxRWGi4x2LwJH/vFdIXI56kJfPzue4NBmWWDSOhiWNsWuGb3Qtt4rVS2EDJjV+ZCFbV5tVc0ZjUvsQWiGtFQp+Az0SKowUVL1ul8E8fjcrFgN/EjQXPjTUMy+OA; XSRF-TOKEN=eyJpdiI6IitDQ1ZTdkNPdTYvOFpoR09GaWYwZkE9PSIsInZhbHVlIjoiMGJFZDlUd2QrN1VEZ1gzNlYwT213SEdncnlLNWg2UnNuQWRhMk5BNmh2TVBlMUVsaGR5LzRBSjVBeUJYbENWKzhFWmpCd1k0eXdDczFLMTJ4T25sS0llTDhQQUNsSU1QQkRESlhuQmRjWmpkR2ZWby9uR1dyYStpcXU0SlJOYXEiLCJtYWMiOiI1ODA3Y2IxZGU4YTFiOWNhOGM4ZTllMmI0OTNmMTVkOWEzMTBkODFiMDIyOWUzYTNhYmQyOGUxNzdlN2U0YTQ2IiwidGFnIjoiIn0%3D; myaccount_session=eyJpdiI6InNTNFI2VjBodkluUVFHWTB2MGJNbVE9PSIsInZhbHVlIjoidDRXelJoc3Fja1FiUHgzU0pFNlppWWlXRTd5L2Yxb0JYcjQ3OVhGYkRwU3ZHL1pwcmJCSlFkaGJPTk9qU0NwbFdldWhIOUZPbzQ1Z2J3OEQ3bUJXaUpwQkFGSmVkak12Ym5lQUNqRno5WFEvRW9iMHlZSlRiaTFZem5pbXNsSmUiLCJtYWMiOiI1NDg2OGExZDVhYjljNmJkNDA5MzBhYzE1NzFjMTJkZmE5MjY0MjNjNWYxYTkxMTg0ZTc4NDQ4M2MwYTY1OGRkIiwidGFnIjoiIn0%3D"

INPUT_FILE  = "../data/active_dealers.csv"
OUTPUT_FILE = "../data/active_dealers_enriched.csv"

HEADERS = {
    "Cookie": MY_COOKIE,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Referer": "https://account.autodealersdigital.com/admin/dashboard",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def scrape_dealer(user_id):
    url = f"https://account.autodealersdigital.com/admin/dealer/{user_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  [{user_id}] HTTP {r.status_code}")
            return "", "", "", "", ""

        soup = BeautifulSoup(r.text, "html.parser")

        name_tag = soup.find(class_="fs-3 text-gray-800 text-hover-primary fw-bold mb-1")
        dealership_name = name_tag.get_text(strip=True) if name_tag else ""

        phone = ""
        address = ""

        for tag in soup.find_all(class_="fw-bold"):
            txt = tag.get_text(strip=True)
            nxt = tag.find_next_sibling()
            if not nxt:
                continue
            val = nxt.get_text(separator=" ", strip=True)
            if txt == "Phone" and not phone:
                phone = val
            elif txt == "Address" and not address:
                address = val

        return dealership_name, address, phone

    except Exception as e:
        print(f"  [{user_id}] Error: {e}")
        return "", "", ""


def main():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        dealers = list(reader)
        fieldnames = reader.fieldnames

    new_fields = ["dealership_name", "dealer_address", "dealer_phone"]
    out_fields = fieldnames + new_fields

    # Check for already-processed dealers to resume
    import os
    done_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, newline="", encoding="utf-8") as f:
            done_ids = {row["user_id"] for row in csv.DictReader(f)}
        print(f"Resuming — {len(done_ids)} already done, appending...")
        file_mode = "a"
        write_header = False
    else:
        file_mode = "w"
        write_header = True

    total = len(dealers)
    print(f"Total dealers: {total}")

    with open(OUTPUT_FILE, file_mode, newline="", encoding="utf-8", buffering=1) as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        if write_header:
            writer.writeheader()
            f.flush()

        for dealer in dealers:
            uid = dealer["user_id"]
            if uid in done_ids:
                continue
            name, address, phone = scrape_dealer(uid)
            dealer["dealership_name"] = name
            dealer["dealer_address"] = address
            dealer["dealer_phone"] = phone
            writer.writerow(dealer)
            f.flush()

            done_ids.add(uid)
            done_count = len(done_ids)
            if done_count % 25 == 0:
                print(f"  {done_count}/{total} — {uid}: {name}", flush=True)

            time.sleep(0.3)

    print(f"\nDone! Saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
