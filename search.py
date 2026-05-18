import lightkurve as lk

def search(target, radius, exptime, cadence, mission,
            author, quarter, month, campaign,
            sector, limit):

        results = lk.search_lightcurve(
            target=target,
            radius=radius,
            exptime=exptime,
            cadence=cadence,
            mission=mission,
            author=author,
            quarter=quarter,
            month=month,
            campaign=campaign,
            sector=sector,
            limit=limit
        )

        if len(results) == 0:
            raise ValueError(f"No light curves found for target: {target}")

        return results