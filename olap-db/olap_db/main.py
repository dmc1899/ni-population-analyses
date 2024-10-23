import os

import duckdb
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def main():
    # Put your main program logic here
    key = os.getenv("MOTHERDUCK_KEY")

    # Initiate a MotherDuck connection using an access token
    # con = duckdb.connect(f'md:?motherduck_token={key}')
    con = duckdb.connect(f'md:?sslmode=disable')

    con.sql("SHOW DATABASES").show()
# TODO - "Request failed: failed to connect to all addresses; last error: UNKNOWN: ipv4:44.209.0.5:443: Cannot check peer: missing selected ALPN property. (UNAVAILABLE, RPC 'GET_WELCOME_PACK', request id: '8192b044-5538-456e-aa16-b1c67335e728')""

if __name__ == "__main__":
    main()
