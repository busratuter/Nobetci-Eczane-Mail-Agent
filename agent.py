from agno.agent import Agent
from tools import nobetci_eczane_cek, mail_gonder

tools = [nobetci_eczane_cek, mail_gonder]

agent = Agent(
    name="NobetciEczaneAgent",
    description="Belirtilen il ve ilçedeki nöbetçi eczaneleri çekip Outlook ile e-posta gönderen agent.",
    tools=tools
)
