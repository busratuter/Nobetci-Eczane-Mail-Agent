from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools import nobetci_eczane_cek, mail_gonder

default_model = OpenAIChat() # default model gpt-4o

tools = [nobetci_eczane_cek, mail_gonder]

agent = Agent(
    name="NobetciEczaneAgent",
    description="Belirtilen il ve ilçedeki nöbetçi eczaneleri çekip Outlook ile e-posta gönderen agent.",
    tools=tools,
    model=default_model,
    markdown=True
)
