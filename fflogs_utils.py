import requests

FRU_FILTER_EXPRESSION = "ability.id IN (40140, 40197, 40179, 40212, 40259, 40266, 40269, 40301, 40298, 40306, 40327)"
FRU_FILTER_EXPRESSION_2 = "ability.name IN ('Fall of Faith', 'Diamond Dust', 'Mirror, Mirror', 'Light Rampant', 'Endless Ice Age', 'Ultimate Relativity', 'Spell-In-Waiting', 'Darklit Dragonsong', 'Crystallize Time', 'Fulgent Blade', 'Paradise Lost')"

def get_fflogs_access_token(client_id, client_secret):
    url = 'https://www.fflogs.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(url, data=data, auth=(client_id, client_secret))

    if response.status_code == 200:
        print(f"Successfully got access token: {response.status_code}")
        return response.json()['access_token']
    else:
        print(f"Failed to get access token: {response.status_code} - {response.text}")
        return None


def get_fflogs_events(report_id, fight_id, access_token):
    url = 'https://www.fflogs.com/api/v2/client'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    query = """
    query($reportID: String!, $fightID: Int!, $filterExpression: String!) {
        reportData {
            report(code: $reportID) {
                events(fightIDs: [$fightID], hostilityType: Enemies, useAbilityIDs:false, filterExpression: $filterExpression) {
									data
						}
					}
        }
    }
    """
    variables = {
        'reportID': report_id,
        'fightID': fight_id,
        'filterExpression': FRU_FILTER_EXPRESSION
    }

    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        response_data = response.json()
        ability_names = list({event['ability']['name'] for event in response_data['data']['reportData']['report']['events']['data']})
        return ability_names

def get_fflogs_report(report_id, access_token):
    url = 'https://www.fflogs.com/api/v2/client'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    query = """
    query($reportID: String!) {
        reportData {
            report(code: $reportID) {
                fights {
                    id
                    startTime
                    endTime
                    name
                }
            }
        }
    }
    """
    variables = {
        'reportID': report_id
    }        

    response = requests.get(url, headers=headers, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        print(f"Successfully fetched report data: {response.status_code}")
        response_data = response.json()
        fight_ids = [fight['id'] for fight in response_data['data']['reportData']['report']['fights'] if fight['name'] == 'Futures Rewritten']
        return fight_ids
    else:
        print(f"Failed to get report data: {response.status_code} - {response.text}")
        return None

def handle_report(url, client_id, client_secret):
    report_id = url.split('/reports/')[1].split('?')[0]
    access_token = get_fflogs_access_token(client_id, client_secret)

    if access_token:
        fight_ids = get_fflogs_report(report_id, access_token)
        print(f"Fetched fight ids: {fight_ids}")
        if fight_ids:
            for fight_id in fight_ids:
                ability_game_ids = get_fflogs_events(report_id, fight_id, access_token)
                print(f"Events for fight: {fight_id}, {ability_game_ids}")