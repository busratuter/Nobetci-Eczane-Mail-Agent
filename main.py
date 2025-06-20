from agent import agent
import os

def main():
    il = "İstanbul"
    ilce = "Kadıköy"
    to_email = os.getenv("GMAIL_USER","busratuter@gmail.com")

    prompt = f"{il} {ilce} için nöbetçi eczaneleri bul ve bulduğun eczaneleri {to_email} adresine mail at."

    print(f"Agent'a gönderilen prompt: '{prompt}'")
    
    # agno agent çalıştırma
    response = agent.run(prompt)


if __name__ == "__main__":
    main()