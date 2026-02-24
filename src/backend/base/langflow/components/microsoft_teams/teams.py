import httpx

from langflow.custom import Component
from langflow.io import BoolInput, MultilineInput, Output, SecretStrInput, StrInput
from langflow.schema import Data


class TeamsSendMessageComponent(Component):
    display_name = "Microsoft Teams"
    description = (
        "Send messages and report notifications to Microsoft Teams channels using Microsoft Graph. "
        "Supports automated report delivery and human-in-the-loop approval workflows."
    )
    documentation = "https://learn.microsoft.com/graph/api/channel-post-messages"
    icon = "Teams"
    name = "TeamsSendMessage"

    inputs = [
        StrInput(name="tenant_id", display_name="Tenant ID", required=True),
        StrInput(name="client_id", display_name="Client ID", required=True),
        SecretStrInput(name="client_secret", display_name="Client Secret", required=True),
        StrInput(
            name="team_id",
            display_name="Team ID",
            required=True,
            info="The ID of the Microsoft Teams team.",
        ),
        StrInput(
            name="channel_id",
            display_name="Channel ID",
            required=True,
            info="The ID of the channel to post messages to.",
        ),
        MultilineInput(
            name="message",
            display_name="Message",
            required=True,
            info="Message content. Supports plain text or HTML.",
        ),
        StrInput(
            name="content_type",
            display_name="Content Type",
            value="html",
            required=True,
            info="Message content type: text or html.",
        ),
        BoolInput(
            name="require_approval",
            display_name="Require Approval",
            value=False,
            info=(
                "When enabled, the message is returned as a preview instead of being posted, "
                "allowing human review before sending."
            ),
        ),
        StrInput(
            name="subject",
            display_name="Subject",
            required=False,
            info="Optional subject line for the Teams message.",
        ),
        StrInput(
            name="importance",
            display_name="Importance",
            value="normal",
            required=False,
            info="Message importance: normal, high, or urgent.",
        ),
    ]

    outputs = [Output(name="result", display_name="Result", method="send_message")]

    graph_base_url = "https://graph.microsoft.com/v1.0"
    token_scope = "https://graph.microsoft.com/.default"

    def send_message(self) -> Data:
        try:
            with httpx.Client(timeout=20) as client:
                token = self._get_access_token(client)
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                message_payload = self._build_message_payload()

                if self.require_approval:
                    result = self._preview_message(message_payload)
                else:
                    result = self._post_message(client, headers=headers, payload=message_payload)

                self.status = result
                return result
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to process Teams message with the provided configuration."
            raise ValueError(msg) from exc

    def _get_access_token(self, client: httpx.Client) -> str:
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.token_scope,
        }
        try:
            response = client.post(token_url, data=payload)
            response.raise_for_status()
            token = response.json().get("access_token")
            if not token:
                msg = "Unable to authenticate with Microsoft."
                raise ValueError(msg)
            return token
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to authenticate with Microsoft. Verify tenant and client credentials."
            raise ValueError(msg) from exc

    def _build_message_payload(self) -> dict:
        payload: dict = {
            "body": {
                "contentType": self.content_type or "html",
                "content": self.message,
            },
            "importance": self.importance or "normal",
        }
        if self.subject:
            payload["subject"] = self.subject
        return payload

    def _post_message(self, client: httpx.Client, *, headers: dict[str, str], payload: dict) -> Data:
        endpoint = (
            f"{self.graph_base_url}/teams/{self.team_id}"
            f"/channels/{self.channel_id}/messages"
        )
        try:
            response = client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            message_id = result.get("id", "")
            web_url = result.get("webUrl", "")
            return Data(
                text=f"Message posted to Teams channel. Message ID: {message_id}",
                data={
                    "source": "teams",
                    "action": "post",
                    "status": "sent",
                    "message_id": message_id,
                    "web_url": web_url,
                    "team_id": self.team_id,
                    "channel_id": self.channel_id,
                },
            )
        except httpx.HTTPError as exc:
            msg = "Unable to post message to Teams channel."
            raise ValueError(msg) from exc

    def _preview_message(self, payload: dict) -> Data:
        return Data(
            text="Message preview ready for human approval.",
            data={
                "source": "teams",
                "action": "preview",
                "status": "pending_review",
                "team_id": self.team_id,
                "channel_id": self.channel_id,
                "message_body": payload.get("body", {}).get("content", ""),
                "content_type": payload.get("body", {}).get("contentType", "html"),
                "subject": payload.get("subject", ""),
                "importance": payload.get("importance", "normal"),
            },
        )
