#!/usr/bin/env python3
"""
Pull GSC + GA4 data for all PhotonBuilder sites.
Stores locally in data/seo/ — query once, reason many times.

Usage:
  python3 scripts/seo-pull.py              # pull all sites
  python3 scripts/seo-pull.py westmount    # pull one site
  python3 scripts/seo-pull.py --ga-only    # GA4 only
  python3 scripts/seo-pull.py --gsc-only   # GSC only
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta

# Google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
DATA = BASE / "data" / "seo"
TOKEN_PATH = DATA / "google_token.pickle"

# OAuth scopes
SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# Site configs: domain → { gsc_property, ga_property_id, folder_name }
SITES = {
    "westmount": {
        "gsc": "sc-domain:westmountfundamentals.com",
        "ga": "properties/527954181",
        "domain": "westmountfundamentals.com",
    },
    "siliconbased": {
        "gsc": "sc-domain:siliconbased.dev",
        "ga": "properties/528410108",
        "domain": "siliconbased.dev",
    },
    "firemaths": {
        "gsc": "sc-domain:firemaths.info",
        "ga": "properties/528415032",
        "domain": "firemaths.info",
    },
    "28grams": {
        "gsc": "sc-domain:28grams.vip",
        "ga": "properties/528378719",
        "domain": "28grams.vip",
    },
    "migratingmammals": {
        "gsc": "sc-domain:migratingmammals.com",
        "ga": "properties/528407891",
        "domain": "migratingmammals.com",
    },
    "leeroyjenkins": {
        "gsc": "sc-domain:leeroyjenkins.quest",
        "ga": "properties/528389326",
        "domain": "leeroyjenkins.quest",
    },
    "ijustwantto": {
        "gsc": "sc-domain:ijustwantto.live",
        "ga": "properties/528427172",
        "domain": "ijustwantto.live",
    },
    "nookienook": {
        "gsc": "sc-domain:thenookienook.com",
        "ga": "properties/528433564",
        "domain": "thenookienook.com",
    },
    "photonbuilder": {
        "gsc": "sc-domain:photonbuilder.com",
        "ga": "properties/528386310",
        "domain": "photonbuilder.com",
    },
    "bodycount": {
        "gsc": "sc-domain:bodycount.photonbuilder.com",
        "ga": "properties/529363724",
        "domain": "bodycount.photonbuilder.com",
    },
    "sendnerds": {
        "gsc": "sc-domain:sendnerds.photonbuilder.com",
        "ga": "properties/529337618",
        "domain": "sendnerds.photonbuilder.com",
    },
    "justonemoment": {
        "gsc": "sc-domain:justonemoment.photonbuilder.com",
        "ga": "properties/529323503",
        "domain": "justonemoment.photonbuilder.com",
    },
    "getthebag": {
        "gsc": "sc-domain:getthebag.photonbuilder.com",
        "ga": "properties/529340038",
        "domain": "getthebag.photonbuilder.com",
    },
    "fixitwithducttape": {
        "gsc": "sc-domain:fixitwithducttape.photonbuilder.com",
        "ga": "properties/529347118",
        "domain": "fixitwithducttape.photonbuilder.com",
    },
    "papyruspeople": {
        "gsc": "sc-domain:papyruspeople.photonbuilder.com",
        "ga": "properties/529345473",
        "domain": "papyruspeople.photonbuilder.com",
    },
    "eeniemeenie": {
        "gsc": "sc-domain:eeniemeenie.photonbuilder.com",
        "ga": "properties/529374256",
        "domain": "eeniemeenie.photonbuilder.com",
    },
    "pleasestartplease": {
        "gsc": "sc-domain:pleasestartplease.photonbuilder.com",
        "ga": "properties/529324505",
        "domain": "pleasestartplease.photonbuilder.com",
    },
}

GOG_CREDS = Path(os.path.expanduser("~/Library/Application Support/gogcli/credentials.json"))


def get_credentials():
    """Get or refresh Google OAuth credentials."""
    creds = None

    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)
        return creds

    # Need new auth — use gog's client credentials
    if GOG_CREDS.exists():
        raw = json.loads(GOG_CREDS.read_text())
        client_config = {
            "installed": {
                "client_id": raw["client_id"],
                "client_secret": raw["client_secret"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        }
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        print("❌ No Google credentials found. Need gog credentials.json")
        sys.exit(1)

    with open(TOKEN_PATH, "wb") as f:
        pickle.dump(creds, f)

    return creds


def pull_gsc(creds, site_id: str, site_config: dict):
    """Pull GSC data: queries + pages for last 28 days."""
    print(f"  📊 GSC: {site_config['domain']}...")

    try:
        service = build("searchconsole", "v1", credentials=creds)
        today = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")

        # Pull query data
        query_response = service.searchanalytics().query(
            siteUrl=site_config["gsc"],
            body={
                "startDate": start,
                "endDate": today,
                "dimensions": ["query"],
                "rowLimit": 5000,
                "dataState": "all",
            },
        ).execute()

        queries = []
        for row in query_response.get("rows", []):
            queries.append({
                "query": row["keys"][0],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0), 4),
                "position": round(row.get("position", 0), 1),
            })

        # Pull page data
        page_response = service.searchanalytics().query(
            siteUrl=site_config["gsc"],
            body={
                "startDate": start,
                "endDate": today,
                "dimensions": ["page"],
                "rowLimit": 5000,
                "dataState": "all",
            },
        ).execute()

        pages = []
        for row in page_response.get("rows", []):
            pages.append({
                "page": row["keys"][0],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0), 4),
                "position": round(row.get("position", 0), 1),
            })

        # Pull query+page combo (what queries drive what pages)
        combo_response = service.searchanalytics().query(
            siteUrl=site_config["gsc"],
            body={
                "startDate": start,
                "endDate": today,
                "dimensions": ["query", "page"],
                "rowLimit": 10000,
                "dataState": "all",
            },
        ).execute()

        combos = []
        for row in combo_response.get("rows", []):
            combos.append({
                "query": row["keys"][0],
                "page": row["keys"][1],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0), 4),
                "position": round(row.get("position", 0), 1),
            })

        # Save
        out_dir = DATA / "gsc" / site_id
        out_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "pulled": datetime.now().isoformat(),
            "site": site_config["domain"],
            "period": {"start": start, "end": today},
            "queries": sorted(queries, key=lambda x: x["impressions"], reverse=True),
            "pages": sorted(pages, key=lambda x: x["impressions"], reverse=True),
            "query_page_combos": sorted(combos, key=lambda x: x["impressions"], reverse=True),
        }

        filename = f"{today}.json"
        (out_dir / filename).write_text(json.dumps(data, indent=2))

        # Update latest symlink
        latest = out_dir / "latest.json"
        if latest.is_symlink():
            latest.unlink()
        latest.symlink_to(filename)

        print(f"    ✅ {len(queries)} queries, {len(pages)} pages, {len(combos)} combos")
        return data

    except Exception as e:
        print(f"    ❌ GSC error: {e}")
        return None


def pull_ga(creds, site_id: str, site_config: dict):
    """Pull GA4 data: top pages by sessions for last 28 days."""
    print(f"  📈 GA4: {site_config['domain']}...")

    try:
        service = build("analyticsdata", "v1beta", credentials=creds)
        today = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")

        response = service.properties().runReport(
            property=site_config["ga"],
            body={
                "dateRanges": [{"startDate": start, "endDate": today}],
                "dimensions": [
                    {"name": "pagePath"},
                    {"name": "pageTitle"},
                ],
                "metrics": [
                    {"name": "sessions"},
                    {"name": "totalUsers"},
                    {"name": "screenPageViews"},
                    {"name": "bounceRate"},
                    {"name": "averageSessionDuration"},
                ],
                "limit": 5000,
                "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            },
        ).execute()

        pages = []
        for row in response.get("rows", []):
            pages.append({
                "path": row["dimensionValues"][0]["value"],
                "title": row["dimensionValues"][1]["value"],
                "sessions": int(row["metricValues"][0]["value"]),
                "users": int(row["metricValues"][1]["value"]),
                "pageviews": int(row["metricValues"][2]["value"]),
                "bounceRate": round(float(row["metricValues"][3]["value"]), 3),
                "avgDuration": round(float(row["metricValues"][4]["value"]), 1),
            })

        # Save
        out_dir = DATA / "ga" / site_id
        out_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "pulled": datetime.now().isoformat(),
            "site": site_config["domain"],
            "period": {"start": start, "end": today},
            "pages": pages,
            "totalSessions": sum(p["sessions"] for p in pages),
            "totalUsers": sum(p["users"] for p in pages),
        }

        filename = f"{today}.json"
        (out_dir / filename).write_text(json.dumps(data, indent=2))

        latest = out_dir / "latest.json"
        if latest.is_symlink():
            latest.unlink()
        latest.symlink_to(filename)

        print(f"    ✅ {len(pages)} pages, {data['totalSessions']} sessions, {data['totalUsers']} users")
        return data

    except Exception as e:
        print(f"    ❌ GA4 error: {e}")
        return None


def update_snapshots(site_id: str, gsc_file: str = None, ga_file: str = None):
    """Update the snapshots index."""
    snap_path = DATA / "snapshots.json"
    snapshots = json.loads(snap_path.read_text()) if snap_path.exists() else {}

    if site_id not in snapshots:
        snapshots[site_id] = {}

    today = datetime.now().strftime("%Y-%m-%d")
    if gsc_file:
        snapshots[site_id]["gsc"] = {"lastPull": today, "file": gsc_file}
    if ga_file:
        snapshots[site_id]["ga"] = {"lastPull": today, "file": ga_file}

    snap_path.write_text(json.dumps(snapshots, indent=2))


def main():
    args = sys.argv[1:]
    gsc_only = "--gsc-only" in args
    ga_only = "--ga-only" in args
    args = [a for a in args if not a.startswith("--")]

    target_sites = args if args else list(SITES.keys())

    print("🔑 Authenticating...")
    creds = get_credentials()
    print("✅ Authenticated\n")

    today = datetime.now().strftime("%Y-%m-%d")

    for site_id in target_sites:
        if site_id not in SITES:
            print(f"⚠️  Unknown site: {site_id}, skipping")
            continue

        config = SITES[site_id]
        print(f"\n🌐 {config['domain']}")

        gsc_file = None
        ga_file = None

        if not ga_only:
            result = pull_gsc(creds, site_id, config)
            if result:
                gsc_file = f"gsc/{site_id}/{today}.json"

        if not gsc_only and config.get("ga"):
            result = pull_ga(creds, site_id, config)
            if result:
                ga_file = f"ga/{site_id}/{today}.json"

        update_snapshots(site_id, gsc_file, ga_file)

    print("\n✅ Done. Data saved to data/seo/")


if __name__ == "__main__":
    main()
