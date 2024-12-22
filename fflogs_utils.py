import requests

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
        print(f"Successfully got report data: {response.status_code}")
        print(f"Response Text: {response.text}")
    else:
        print(f"Failed to get report data: {response.status_code} - {response.text}")
        return None

def handle_report(url, client_id, client_secret):
    report_id = url.split('/reports/')[1].split('?')[0]
    access_token = get_fflogs_access_token(client_id, client_secret)

    if access_token:
        report_data = get_fflogs_report(report_id, access_token)
        if report_data:
            print(report_data)