import requests
from time_utils import ms_to_datetime, ms_to_hhmmss
from ultimate import FRU

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
    

def get_latest_event(priority_list, events):
    for ability in priority_list:
        if ability in events:
            return ability
    return priority_list[-1]

def get_fflogs_events(report_id, fight_id, access_token, priority_list, filter_expression):
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
        'filterExpression': filter_expression
    }

    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        response_data = response.json()
        ability_names = list({event['ability']['name'] for event in response_data['data']['reportData']['report']['events']['data']})

        latest_event = get_latest_event(priority_list, ability_names)
        return latest_event

def get_fflogs_report(report_id, access_token):
    url = 'https://www.fflogs.com/api/v2/client'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    query = """
    query($reportID: String!) {
        reportData {
            report(code: $reportID) {
                startTime
                endTime
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

        fight_ids = []
        longest_pull_duration = 0
        pull_duration_sum = 0
        raid_start_time = None
        raid_end_time = None

        report_start_time = response_data['data']['reportData']['report']['startTime']

        for fight in response_data['data']['reportData']['report']['fights']:
            pull_duration = fight['endTime'] - fight['startTime']

            # Only include fights from the Ultimate and that are longer than 20 seconds
            if fight['name'] == 'Futures Rewritten' and pull_duration >= 20000:
                fight_ids.append(fight['id'])
                pull_duration_sum += pull_duration

                if raid_start_time is None:
                    raid_start_time = fight['startTime']
                if raid_end_time is None or fight['endTime'] > raid_end_time:
                    raid_end_time = fight['endTime']
                if pull_duration > longest_pull_duration:
                    longest_pull_duration = pull_duration
        
        average_pull_duration = round(pull_duration_sum / len(fight_ids))
        pull_count = len(fight_ids)
        adjusted_raid_start_time = report_start_time + raid_start_time
        adjusted_raid_end_time = report_start_time + raid_end_time

        return fight_ids, pull_count, adjusted_raid_start_time, adjusted_raid_end_time, longest_pull_duration, average_pull_duration, pull_duration_sum
    else:
        print(f"Failed to get report data: {response.status_code} - {response.text}")
        return None

def generate_report_summary(url, client_id, client_secret):
    report_id = url.split('/reports/')[1].split('?')[0]
    access_token = get_fflogs_access_token(client_id, client_secret)

    ult = FRU()

    if access_token:
        fight_ids, pull_count, raid_start_time, raid_end_time, longest_pull_duration, average_pull_duration, pull_duration_sum = get_fflogs_report(report_id, access_token)
        
        raid_duration = raid_end_time - raid_start_time

        latest_event_counts = {event: 0 for event in ult.get_priority_list()}

        if fight_ids:
            for fight_id in fight_ids:
                latest_event = get_fflogs_events(report_id, fight_id, access_token, ult.get_priority_list(), ult.get_filter_expression())
                if latest_event in latest_event_counts:
                    latest_event_counts[latest_event] += 1

        event_counts_summary = ", ".join([f"{ult.get_ability_names()[event]}: {latest_event_counts[event]}" for event in reversed(ult.get_priority_list())])
        
        summary = (
            f"{ult.get_long_name()}\n\n"
            f"Report ID:  \t\t{report_id}\n"
            f"Total pulls:\t\t{pull_count}\n"
            f"Raid start: \t\t{ms_to_datetime(raid_start_time)}\n"
            f"Raid end:   \t\t{ms_to_datetime(raid_end_time)}\n"
            f"Raid duration:  \t{ms_to_hhmmss(raid_duration)}\n"
            f"Time in combat: \t{ms_to_hhmmss(pull_duration_sum)}\n"
            f"Max pull length:\t{ms_to_hhmmss(longest_pull_duration)}\n"
            f"Avg pull length:\t{ms_to_hhmmss(average_pull_duration)}\n\n"
            f"Additional {ult.get_short_name()} information - Wipes by phase:\n\n"
            f"{event_counts_summary}"
        )

        return summary