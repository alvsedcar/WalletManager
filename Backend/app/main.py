# Importamos librerías necesarias para el funcionamiento de la API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from utils.wallet import create_wallet, send_transaction, get_balance
from config.blockchain import get_web3

# Inicializamos el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Cargamos el archivo token.env que contiene las variables de entorno para mas seguridad
logger.info("Cargando variables de entorno...")
load_dotenv('token.env')


# Leer la API Key de Infura desde las variables de entorno
logger.info("Leyendo el project ID...")
infura_project_id = os.getenv('INFURA_PROJECT_ID')


# Variable global que almacena la conexión web3
w3 = get_web3(infura_project_id)

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Modelo de Pydantic para validar la estructura de la entrada de datos de la transacción
class Transaction(BaseModel):
    from_private_key: str
    to_address: str
    amount: float

# Endpoint para crear una nueva wallet
@app.post("/wallet/create")
async def api_create_wallet():
    logger.info("Creando una nueva wallet...")
    wallet = create_wallet(w3)
    return wallet

# Endpoint para enviar una transacción
@app.post("/wallet/transfer")
async def api_send_transaction(transaction: Transaction):
    logger.info("Enviando una transacción...")
    try:
        # Intenta realizar la transacción y devuelve el hash de la transacción
        tx_hash = send_transaction(transaction.from_private_key, transaction.to_address, transaction.amount,w3)
        return {"transaction_hash": tx_hash}
    
    except Exception as e:
        # Si ocurre un error, devuelve un mensaje de error con estado HTTP 400
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para consultar el saldo de una wallet
@app.get("/wallet/balance/{address}")
async def api_get_balance(address: str):
    logger.info("Consultando el saldo de una wallet...")
    balance = get_balance(address,w3)
    return {"balance": balance}

# Para ejecutar la API, usar en consola:
# uvicorn main.py:app --reload
