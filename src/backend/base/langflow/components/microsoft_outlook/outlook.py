import httpx

from langflow.components.microsoft_templates.registry import (
    get_outlook_template_names,
    get_template,
    render_template,
)
from langflow.custom import Component
from langflow.io import BoolInput, DropdownInput, MultilineInput, Output, SecretStrInput, StrInput
from langflow.schema import Data
from langflow.schema.content_block import ContentBlock
from langflow.schema.content_types import CodeContent, TextContent


class OutlookSendEmailComponent(Component):
    display_name = "Microsoft Outlook"
    description = (
        "Send emails and report notifications via Microsoft Outlook using Microsoft Graph. "
        "Supports automated report delivery, selectable templates, and human-in-the-loop approval workflows."
    )
    documentation = "https://learn.microsoft.com/graph/api/user-sendmail"
    icon = "Outlook"
    name = "OutlookSendEmail"

    inputs = [
        StrInput(name="tenant_id", display_name="Tenant ID", required=True),
        StrInput(name="client_id", display_name="Client ID", required=True),
        SecretStrInput(name="client_secret", display_name="Client Secret", required=True),
        StrInput(
            name="sender_email",
            display_name="Sender Email",
            required=True,
            info="Email address of the sender (must have Send.Mail permission).",
        ),
        StrInput(
            name="recipient_emails",
            display_name="Recipient Emails",
            required=True,
            info="Comma-separated list of recipient email addresses.",
        ),
        StrInput(name="subject", display_name="Subject", required=True),
        MultilineInput(
            name="body",
            display_name="Body",
            required=True,
            info="Email body content. Supports plain text or HTML. Ignored when a template is selected.",
        ),
        DropdownInput(
            name="body_content_type",
            display_name="Body Content Type",
            options=["Text", "HTML"],
            value="HTML",
            required=True,
        ),
        DropdownInput(
            name="template_name",
            display_name="Template",
            options=["None", *get_outlook_template_names()],
            value="None",
            required=False,
            info="Select a pre-designed email template. Field values are taken from the Field Mapping input.",
        ),
        MultilineInput(
            name="field_mapping",
            display_name="Field Mapping",
            required=False,
            info=(
                "Map structured data to template fields as key:value pairs, one per line. "
                "Example:\ntitle: Weekly Report\nsummary: Revenue up 12%\nmetrics: ARR $5M, MRR $420K"
            ),
        ),
        BoolInput(
            name="require_approval",
            display_name="Require Approval",
            value=False,
            info="When enabled, the email is saved as a draft instead of sent, allowing human review.",
        ),
        StrInput(
            name="cc_emails",
            display_name="CC Emails",
            required=False,
            info="Comma-separated list of CC email addresses.",
        ),
        StrInput(
            name="importance",
            display_name="Importance",
            value="normal",
            required=False,
            info="Email importance: low, normal, or high.",
        ),
    ]

    outputs = [Output(name="result", display_name="Result", method="send_email")]

    graph_base_url = "https://graph.microsoft.com/v1.0"
    token_scope = "https://graph.microsoft.com/.default"

    def send_email(self) -> Data:
        try:
            rendered_body = self._resolve_body()

            with httpx.Client(timeout=20) as client:
                token = self._get_access_token(client)
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                message_payload = self._build_message_payload(rendered_body)

                if self.require_approval:
                    result = self._create_draft(client, headers=headers, payload=message_payload)
                else:
                    result = self._send_mail(client, headers=headers, payload=message_payload)

                result.data["template"] = self.template_name if self.template_name != "None" else None
                result.data["content_blocks"] = self._build_content_blocks(rendered_body, result)
                self.status = result
                return result
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to process Outlook email with the provided configuration."
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

    def _build_message_payload(self, body_content: str) -> dict:
        to_recipients = [
            {"emailAddress": {"address": addr.strip()}}
            for addr in self.recipient_emails.split(",")
            if addr.strip()
        ]
        content_type = "HTML" if (self.template_name and self.template_name != "None") else self.body_content_type
        message: dict = {
            "subject": self.subject,
            "body": {
                "contentType": content_type,
                "content": body_content,
            },
            "toRecipients": to_recipients,
            "importance": self.importance or "normal",
        }

        if self.cc_emails:
            cc_recipients = [
                {"emailAddress": {"address": addr.strip()}}
                for addr in self.cc_emails.split(",")
                if addr.strip()
            ]
            message["ccRecipients"] = cc_recipients

        return message

    def _send_mail(self, client: httpx.Client, *, headers: dict[str, str], payload: dict) -> Data:
        endpoint = f"{self.graph_base_url}/users/{self.sender_email}/sendMail"
        body = {"message": payload, "saveToSentItems": True}
        try:
            response = client.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            return Data(
                text="Email sent successfully.",
                data={
                    "source": "outlook",
                    "action": "send",
                    "status": "sent",
                    "subject": self.subject,
                    "recipients": self.recipient_emails,
                },
            )
        except httpx.HTTPError as exc:
            msg = "Unable to send email via Outlook."
            raise ValueError(msg) from exc

    def _create_draft(self, client: httpx.Client, *, headers: dict[str, str], payload: dict) -> Data:
        endpoint = f"{self.graph_base_url}/users/{self.sender_email}/messages"
        try:
            response = client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            draft = response.json()
            draft_id = draft.get("id", "")
            web_link = draft.get("webLink", "")
            return Data(
                text=f"Draft created for human review. Draft ID: {draft_id}",
                data={
                    "source": "outlook",
                    "action": "draft",
                    "status": "pending_review",
                    "draft_id": draft_id,
                    "web_link": web_link,
                    "subject": self.subject,
                    "recipients": self.recipient_emails,
                },
            )
        except httpx.HTTPError as exc:
            msg = "Unable to create draft email in Outlook."
            raise ValueError(msg) from exc

    # ------------------------------------------------------------------
    # Template helpers
    # ------------------------------------------------------------------

    def _resolve_body(self) -> str:
        """Return the email body — either rendered from a template or raw."""
        if self.template_name and self.template_name != "None":
            values = self._parse_field_mapping()
            return render_template(self.template_name, values)
        return self.body

    @staticmethod
    def _parse_field_mapping_str(raw: str | None) -> dict[str, str]:
        """Parse ``key: value`` lines into a dict."""
        mapping: dict[str, str] = {}
        if not raw:
            return mapping
        for line in raw.splitlines():
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                mapping[key.strip()] = value.strip()
        return mapping

    def _parse_field_mapping(self) -> dict[str, str]:
        return self._parse_field_mapping_str(self.field_mapping)

    @staticmethod
    def _build_content_blocks(rendered_body: str, result: Data) -> list[dict]:
        """Build ContentBlock dicts for rich playground preview."""
        blocks: list[dict] = []
        tpl_name = result.data.get("template")
        status = result.data.get("status", "")

        # Header block
        header_text = (
            f"✅ Email {result.data.get('action', '')} — {status}"
            if status == "sent"
            else f"📝 Draft created — awaiting human review"
        )
        header_block = ContentBlock(
            title="Outlook",
            contents=[TextContent(text=header_text)],
        )
        blocks.append(header_block.model_dump())

        # Template preview block
        if tpl_name:
            tpl = get_template(tpl_name)
            tpl_desc = tpl["description"] if tpl else ""
            preview_block = ContentBlock(
                title=f"Template: {tpl_name}",
                contents=[
                    TextContent(text=tpl_desc),
                    CodeContent(code=rendered_body, language="html", title="Rendered Content"),
                ],
            )
            blocks.append(preview_block.model_dump())

        return blocks
