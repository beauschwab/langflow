import httpx

from langflow.components.microsoft_templates.registry import (
    get_teams_template_names,
    get_template,
    parse_field_mapping,
    render_template,
)
from langflow.custom import Component
from langflow.io import BoolInput, DropdownInput, MultilineInput, Output, SecretStrInput, StrInput
from langflow.schema import Data
from langflow.schema.content_block import ContentBlock
from langflow.schema.content_types import CodeContent, JSONContent, TextContent


class TeamsSendMessageComponent(Component):
    display_name = "Microsoft Teams"
    description = (
        "Send messages and report notifications to Microsoft Teams channels using Microsoft Graph. "
        "Supports automated report delivery, selectable templates (including Adaptive Cards), "
        "and human-in-the-loop approval workflows."
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
            info="Message content. Supports plain text or HTML. Ignored when a template is selected.",
        ),
        StrInput(
            name="content_type",
            display_name="Content Type",
            value="html",
            required=True,
            info="Message content type: text or html.",
        ),
        DropdownInput(
            name="template_name",
            display_name="Template",
            options=["None", *get_teams_template_names()],
            value="None",
            required=False,
            info=(
                "Select a pre-designed message template or Adaptive Card. "
                "Field values are taken from the Field Mapping input."
            ),
        ),
        MultilineInput(
            name="field_mapping",
            display_name="Field Mapping",
            required=False,
            info=(
                "Map structured data to template fields as key:value pairs, one per line. "
                "Example:\ntitle: Sprint Review\nsummary: All tasks completed\n"
                "facts: Velocity: 42, Stories: 8, Bugs: 2"
            ),
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
            rendered_content = self._resolve_content()
            is_adaptive_card = self._is_adaptive_card(rendered_content)

            with httpx.Client(timeout=20) as client:
                token = self._get_access_token(client)
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                message_payload = self._build_message_payload(rendered_content, is_adaptive_card=is_adaptive_card)

                if self.require_approval:
                    result = self._preview_message(message_payload, rendered_content)
                else:
                    result = self._post_message(client, headers=headers, payload=message_payload)

                result.data["template"] = self.template_name if self.template_name != "None" else None
                result.data["content_blocks"] = self._build_content_blocks(rendered_content, result)
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

    def _build_message_payload(self, content: str, *, is_adaptive_card: bool = False) -> dict:
        if is_adaptive_card:
            import json as _json

            card_obj = _json.loads(content)
            payload: dict = {
                "body": {
                    "contentType": "html",
                    "content": "",
                },
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": card_obj,
                    }
                ],
                "importance": self.importance or "normal",
            }
        else:
            payload = {
                "body": {
                    "contentType": self.content_type or "html",
                    "content": content,
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

    def _preview_message(self, payload: dict, rendered_content: str) -> Data:
        return Data(
            text="Message preview ready for human approval.",
            data={
                "source": "teams",
                "action": "preview",
                "status": "pending_review",
                "team_id": self.team_id,
                "channel_id": self.channel_id,
                "message_body": rendered_content,
                "content_type": payload.get("body", {}).get("contentType", "html"),
                "subject": payload.get("subject", ""),
                "importance": payload.get("importance", "normal"),
            },
        )

    # ------------------------------------------------------------------
    # Template helpers
    # ------------------------------------------------------------------

    def _resolve_content(self) -> str:
        """Return the message content — either rendered from a template or raw."""
        if self.template_name and self.template_name != "None":
            values = self._parse_field_mapping()
            return render_template(self.template_name, values)
        return self.message

    @staticmethod
    def _is_adaptive_card(content: str) -> bool:
        """Detect if rendered content is an Adaptive Card JSON payload."""
        stripped = content.strip()
        return stripped.startswith("{") and '"AdaptiveCard"' in stripped

    def _parse_field_mapping(self) -> dict[str, str]:
        return parse_field_mapping(self.field_mapping)

    @staticmethod
    def _build_content_blocks(rendered_content: str, result: Data) -> list[dict]:
        """Build ContentBlock dicts for rich playground preview."""
        import json as _json

        blocks: list[dict] = []
        tpl_name = result.data.get("template")
        status = result.data.get("status", "")

        # Header block
        header_text = (
            f"✅ Message posted to Teams — {status}"
            if status == "sent"
            else "📝 Message preview — awaiting human approval"
        )
        header_block = ContentBlock(
            title="Teams",
            contents=[TextContent(text=header_text)],
        )
        blocks.append(header_block.model_dump())

        # Template preview block
        if tpl_name:
            tpl = get_template(tpl_name)
            tpl_desc = tpl["description"] if tpl else ""
            is_card = rendered_content.strip().startswith("{") and '"AdaptiveCard"' in rendered_content
            if is_card:
                try:
                    card_data = _json.loads(rendered_content)
                except _json.JSONDecodeError:
                    card_data = {"raw": rendered_content}
                preview_block = ContentBlock(
                    title=f"Template: {tpl_name}",
                    contents=[
                        TextContent(text=tpl_desc),
                        JSONContent(data=card_data),
                    ],
                )
            else:
                preview_block = ContentBlock(
                    title=f"Template: {tpl_name}",
                    contents=[
                        TextContent(text=tpl_desc),
                        CodeContent(code=rendered_content, language="html", title="Rendered Content"),
                    ],
                )
            blocks.append(preview_block.model_dump())

        return blocks
