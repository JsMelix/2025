import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define el alcance (scope) de la API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    """Autenticación con la API de Gmail."""
    creds = None
    # Si ya existe un token, cargarlo
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Si no hay token o está vencido, solicitar autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guardar el token para futuras ejecuciones
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def delete_messages(service, query):
    """Busca y elimina mensajes según una consulta."""
    try:
        # Busca mensajes según el query
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No se encontraron mensajes para borrar.")
            return

        for message in messages:
            msg_id = message['id']
            # Borra el mensaje
            service.users().messages().delete(userId='me', id=msg_id).execute()
            print(f"Mensaje con ID {msg_id} borrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    # Autenticar la API
    service = authenticate_gmail()

    # Define una consulta (por ejemplo, mensajes con la palabra 'promoción')
    query = 'subject:promoción'

    # Borra los mensajes que coincidan con la consulta
    delete_messages(service, query)
