"""Generate a world map of CIM website visitors from GA4 data."""

import json
import subprocess
import sys

import plotly.graph_objects as go

# Country name to ISO-3 mapping for names GA4 uses that don't match plotly
COUNTRY_OVERRIDES = {
    "South Korea": "KOR",
    "Türkiye": "TUR",
    "Hong Kong": "HKG",
    "Taiwan": "TWN",
    "Czechia": "CZE",
    "Palestine": "PSE",
    "Congo - Brazzaville": "COG",
    "Congo - Kinshasa": "COD",
    "St. Vincent & Grenadines": "VCT",
    "Turks & Caicos Islands": "TCA",
    "Cayman Islands": "CYM",
    "Maldives": "MDV",
    "Seychelles": "SYC",
    "Mauritius": "MUS",
}

# Standard ISO-3 lookup
COUNTRY_TO_ISO3 = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA", "Argentina": "ARG",
    "Armenia": "ARM", "Australia": "AUS", "Austria": "AUT", "Azerbaijan": "AZE",
    "Bangladesh": "BGD", "Belarus": "BLR", "Belgium": "BEL", "Bolivia": "BOL",
    "Brazil": "BRA", "Bulgaria": "BGR", "Cambodia": "KHM", "Canada": "CAN",
    "Chile": "CHL", "China": "CHN", "Colombia": "COL", "Costa Rica": "CRI",
    "Croatia": "HRV", "Cyprus": "CYP", "Denmark": "DNK", "Dominican Republic": "DOM",
    "Ecuador": "ECU", "Egypt": "EGY", "Estonia": "EST", "Ethiopia": "ETH",
    "Finland": "FIN", "France": "FRA", "Georgia": "GEO", "Germany": "DEU",
    "Ghana": "GHA", "Greece": "GRC", "Guatemala": "GTM", "Hungary": "HUN",
    "India": "IND", "Indonesia": "IDN", "Iraq": "IRQ", "Ireland": "IRL",
    "Italy": "ITA", "Japan": "JPN", "Kazakhstan": "KAZ", "Kuwait": "KWT",
    "Lithuania": "LTU", "Malawi": "MWI", "Malaysia": "MYS", "Mexico": "MEX",
    "Morocco": "MAR", "Namibia": "NAM", "Nepal": "NPL", "Netherlands": "NLD",
    "New Zealand": "NZL", "Nicaragua": "NIC", "Nigeria": "NGA", "Norway": "NOR",
    "Pakistan": "PAK", "Panama": "PAN", "Peru": "PER", "Philippines": "PHL",
    "Poland": "POL", "Portugal": "PRT", "Qatar": "QAT", "Romania": "ROU",
    "Russia": "RUS", "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB",
    "Singapore": "SGP", "Slovakia": "SVK", "Slovenia": "SVN", "South Africa": "ZAF",
    "Spain": "ESP", "Sri Lanka": "LKA", "Sweden": "SWE", "Switzerland": "CHE",
    "Tanzania": "TZA", "Thailand": "THA", "Uganda": "UGA", "Ukraine": "UKR",
    "United Arab Emirates": "ARE", "United Kingdom": "GBR", "United States": "USA",
    "Venezuela": "VEN", "Vietnam": "VNM", "Zimbabwe": "ZWE",
}
COUNTRY_TO_ISO3.update(COUNTRY_OVERRIDES)
COUNTRY_TO_ISO3.update({
    "Uzbekistan": "UZB", "Zambia": "ZMB", "Myanmar (Burma)": "MMR",
})


def main():
    # Fetch data
    result = subprocess.run(
        [sys.executable, "ga4.py", "custom",
         "--metrics", "activeUsers", "sessions",
         "--dimensions", "country",
         "--start", "7daysAgo", "--end", "yesterday",
         "--limit", "200"],
        capture_output=True, text=True, cwd="."
    )
    data = json.loads(result.stdout)

    countries, users, sessions, iso_codes = [], [], [], []
    for row in data["rows"]:
        name = row["country"]
        if name == "(not set)":
            continue
        iso = COUNTRY_TO_ISO3.get(name)
        if not iso:
            print(f"  Warning: no ISO-3 code for '{name}', skipping")
            continue
        countries.append(name)
        users.append(int(row["activeUsers"]))
        sessions.append(int(row["sessions"]))
        iso_codes.append(iso)

    hover_text = [
        f"<b>{c}</b><br>Active Users: {u}<br>Sessions: {s}"
        for c, u, s in zip(countries, users, sessions)
    ]

    fig = go.Figure(data=go.Choropleth(
        locations=iso_codes,
        z=users,
        text=hover_text,
        hoverinfo="text",
        colorscale="YlOrRd",
        colorbar_title="Active Users",
        marker_line_color="white",
        marker_line_width=0.5,
    ))

    fig.update_layout(
        title=dict(text="CIM Website Visitors by Country (Last 7 Days)", font_size=20, x=0.5),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="lightgray",
            projection_type="natural earth",
            bgcolor="white",
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        width=1200,
        height=650,
    )

    output = "reports/cim-visitors-map-7d.html"
    fig.write_html(output)
    print(f"Map saved to {output}")

    # Also save a static PNG
    try:
        png_output = "reports/cim-visitors-map-7d.png"
        fig.write_image(png_output, scale=2)
        print(f"PNG saved to {png_output}")
    except Exception as e:
        print(f"  PNG export failed ({e}), HTML is still available")


if __name__ == "__main__":
    main()
