import requests

def get_request(url: str, payload: dict):
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("Falha de conexão") from e
    except requests.exceptions.Timeout as e:
        raise TimeoutError("Timeout na requisição") from e
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Erro HTTP {e.response.status_code}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro na requisição: {e}") from e
