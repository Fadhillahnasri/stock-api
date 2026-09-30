from app.utils.logger import logger


HISTORICAL_SCENARIOS = {
    "lehman_2008": {
        "id": "lehman_2008",
        "name": "Lehman Brothers / Global Financial Crisis",
        "startDate": "2008-09-15",
        "endDate": "2008-10-31",
        "description": (
            "Historical market stress associated with the collapse "
            "of Lehman Brothers and the escalation of the global "
            "financial crisis."
        ),
        "source": "Federal Reserve",
    },
    "greece_2010": {
        "id": "greece_2010",
        "name": "Greece Debt Crisis",
        "startDate": "2010-05-03",
        "endDate": "2010-05-31",
        "description": (
            "Historical market stress associated with the escalation "
            "of the Greek sovereign debt crisis."
        ),
        "source": "International Monetary Fund",
    },
    "oil_2010": {
        "id": "oil_2010",
        "name": "Oil Price Shock 2010",
        "startDate": "2010-05-03",
        "endDate": "2010-05-28",
        "description": (
            "Historical oil price decline during May 2010."
        ),
        "source": "U.S. Energy Information Administration",
    },
    "trade_war_2018": {
        "id": "trade_war_2018",
        "name": "US-China Trade Tensions",
        "startDate": "2018-10-01",
        "endDate": "2018-10-31",
        "description": (
            "Historical market stress associated with escalating "
            "US-China trade tensions and October 2018 equity volatility."
        ),
        "source": "Federal Reserve",
    },
    "covid_2020": {
        "id": "covid_2020",
        "name": "COVID-19 Market Crash",
        "startDate": "2020-02-19",
        "endDate": "2020-03-23",
        "description": (
            "Historical equity market stress during the initial "
            "COVID-19 market crash."
        ),
        "source": "Federal Reserve",
    },
}


def get_historical_scenarios():
    logger.info("Historical Scenario - Get All Scenarios")

    return list(HISTORICAL_SCENARIOS.values())


def get_historical_scenario(scenario_id: str):
    scenario_id = scenario_id.strip().lower()

    logger.info(
        f"Historical Scenario - Get Scenario: {scenario_id}"
    )

    return HISTORICAL_SCENARIOS.get(scenario_id)