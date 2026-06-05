from google_auth_oauthlib.flow import (
    InstalledAppFlow
)

from google.auth.transport.requests import (
    Request
)

from googleapiclient.discovery import (
    build
)

import os
import pickle
from datetime import datetime


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


class GoogleCalendarService:

    def __init__(self):

        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists(
            "token.pickle"
        ):

            with open(
                "token.pickle",
                "rb"
            ) as token:

                creds = pickle.load(
                    token
                )

        if (
            not creds
            or not creds.valid
        ):

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):

                creds.refresh(
                    Request()
                )

            else:

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        "credentials.json",
                        SCOPES
                    )
                )

                creds = (
                    flow.run_local_server(
                        port=0
                    )
                )

            with open(
                "token.pickle",
                "wb"
            ) as token:

                pickle.dump(
                    creds,
                    token
                )

        return build(
            "calendar",
            "v3",
            credentials=creds
        )

    def create_event(self,company_name,role_name,start_time,end_time):

        event = {

            "summary":
                f"{company_name} | {role_name}",

            "description":
                f"""
    Company: {company_name}

    Role: {role_name}

    Scheduled via AI Persona
    """,

            "start": {
                "dateTime": start_time,
                "timeZone":
                    "Asia/Kolkata"
            },

            "end": {
                "dateTime": end_time,
                "timeZone":
                    "Asia/Kolkata"
            }
        }

        created_event = (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event
            )
            .execute()
        )

        return created_event["id"]
    
    def is_slot_busy(self,start_time,end_time):

        body = {

            "timeMin":
                start_time + "+05:30",

            "timeMax":
                end_time + "+05:30",

            "items": [
                {
                    "id": "primary"
                }
            ]
        }

        response = (
            self.service.freebusy()
            .query(
                body=body
            )
            .execute()
        )

        busy = (
            response["calendars"]
            ["primary"]
            ["busy"]
        )

        return len(busy) > 0